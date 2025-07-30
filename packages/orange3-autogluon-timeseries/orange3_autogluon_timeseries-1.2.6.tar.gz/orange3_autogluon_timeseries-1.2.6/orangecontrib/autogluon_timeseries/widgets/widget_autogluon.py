import logging
import os
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from Orange.data import Table, Domain, ContinuousVariable, StringVariable, DiscreteVariable, TimeVariable, Variable
import pandas as pd
import numpy as np
import tempfile
from autogluon.timeseries import TimeSeriesPredictor, TimeSeriesDataFrame
from datetime import datetime, timedelta
from pathlib import Path
import traceback
from Orange.widgets.utils.widgetpreview import WidgetPreview
from PyQt5.QtWidgets import QPlainTextEdit, QCheckBox, QComboBox, QLabel
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont
import holidays # Импортируем библиотеку holidays
import warnings

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OWAutoGluonTimeSeries(OWWidget):
    name = "AutoGluon TimeSeries"
    description = "Прогнозирование временных рядов с AutoGluon"
    icon = "icons/autogluon.png"
    priority = 100
    keywords = ["timeseries", "forecast", "autogluon"]

    # Настройки
    prediction_length = settings.Setting(10)
    time_limit = settings.Setting(60)
    selected_metric = settings.Setting("MAE")
    selected_preset = settings.Setting("best_quality")
    target_column = settings.Setting("sales")
    id_column = settings.Setting("item_id")
    timestamp_column = settings.Setting("timestamp")
    include_holidays = settings.Setting(False)
    use_current_date = settings.Setting(True)  # Настройка для использования текущей даты
    frequency = settings.Setting("D")  # Частота для прогноза (по умолчанию дни)
    auto_frequency = settings.Setting(True)  # Автоопределение частоты
    selected_model = settings.Setting("auto") # выбор моделей
    holiday_country = settings.Setting("RU") # Страна для праздников

    # Метрики
    METRICS = ["MAE", "MAPE", "MSE", "RMSE", "WQL"]
    
    # Частоты
    FREQUENCIES = [
        ("D", "День"),
        ("W", "Неделя"),
        ("M", "Месяц"),
        ("Q", "Квартал"),
        ("Y", "Год"),
        ("H", "Час"),
        ("T", "Минута"),
        ("B", "Рабочий день")
    ]
    # Доступные страны для праздников (можно расширить)
    HOLIDAY_COUNTRIES = ["RU", "US", "GB", "DE", "FR", "CA"]


    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        prediction = Output("Prediction", Table)
        leaderboard = Output("Leaderboard", Table)
        model_info = Output("Model Info", Table)
        log_messages = Output("Log", str)

    def __init__(self):
        super().__init__()
        self.data = None
        self.predictor = None
        self.log_messages = ""
        self.detected_frequency = "D"  # Определенная частота данных по умолчанию
        self.mainArea.hide()
        self.setup_ui()
        self.warning("")
        self.error("")
        self.log("Виджет инициализирован")
        
        # Данные для валидации длины прогноза
        self.max_allowed_prediction = 0
        self.data_length = 0
        self.from_form_timeseries = False  # Флаг для определения источника данных
        self.categorical_mapping = {} # для сопоставления категориальных значений

    def setup_ui(self):

        # Основные параметры
        box = gui.widgetBox(self.controlArea, "Параметры")
        self.prediction_spin = gui.spin(box, self, "prediction_length", 1, 365, 1, label="Длина прогноза:")
        self.prediction_spin.valueChanged.connect(self.on_prediction_length_changed)
        
        # Добавляем информационную метку о максимальной длине прогноза
        self.max_length_label = QLabel("Максимальная длина прогноза: N/A")
        box.layout().addWidget(self.max_length_label)
        
        gui.spin(box, self, "time_limit", 10, 86400, 10, label="Лимит времени (сек):")
        
        # Используем строки для метрик
        self.metric_combo = gui.comboBox(box, self, "selected_metric", 
                    items=self.METRICS,
                    label="Метрика:")
        
        self.model_selector = gui.comboBox(
            box, self, "selected_preset",
            items=["best_quality", "high_quality", "medium_quality", "fast_training"],
            label="Пресет:",
            sendSelectedValue=True
        )

        # Добавляем выбор моделей
        self.model_selector = gui.comboBox(
            box, self, "selected_model",
            items=["auto", "DirectTabular", "ETS", "DeepAR", "MLP", "TemporalFusionTransformer", "TiDE"],
            label="Модель autogluon:",
            sendSelectedValue=True  # вот это ключевое!
        )
        
        # Настройки столбцов
        col_box = gui.widgetBox(self.controlArea, "Столбцы")
        # Хранение всех колонок для выпадающего списка
        self.all_columns = []
        
        # Целевая переменная
        self.target_combo = gui.comboBox(col_box, self, "target_column", label="Целевая:", 
                                         items=[], sendSelectedValue=True,
                                         callback=self.on_target_column_changed) 
        # ID ряда
        self.id_combo = gui.comboBox(col_box, self, "id_column", label="ID ряда:", 
                                     items=[], sendSelectedValue=True,
                                     callback=self.on_id_column_changed) 
        # Временная метка
        self.timestamp_combo = gui.comboBox(col_box, self, "timestamp_column", label="Время:", 
                                            items=[], sendSelectedValue=True,
                                            callback=self.on_timestamp_column_changed) 
        
        # Настройки частоты
        freq_box = gui.widgetBox(self.controlArea, "Частота временного ряда")
        
        # Чекбокс для автоопределения частоты
        self.auto_freq_checkbox = QCheckBox("Автоматически определять частоту")
        self.auto_freq_checkbox.setChecked(self.auto_frequency)
        self.auto_freq_checkbox.stateChanged.connect(self.on_auto_frequency_changed)
        freq_box.layout().addWidget(self.auto_freq_checkbox)
        
        # Выпадающий список частот
        self.freq_combo = gui.comboBox(freq_box, self, "frequency", 
                      items=[f[0] for f in self.FREQUENCIES], 
                      label="Частота:")
        # Заменяем технические обозначения на понятные названия
        for i, (code, label) in enumerate(self.FREQUENCIES):
            self.freq_combo.setItemText(i, f"{label} ({code})")
        
        # Отключаем комбобокс, если автоопределение включено
        self.freq_combo.setDisabled(self.auto_frequency)
        
        # Метка для отображения определенной частоты
        self.detected_freq_label = QLabel("Определенная частота: N/A")
        freq_box.layout().addWidget(self.detected_freq_label)

        # Дополнительные настройки
        extra_box = gui.widgetBox(self.controlArea, "Дополнительно")
        self.holidays_checkbox = QCheckBox("Учитывать праздники")
        self.holidays_checkbox.setChecked(self.include_holidays)
        self.holidays_checkbox.stateChanged.connect(self.on_holidays_changed)
        extra_box.layout().addWidget(self.holidays_checkbox)

        # Добавляем выбор страны для праздников
        self.holiday_country_combo = gui.comboBox(extra_box, self, "holiday_country",
                                                  label="Страна для праздников:",
                                                  items=self.HOLIDAY_COUNTRIES,
                                                  sendSelectedValue=True)
        self.holiday_country_combo.setEnabled(self.include_holidays) # Активируем только если включены праздники
        
        # Настройка для принудительного использования текущей даты
        self.date_checkbox = QCheckBox("Использовать текущую дату (игнорировать даты в данных)")
        self.date_checkbox.setChecked(self.use_current_date)
        self.date_checkbox.stateChanged.connect(self.on_date_option_changed)
        extra_box.layout().addWidget(self.date_checkbox)

        # кнопка
        self.run_button = gui.button(self.controlArea, self, "Запустить", callback=self.run_model)

        # логи
        log_box_main = gui.widgetBox(self.controlArea, "Логи", addSpace=True)
        self.log_widget = QPlainTextEdit(readOnly=True)
        self.log_widget.setMinimumHeight(200)
        font = QFont("Monospace")
        font.setStyleHint(QFont.TypeWriter)
        self.log_widget.setFont(font)
        log_box_main.layout().addWidget(self.log_widget)

    def on_target_column_changed(self):
        self.log(f"Пользователь выбрал целевую колонку: {self.target_column}")
    def on_id_column_changed(self):
        self.log(f"Пользователь выбрал ID колонку: {self.id_column}")
    def on_timestamp_column_changed(self):
        self.log(f"Пользователь выбрал временную колонку: {self.timestamp_column}")

    def on_holidays_changed(self, state):
        self.include_holidays = state > 0
        self.holiday_country_combo.setEnabled(self.include_holidays) # Включаем/отключаем выбор страны

    def on_date_option_changed(self, state):
        self.use_current_date = state > 0
        
    def on_auto_frequency_changed(self, state):
        self.auto_frequency = state > 0
        self.freq_combo.setDisabled(self.auto_frequency)
        if self.auto_frequency and self.data is not None:
            self.detected_freq_label.setText(f"Определенная частота: {self.detected_frequency}")
        
    def on_prediction_length_changed(self, value):
        """Проверяет валидность выбранной длины прогноза"""
        if self.data_length > 0:
            # Обновляем интерфейс и проверяем валидность
            self.check_prediction_length()

    def detect_frequency(self, data):
        """Определяет частоту временного ряда на основе данных"""
        try:
            # Сортируем даты
            dates = data[self.timestamp_column].sort_values()
            
            # Если меньше 2 точек, невозможно определить
            if len(dates) < 2:
                return "D"  # По умолчанию день
                
            # Вычисляем разницу между последовательными датами
            diffs = []
            for i in range(1, min(10, len(dates))):
                diff = dates.iloc[i] - dates.iloc[i-1]
                diffs.append(diff.total_seconds())
                
            # Используем медиану для определения типичного интервала
            if not diffs:
                return "D"
                
            median_diff = pd.Series(diffs).median()
            
            # Определяем частоту на основе интервала
            if median_diff <= 60:  # до 1 минуты
                freq = "T"
            elif median_diff <= 3600:  # до 1 часа
                freq = "H"
            elif median_diff <= 86400:  # до 1 дня
                freq = "D"
            elif median_diff <= 604800:  # до 1 недели
                freq = "W"
            elif median_diff <= 2678400:  # до ~1 месяца (31 день)
                freq = "M"
            elif median_diff <= 7948800:  # до ~3 месяцев (92 дня)
                freq = "Q"
            else:  # более 3 месяцев
                freq = "Y"
                
            self.log(f"Определена частота данных: {freq} (медианный интервал: {median_diff/3600:.1f} часов)")
            return freq
            
        except Exception as e:
            self.log(f"Ошибка при определении частоты: {str(e)}")
            return "D"  # По умолчанию день

    def check_prediction_length(self):
        """Проверяет длину прогноза и обновляет интерфейс"""
        if self.data_length == 0:
            return
            
        # Корректируем формулу расчета максимальной длины прогноза
        # Предыдущая формула: max(1, (self.data_length - 3) // 2)
        # Новая формула: более либеральная для данных средней длины
        
        if self.data_length <= 10:
            # Для очень коротких временных рядов очень строгое ограничение
            self.max_allowed_prediction = max(1, self.data_length // 3)
        elif self.data_length <= 30:
            # Для средних временных рядов - более либеральное ограничение
            # Для 21 строки: (21 - 1) // 2 = 10
            self.max_allowed_prediction = max(1, (self.data_length - 1) // 2)
        else:
            # Для длинных временных рядов - стандартное ограничение
            self.max_allowed_prediction = max(1, (self.data_length - 3) // 2)
            
        self.max_length_label.setText(f"Максимальная длина прогноза: {self.max_allowed_prediction}")
        
        # Проверка текущего значения
        if self.prediction_length > self.max_allowed_prediction:
            self.warning(f"Длина прогноза слишком велика для ваших данных. Максимум: {self.max_allowed_prediction}")
            # Визуальное предупреждение
            self.max_length_label.setStyleSheet("color: red; font-weight: bold")
            # Отключаем кнопку запуска, если прогноз слишком длинный
            self.run_button.setDisabled(True)
        else:
            self.warning("")
            self.max_length_label.setStyleSheet("")
            self.run_button.setDisabled(False)

    def log(self, message):
        """Надежное логирование"""
        log_entry = f"{datetime.now().strftime('%H:%M:%S')} - {message}"
        self.log_messages += log_entry + "\n"
        self.log_widget.appendPlainText(log_entry)
        self.log_widget.verticalScrollBar().setValue(
            self.log_widget.verticalScrollBar().maximum()
        )
        QCoreApplication.processEvents()

    @Inputs.data
    def set_data(self, dataset):
        self.error("")
        self.warning("")
        try:
            if dataset is None:
                self.data = None
                self.log("Данные очищены")
                self.data_length = 0
                self.max_length_label.setText("Максимальная длина прогноза: N/A")
                self.detected_freq_label.setText("Определенная частота: N/A")
                return
            
            # Проверка наличия специальных атрибутов от FormTimeseries
            self.from_form_timeseries = False  # Сбрасываем флаг
            if hasattr(dataset, 'from_form_timeseries') and dataset.from_form_timeseries:
                self.from_form_timeseries = True
                self.log("Данные получены из компонента FormTimeseries")
                # Если данные от FormTimeseries, можно получить дополнительную информацию
                if hasattr(dataset, 'time_variable') and dataset.time_variable:
                    self.timestamp_column = dataset.time_variable
                    self.log(f"Автоматически установлена временная переменная: {self.timestamp_column}")
            

            # Получаем колонки из dataset ДО prepare_data
            domain = dataset.domain
            attr_cols = [var.name for var in domain.attributes]
            meta_cols = [var.name for var in domain.metas]
            class_cols = [var.name for var in domain.class_vars] if domain.class_vars else []
            self.all_columns = attr_cols + class_cols + meta_cols
            
            # Находим и сохраняем категориальные маппинги
            self.categorical_mapping = {}  # Сбрасываем предыдущие маппинги
            for var in domain.variables + domain.metas:
                if hasattr(var, 'values') and var.values:
                    # Получаем список значений категориальной переменной
                    values = var.values
                    if values:
                        self.log(f"Сохраняем маппинг для категориальной переменной '{var.name}': {values}")
                        self.categorical_mapping[var.name] = values

            # ДОБАВЛЕНО: Проверяем наличие TimeVariable
            time_vars = []
            for var in domain.variables + domain.metas:
                if isinstance(var, TimeVariable):
                    time_vars.append(var.name)
            
            if time_vars:
                self.log(f"Обнаружены временные переменные: {', '.join(time_vars)}")
                if self.timestamp_column not in time_vars:
                    # Автоматически выбираем первую временную переменную
                    self.timestamp_column = time_vars[0]
                    self.log(f"Автоматически выбрана временная переменная (TimeVariable по умолчанию): {self.timestamp_column}")
            
            if not self.all_columns:
                raise ValueError("Нет колонок в данных!")
            
            # --- Автоматическое определение столбцов ---
            # Пытаемся определить, только если текущий выбор невалиден или не сделан
            
            # Получаем DataFrame для проверки типов, если еще не создан
            temp_df_for_types = None
            if not isinstance(dataset, pd.DataFrame): # Если на вход пришел Orange.data.Table
                temp_df_for_types = self.prepare_data(dataset, for_type_check_only=True)
            else: # Если на вход уже пришел DataFrame (маловероятно для set_data, но для полноты)
                temp_df_for_types = dataset

            # Целевой столбец
            if not self.target_column or self.target_column not in self.all_columns:
                self.log(f"Целевой столбец '{self.target_column}' не установлен или не найден в текущих данных. Попытка автоопределения...")
                potential_target = None
                
                # 1. Проверяем Orange Class Variable
                if domain.class_vars:
                    for cv in domain.class_vars:
                        if isinstance(cv, ContinuousVariable) or \
                           (temp_df_for_types is not None and cv.name in temp_df_for_types.columns and pd.api.types.is_numeric_dtype(temp_df_for_types[cv.name])):
                            potential_target = cv.name
                            self.log(f"Найдена целевая колонка из Orange Class Variable: '{potential_target}'")
                            break
                
                if not potential_target:
                    # 2. Ищем по приоритетным точным именам
                    priority_names = ["Target", "target", "sales", "Sales", "value", "Value"]
                    for name in priority_names:
                        if name in self.all_columns and \
                           (temp_df_for_types is not None and name in temp_df_for_types.columns and pd.api.types.is_numeric_dtype(temp_df_for_types[name])):
                            potential_target = name
                            self.log(f"Найдена целевая колонка по точному приоритетному имени: '{potential_target}'")
                            break
                
                if not potential_target and self.all_columns and temp_df_for_types is not None:
                    # 3. Ищем по подстрокам (числовые)
                    search_terms = ["target", "sales", "value"]
                    for term in search_terms:
                        for col_name in self.all_columns:
                            if term in col_name.lower() and col_name in temp_df_for_types.columns and \
                               pd.api.types.is_numeric_dtype(temp_df_for_types[col_name]):
                                potential_target = col_name
                                self.log(f"Найдена целевая колонка по подстроке '{term}': '{potential_target}' (числовая)")
                                break
                        if potential_target: break

                if not potential_target and self.all_columns and temp_df_for_types is not None:
                    # 4. Берем первую числовую Orange ContinuousVariable, не являющуюся ID или Timestamp
                    for var in domain.attributes: # Атрибуты обычно числовые или категориальные
                        if isinstance(var, ContinuousVariable) and var.name not in [self.id_column, self.timestamp_column]:
                             potential_target = var.name
                             self.log(f"В качестве целевой колонки выбрана первая Orange ContinuousVariable: '{potential_target}'")
                             break
                    if not potential_target: # Если не нашли среди атрибутов, ищем просто числовую
                        for col in self.all_columns:
                            if col not in [self.id_column, self.timestamp_column] and \
                               col in temp_df_for_types.columns and pd.api.types.is_numeric_dtype(temp_df_for_types[col]):
                                potential_target = col
                                self.log(f"В качестве целевой колонки выбрана первая числовая: '{potential_target}'")
                                break

                self.target_column = potential_target if potential_target else (self.all_columns[0] if self.all_columns else "")
                self.log(f"Автоматически выбран целевой столбец: '{self.target_column}'")

            # ID столбец
            if not self.id_column or self.id_column not in self.all_columns:
                self.log(f"ID столбец '{self.id_column}' не установлен или не найден в текущих данных. Попытка автоопределения...")
                potential_id = None
                # 1. Ищем Orange DiscreteVariable или StringVariable (не цель и не время)
                for var_list in [domain.attributes, domain.metas]:
                    for var in var_list:
                        if var.name not in [self.target_column, self.timestamp_column] and \
                           (isinstance(var, DiscreteVariable) or isinstance(var, StringVariable)):
                            potential_id = var.name
                            self.log(f"Найдена ID колонка из Orange Discrete/String Variable: '{potential_id}'")
                            break
                    if potential_id: break
                
                if not potential_id:
                    # 2. Поиск по стандартным именам
                    potential_id = next((name for name in ["item_id", "id", "ID", "Country", "Shop", "City"] if name in self.all_columns and name not in [self.target_column, self.timestamp_column]), None)
                    if potential_id: self.log(f"Найдена ID колонка по стандартному имени: '{potential_id}'")

                if not potential_id and self.all_columns and temp_df_for_types is not None:
                    # 3. Ищем подходящий тип (строка/объект/категория), не цель и не время
                    for col in self.all_columns:
                        if col not in [self.target_column, self.timestamp_column] and col in temp_df_for_types.columns and \
                           (pd.api.types.is_string_dtype(temp_df_for_types[col]) or \
                            pd.api.types.is_object_dtype(temp_df_for_types[col]) or \
                            pd.api.types.is_categorical_dtype(temp_df_for_types[col])):
                            potential_id = col
                            self.log(f"Найдена подходящая по типу ID колонка: '{potential_id}'")
                            break
                self.id_column = potential_id if potential_id else (next((c for c in self.all_columns if c not in [self.target_column, self.timestamp_column]), self.all_columns[0] if self.all_columns else ""))
                self.log(f"Автоматически выбран ID столбец: '{self.id_column}'")

            # Временной столбец (если не определен как TimeVariable и невалиден)
            if not self.timestamp_column or self.timestamp_column not in self.all_columns:
                self.log(f"Временной столбец '{self.timestamp_column}' не установлен/не найден или не является TimeVariable. Попытка автоопределения...")
                potential_ts = None
                # 1. Orange TimeVariable уже должен был быть выбран ранее в set_data.
                # Здесь мы ищем, если он не был TimeVariable или стал невалидным.
                
                # 2. Поиск по стандартным именам
                potential_ts = next((name for name in ["timestamp", "Timestamp", "time", "Time", "Date", "date"] if name in self.all_columns and name not in [self.target_column, self.id_column]), None)
                if potential_ts: self.log(f"Найдена временная колонка по стандартному имени: '{potential_ts}'")

                if not potential_ts and self.all_columns and temp_df_for_types is not None:
                    # 3. Пытаемся распарсить
                    for col in self.all_columns:
                        if col not in [self.target_column, self.id_column] and col in temp_df_for_types.columns:
                            try:
                                parsed_sample = pd.to_datetime(temp_df_for_types[col].dropna().iloc[:5], errors='coerce')
                                if not parsed_sample.isna().all():
                                    potential_ts = col
                                    self.log(f"Найдена подходящая по типу временная колонка: '{potential_ts}' (можно преобразовать в дату)")
                                    break
                            except Exception:
                                continue
                self.timestamp_column = potential_ts if potential_ts else (next((c for c in self.all_columns if c not in [self.target_column, self.id_column]), self.all_columns[0] if self.all_columns else ""))
                self.log(f"Автоматически выбран временной столбец: '{self.timestamp_column}'")
            
            self.log("Обработка входных данных...")
            self.data = self.prepare_data(dataset)
            
            # Обновляем выпадающие списки колонок
            self.target_combo.clear()
            self.id_combo.clear()
            self.timestamp_combo.clear()
            
            self.target_combo.addItems(self.all_columns)
            self.id_combo.addItems(self.all_columns)
            self.timestamp_combo.addItems(self.all_columns)
            
            # Устанавливаем выбранные значения в comboBox'ах
            self.target_combo.setCurrentText(self.target_column)
            self.id_combo.setCurrentText(self.id_column)
            self.timestamp_combo.setCurrentText(self.timestamp_column)
            
            # Логируем финальный выбор колонок после автоопределения (если оно было) и установки в UI
            self.log(f"Автоопределены колонки — Target: {self.target_column}, ID: {self.id_column}, Timestamp: {self.timestamp_column}")
            
            required = {self.timestamp_column, self.target_column, self.id_column}
            if not required.issubset(set(self.data.columns)):
                missing = required - set(self.data.columns)
                raise ValueError(f"Отсутствуют столбцы: {missing}")
                
            # Получаем длину данных
            self.data_length = len(self.data)
            self.log(f"Загружено {self.data_length} записей")
            
            # Определяем частоту данных
            if pd.api.types.is_datetime64_dtype(self.data[self.timestamp_column]):
                self.detected_frequency = self.detect_frequency(self.data)
                self.detected_freq_label.setText(f"Определенная частота: {self.detected_frequency}")
            
            # Обновляем максимальную длину прогноза
            self.check_prediction_length()
            
            # Если нужно заменить даты на текущую
            if self.use_current_date and self.timestamp_column in self.data.columns:
                self.log("Применяется замена дат на актуальные")
                
                # Получаем частоту
                freq = self.detected_frequency if self.auto_frequency else self.frequency
                
                try:
                    # Создаем даты от сегодня назад с нужной частотой
                    today = pd.Timestamp.now().normalize()
                    dates = pd.date_range(end=today, periods=len(self.data), freq=freq)
                    dates = dates.sort_values()  # Сортируем от ранних к поздним
                    
                    # Заменяем столбец времени
                    self.data[self.timestamp_column] = dates
                    self.log(f"Даты заменены: от {dates.min().strftime('%Y-%m-%d')} до {dates.max().strftime('%Y-%m-%d')}")
                except Exception as e:
                    self.log(f"Ошибка при создании дат с частотой {freq}: {str(e)}. Используем ежедневную частоту.")
                    # Резервный вариант - ежедневная частота
                    dates = pd.date_range(end=pd.Timestamp.now().normalize(), periods=len(self.data), freq='D')
                    self.data[self.timestamp_column] = dates
            
        except Exception as e:
            self.log(f"ОШИБКА: {str(e)}\n{traceback.format_exc()}")
            self.error(f"Ошибка данных: {str(e)}")
            self.data = None
            self.data_length = 0
            self.max_length_label.setText("Максимальная длина прогноза: N/A")

    def prepare_data(self, table, for_type_check_only=False):
        """Подготовка данных"""
        if table is None:
            if not for_type_check_only: self.log("prepare_data вызван с None table")
            return None

        domain = table.domain
        # Получаем атрибуты
        attr_cols = [var.name for var in domain.attributes]
        df = pd.DataFrame(table.X, columns=attr_cols)
        
        # Добавляем классы, если есть
        if domain.class_vars:
            class_cols = [var.name for var in domain.class_vars]
            class_data = table.Y
            if len(domain.class_vars) == 1:
                class_data = class_data.reshape(-1, 1)
            df_class = pd.DataFrame(class_data, columns=class_cols)
            df = pd.concat([df, df_class], axis=1)
        
        # Добавляем мета-атрибуты
        if domain.metas:
            meta_cols = [var.name for var in domain.metas]
            meta_data = table.metas
            df_meta = pd.DataFrame(meta_data, columns=meta_cols)
            df = pd.concat([df, df_meta], axis=1)
        
        if for_type_check_only: # Если только для проверки типов, возвращаем как есть
            return df

        # --- Преобразования типов для фактического использования ---
        if self.timestamp_column and self.timestamp_column in df.columns:
            try:
                is_datetime_var = any(var.name == self.timestamp_column and isinstance(var, TimeVariable) for var in domain.variables + domain.metas)
                if not is_datetime_var:
                    if pd.api.types.is_object_dtype(df[self.timestamp_column]) or pd.api.types.is_string_dtype(df[self.timestamp_column]):
                        self.log(f"Попытка распарсить '{self.timestamp_column}' как дату/время...")
                        # Сначала пробуем автоматическое определение, оно часто работает хорошо
                        parsed_dates = pd.to_datetime(df[self.timestamp_column], errors='coerce')
                        if not parsed_dates.isna().all(): # Если хоть что-то распарсилось
                            df[self.timestamp_column] = parsed_dates
                            self.log(f"'{self.timestamp_column}' успешно преобразована в datetime (авто).")
                        else: # Если авто не сработало, пробуем форматы
                            for fmt in ['%Y-%m-%d', '%d.%m.%Y', '%Y/%m/%d', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S', '%d.%m.%Y %H:%M:%S']:
                                try:
                                    df[self.timestamp_column] = pd.to_datetime(df[self.timestamp_column], format=fmt, errors='raise')
                                    self.log(f"'{self.timestamp_column}' успешно распознано с форматом {fmt}.")
                                    break
                                except Exception:
                                    continue
                            else: # Если ни один формат не подошел
                                self.log(f"Не удалось распознать формат даты для '{self.timestamp_column}'. Оставляем как есть или будет ошибка позже.")
                    elif pd.api.types.is_numeric_dtype(df[self.timestamp_column]):
                        self.log(f"'{self.timestamp_column}' является числовой. Попытка преобразования из Unix timestamp...")
                        df[self.timestamp_column] = pd.to_datetime(df[self.timestamp_column], unit='s', errors='coerce')
                self.log(f"Тип данных '{self.timestamp_column}' после обработки: {df[self.timestamp_column].dtype}")
            except Exception as e:
                self.log(f"Ошибка при обработке временной колонки '{self.timestamp_column}': {str(e)}")

        if self.target_column and self.target_column in df.columns:
            df[self.target_column] = pd.to_numeric(df[self.target_column], errors="coerce")
            self.log(f"Тип данных '{self.target_column}' после преобразования в числовой: {df[self.target_column].dtype}")

        if self.id_column and self.id_column in df.columns:
            df[self.id_column] = df[self.id_column].astype(str)
            self.log(f"Тип данных '{self.id_column}' после преобразования в строку: {df[self.id_column].dtype}")
        
        # Удаляем строки, где ключевые колонки (после преобразований) стали NaT/NaN
        cols_to_check_na = []
        if self.timestamp_column and self.timestamp_column in df.columns: cols_to_check_na.append(self.timestamp_column)
        if self.target_column and self.target_column in df.columns: cols_to_check_na.append(self.target_column)
        if self.id_column and self.id_column in df.columns: cols_to_check_na.append(self.id_column)
        
        return df.dropna(subset=cols_to_check_na) if cols_to_check_na else df

    def create_future_dates(self, periods):
        """Создает будущие даты с учетом нужной частоты"""
        # ✅ Выбор стартовой даты
        if self.use_current_date:
            last_date = pd.Timestamp.now().normalize()
            self.log("Используется текущая дата для старта прогноза")
        else:
            # Берем последнюю дату из временного ряда
            try:
                self.log(f"DEBUG create_future_dates: self.data[{self.timestamp_column}].dtype = {self.data[self.timestamp_column].dtype}")
                self.log(f"DEBUG create_future_dates: self.data[{self.timestamp_column}].head() = \n{self.data[self.timestamp_column].head().to_string()}")
                self.log(f"DEBUG create_future_dates: self.data[{self.timestamp_column}].tail() = \n{self.data[self.timestamp_column].tail().to_string()}")
                raw_last_date = self.data[self.timestamp_column].max()
                self.log(f"Используется последняя дата из данных (сырое значение): {raw_last_date}, тип: {type(raw_last_date)}")
                
                if isinstance(raw_last_date, pd.Timestamp) or pd.api.types.is_datetime64_any_dtype(raw_last_date):
                    last_date = pd.Timestamp(raw_last_date) # Убедимся, что это Timestamp объект
                    self.log(f"Последняя дата уже является datetime: {last_date}")
                elif isinstance(raw_last_date, (int, float)):
                    self.log(f"Последняя дата - число: {raw_last_date}. Попытка преобразования из Unix timestamp.")
                    # Попробуем определить масштаб (секунды, миллисекунды, микросекунды, наносекунды)
                    # Год 2000 в секундах: ~9.4e8, в мс: ~9.4e11, в мкс: ~9.4e14, в нс: ~9.4e17
                    # Год 2030 в секундах: ~1.9e9
                    if pd.Timestamp("2000-01-01").timestamp() < raw_last_date < pd.Timestamp("2050-01-01").timestamp(): # Вероятно, секунды
                        last_date = pd.Timestamp(raw_last_date, unit='s')
                        self.log(f"Преобразовано из секунд: {last_date}")
                    elif pd.Timestamp("2000-01-01").timestamp() * 1000 < raw_last_date < pd.Timestamp("2050-01-01").timestamp() * 1000: # Вероятно, миллисекунды
                        last_date = pd.Timestamp(raw_last_date, unit='ms')
                        self.log(f"Преобразовано из миллисекунд: {last_date}")
                    # Можно добавить проверки для микро- и наносекунд, если необходимо
                    else:
                        # Если масштаб неясен или значение слишком мало/велико, пробуем авто
                        try:
                            last_date = pd.to_datetime(raw_last_date)
                            self.log(f"Преобразовано pd.to_datetime (авто): {last_date}")
                        except:
                            last_date = pd.Timestamp.now().normalize()
                            self.log(f"Не удалось определить масштаб timestamp или преобразовать. Используем текущую дату: {last_date}")
                else: # Строка или другой тип
                    try:
                        last_date = pd.to_datetime(raw_last_date)
                        self.log(f"Последняя дата преобразована из другого типа ({type(raw_last_date)}): {last_date}")
                    except Exception as e_conv:
                        self.log(f"Не удалось преобразовать последнюю дату '{raw_last_date}' в datetime: {e_conv}. Используем текущую дату.")
                        last_date = pd.Timestamp.now().normalize()

            except Exception as e:
                self.log(f"Ошибка при получении/обработке последней даты: {e}")
                last_date = pd.Timestamp.now().normalize()

        # Определяем частоту
        freq = self.detected_frequency if self.auto_frequency else self.frequency
        self.log(f"Создание будущих дат от {last_date} с частотой {freq}")
        
        try:
            # Создаем диапазон дат
            if freq == 'B':
                all_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=periods * 2, freq='D')
                dates = all_dates[all_dates.weekday < 5][:periods]
            else:
                dates = pd.date_range(start=last_date + pd.tseries.frequencies.to_offset(freq), periods=periods, freq=freq)
        except Exception as e:
            self.log(f"Ошибка при создании дат: {e}")
            
            # Более надежный запасной вариант
            try:
                # Пробуем просто создать последовательность дат начиная с завтра
                start_date = pd.Timestamp.now().normalize() + pd.Timedelta(days=1)
                dates = pd.date_range(start=start_date, periods=periods, freq='D')
                self.log(f"Используем альтернативные даты с {start_date}")
            except:
                # Если и это не работает, создаем фиксированные даты
                base_date = pd.Timestamp('2023-06-01')
                dates = pd.date_range(start=base_date, periods=periods, freq='D')
                self.log(f"Используем фиксированные даты с {base_date}")

        self.log(f"Создан диапазон дат: с {dates[0]} по {dates[-1]}")
        return dates

    def run_model(self):
        if self.data is None:
            self.error("Нет данных")
            self.log("Ошибка: данные не загружены")
            return
            
        # Глубокая диагностика структуры данных
        self.log(f"=== ДИАГНОСТИКА ДАННЫХ ===")
        self.log(f"Тип объекта данных: {type(self.data)}")
        
        # Проверяем, DataFrame ли это
        if not isinstance(self.data, pd.DataFrame):
            self.log("Данные не являются pandas DataFrame, пытаюсь преобразовать")
            # Попытка получить исходный Table, если self.data был изменен
            # Это рискованно, если set_data не вызывался с Table
            # Для безопасности, лучше полагаться на то, что self.data уже DataFrame
            try:
                # Если self.data это Table, преобразуем
                if isinstance(self.data, Table): # type: ignore
                    self.data = self.prepare_data(self.data) # prepare_data ожидает Table
                    self.log("Преобразование из Table в DataFrame успешно")
                else:
                    # Если это что-то другое, но не DataFrame, это проблема
                    self.error("Данные имеют неожиданный тип и не могут быть обработаны.")
                    return
            except Exception as e:
                self.log(f"Ошибка преобразования в DataFrame: {str(e)}")
                self.error("Невозможно преобразовать данные в нужный формат")
                return
        
        # Теперь у нас должен быть DataFrame
        self.log(f"Колонки в DataFrame для анализа: {list(self.data.columns)}")
        self.log(f"Колонки, выбранные в UI (или по умолчанию): ID='{self.id_column}', Время='{self.timestamp_column}', Цель='{self.target_column}'")

        # --- Проверка выбранных колонок ---
        # ID колонка
        if not self.id_column or self.id_column not in self.data.columns:
            self.error(f"Выбранная ID колонка '{self.id_column}' отсутствует в данных. Пожалуйста, выберите корректную колонку.")
            return
        # Преобразуем ID колонку в строку на всякий случай, если она еще не такая
        if not pd.api.types.is_string_dtype(self.data[self.id_column]):
            self.data[self.id_column] = self.data[self.id_column].astype(str)
            self.log(f"ID колонка '{self.id_column}' приведена к строковому типу.")

        # Временная колонка
        if not self.timestamp_column or self.timestamp_column not in self.data.columns:
            self.error(f"Выбранная временная колонка '{self.timestamp_column}' отсутствует в данных. Пожалуйста, выберите корректную колонку.")
            return
        if not pd.api.types.is_datetime64_any_dtype(self.data[self.timestamp_column]):
             # Попытка преобразования, если еще не datetime
            try:
                self.data[self.timestamp_column] = pd.to_datetime(self.data[self.timestamp_column], errors='raise')
                self.log(f"Временная колонка '{self.timestamp_column}' успешно преобразована в datetime.")
            except Exception as e:
                self.error(f"Выбранная временная колонка '{self.timestamp_column}' не может быть преобразована в формат даты/времени: {e}")
                return

        # Целевая колонка
        if not self.target_column or self.target_column not in self.data.columns:
            self.error(f"Выбранная целевая колонка '{self.target_column}' отсутствует в данных. Пожалуйста, выберите корректную колонку.")
            return
        if not pd.api.types.is_numeric_dtype(self.data[self.target_column]):
            # Попытка преобразования в числовой тип
            try:
                self.data[self.target_column] = pd.to_numeric(self.data[self.target_column], errors='raise')
                self.log(f"Целевая колонка '{self.target_column}' успешно преобразована в числовой тип.")
            except Exception as e:
                self.error(f"Выбранная целевая колонка '{self.target_column}' не является числовой и не может быть преобразована: {e}")
                return
            
        # Теперь должны быть найдены все колонки
        self.log(f"Финально используемые колонки для модели: ID='{self.id_column}', Время='{self.timestamp_column}', Цель='{self.target_column}'")
        
        # Безопасная сортировка с обработкой ошибок
        try:
            self.log("Попытка сортировки данных...")
            df_sorted = self.data.sort_values([self.id_column, self.timestamp_column])
            self.log("Сортировка успешна")
        except Exception as e:
            self.log(f"Ошибка при сортировке: {str(e)}")
            
            # Проверяем, может ли это быть проблема с индексом вместо имени колонки
            if "KeyError: 1" in str(e) or "KeyError: 0" in str(e):
                self.log("Обнаружена ошибка с индексом. Пробую альтернативный подход")
                # Создаем копию с гарантированными колонками
                df_temp = self.data.copy()
                
                # Если нужная колонка отсутствует или имеет неверное имя, создаем новую
                if self.id_column not in df_temp.columns:
                    df_temp['item_id'] = 'single_item'
                    self.id_column = 'item_id'
                
                try:
                    df_sorted = df_temp.sort_values([self.id_column, self.timestamp_column])
                    self.log("Альтернативная сортировка успешна")
                except:
                    # Если и это не работает, создаем полностью новый DataFrame
                    self.log("Создаю новый DataFrame с правильной структурой")
                    df_new = pd.DataFrame()
                    df_new['item_id'] = ['item_1'] * len(self.data)
                    df_new[self.timestamp_column] = self.data[self.timestamp_column].copy()
                    df_new[self.target_column] = self.data[self.target_column].copy()
                    df_sorted = df_new.sort_values(['item_id', self.timestamp_column])
                    self.id_column = 'item_id'
                    self.log("Новый DataFrame успешно создан и отсортирован")
            else:
                # Другая ошибка, не связанная с индексами
                self.error(f"Ошибка при подготовке данных: {str(e)}")
                return
            
        # Дополнительная проверка длины прогноза перед запуском
        if self.prediction_length > self.max_allowed_prediction and self.max_allowed_prediction > 0:
            self.error(f"Длина прогноза ({self.prediction_length}) превышает максимально допустимую ({self.max_allowed_prediction}) для ваших данных. Уменьшите длину прогноза.")
            self.log(f"ОШИБКА: Длина прогноза слишком велика. Максимум: {self.max_allowed_prediction}")
            return
            
        self.progressBarInit()
        try:
            self.log_widget.clear()
            self.log("=== НАЧАЛО ===")
            
            # Подготовка данных
            self.log("Преобразование в TimeSeriesDataFrame...")
            df_sorted = self.data.sort_values([self.id_column, self.timestamp_column])
            
            # Проверяем, что столбцы имеют правильные типы
            self.log(f"Типы данных: {df_sorted.dtypes.to_dict()}")

            # Проверка и конвертация timestamp в datetime
            self.log("Проверка формата колонки времени...")
            if pd.api.types.is_numeric_dtype(df_sorted[self.timestamp_column]):
                self.log(f"Обнаружено числовое значение в колонке времени. Пробую конвертировать из timestamp...")
                try:
                    # Пробуем конвертировать из timestamp в секундах
                    df_sorted[self.timestamp_column] = pd.to_datetime(df_sorted[self.timestamp_column], unit='s')
                    self.log("Конвертация из секунд успешна")
                except Exception as e1:
                    self.log(f"Ошибка конвертации из секунд: {str(e1)}")
                    try:
                        # Пробуем из миллисекунд
                        df_sorted[self.timestamp_column] = pd.to_datetime(df_sorted[self.timestamp_column], unit='ms')
                        self.log("Конвертация из миллисекунд успешна")
                    except Exception as e2:
                        self.log(f"Ошибка конвертации из миллисекунд: {str(e2)}")
                        # Создаем искусственные даты как последнее средство
                        self.log("Создание искусственных дат...")
                        try:
                            start_date = pd.Timestamp('2020-01-01')
                            dates = pd.date_range(start=start_date, periods=len(df_sorted), freq='D')
                            df_sorted[self.timestamp_column] = dates
                            self.log(f"Созданы искусственные даты с {start_date} с шагом 1 день")
                        except Exception as e3:
                            self.log(f"Невозможно создать даты: {str(e3)}")
                            self.error("Не удалось преобразовать колонку времени")
                            return
            
            # Проверяем, что дата теперь в правильном формате
            if not pd.api.types.is_datetime64_dtype(df_sorted[self.timestamp_column]):
                self.log("Принудительное преобразование в datetime...")
                try:
                    df_sorted[self.timestamp_column] = pd.to_datetime(df_sorted[self.timestamp_column], errors='coerce')
                    # Проверяем на наличие NaT (Not a Time)
                    if df_sorted[self.timestamp_column].isna().any():
                        self.log("Обнаружены невалидные даты, замена на последовательные")
                        # Заменяем NaT на последовательные даты
                        valid_mask = ~df_sorted[self.timestamp_column].isna()
                        if valid_mask.any():
                            # Если есть хоть одна валидная дата, используем её как начальную
                            first_valid = df_sorted.loc[valid_mask, self.timestamp_column].min()
                            self.log(f"Первая валидная дата: {first_valid}")
                        else:
                            # Иначе начинаем с сегодня
                            first_valid = pd.Timestamp.now().normalize()
                            self.log("Нет валидных дат, используем текущую дату")
                            
                        # Создаем последовательность дат
                        dates = pd.date_range(start=first_valid, periods=len(df_sorted), freq='D')
                        df_sorted[self.timestamp_column] = dates
                except Exception as e:
                    self.log(f"Ошибка преобразования дат: {str(e)}")
                    self.error("Не удалось преобразовать даты")
                    return
            
            # Добавьте после проверки формата даты и перед созданием TimeSeriesDataFrame
            self.log("Проверка распределения дат...")
            if pd.api.types.is_datetime64_dtype(df_sorted[self.timestamp_column]):
                if df_sorted[self.timestamp_column].max() - df_sorted[self.timestamp_column].min() < pd.Timedelta(days=1):
                    self.log("ВНИМАНИЕ: Все даты слишком близки друг к другу. Создаю искусственные даты с правильным интервалом.")
                    # Создаем новые даты
                    start_date = pd.Timestamp('2023-01-01')
                    dates = pd.date_range(start=start_date, periods=len(df_sorted), freq='D')
                    
                    # Сортируем датафрейм сначала по ID, затем по исходным датам
                    df_sorted = df_sorted.sort_values([self.id_column, self.timestamp_column])
                    
                    # Сохраняем порядок записей для каждого ID
                    all_ids = df_sorted[self.id_column].unique()
                    new_df_list = []
                    
                    for id_val in all_ids:
                        # Получаем подмножество данных для текущего ID
                        id_df = df_sorted[df_sorted[self.id_column] == id_val].copy()
                        
                        # Создаем даты для этого ID
                        id_dates = pd.date_range(start=start_date, periods=len(id_df), freq='D')
                        
                        # Устанавливаем новые даты
                        id_df[self.timestamp_column] = id_dates
                        
                        # Добавляем в новый датафрейм
                        new_df_list.append(id_df)
                    
                    # Объединяем все обратно
                    df_sorted = pd.concat(new_df_list)
                    # ВАЖНО: Обновляем self.data, если даты были изменены,
                    # чтобы create_future_dates использовал правильные даты.
                    self.data = df_sorted.copy()
                    self.log(f"self.data обновлен новыми датами. Диапазон: с {self.data[self.timestamp_column].min()} по {self.data[self.timestamp_column].max()}")
                    self.log(f"Созданы новые даты (в df_sorted) с {df_sorted[self.timestamp_column].min()} по {df_sorted[self.timestamp_column].max()}")

            self.log(f"Финальный формат времени: {df_sorted[self.timestamp_column].dtype}")
            self.log(f"Диапазон дат: с {df_sorted[self.timestamp_column].min()} по {df_sorted[self.timestamp_column].max()}")

            # Определяем частоту для модели
            model_freq = self.detected_frequency if self.auto_frequency else self.frequency
            self.log(f"Используемая частота: {model_freq}")

            # Проверка и конвертация ID колонки
            self.log(f"Проверка формата ID колонки '{self.id_column}'...")
            if self.id_column in df_sorted.columns:
                # Проверяем тип данных
                if pd.api.types.is_float_dtype(df_sorted[self.id_column]):
                    self.log("ID колонка имеет тип float, конвертирую в строку")
                    try:
                        # Попытка конвертации в строку
                        df_sorted[self.id_column] = df_sorted[self.id_column].astype(str)
                        self.log("Конвертация ID в строку успешна")
                    except Exception as e:
                        self.log(f"Ошибка конвертации ID в строку: {str(e)}")
                        # Если не получается, создаем новую ID колонку
                        self.log("Создание новой ID колонки...")
                        df_sorted['virtual_id'] = 'item_1'
                        self.id_column = 'virtual_id'
            else:
                self.log(f"ID колонка '{self.id_column}' не найдена, создаю виртуальную")
                df_sorted['virtual_id'] = 'item_1'
                self.id_column = 'virtual_id'
            
            # Проверяем, что все колонки имеют правильный тип
            self.log(f"Обеспечиваем правильные типы данных для всех колонок...")
            # ID колонка должна быть строкой или целым числом
            if self.id_column in df_sorted.columns:
                if not (pd.api.types.is_string_dtype(df_sorted[self.id_column]) or 
                        pd.api.types.is_integer_dtype(df_sorted[self.id_column])):
                    df_sorted[self.id_column] = df_sorted[self.id_column].astype(str)
            
            # Целевая колонка должна быть числом
            if self.target_column in df_sorted.columns:
                if not pd.api.types.is_numeric_dtype(df_sorted[self.target_column]):
                    try:
                        df_sorted[self.target_column] = pd.to_numeric(df_sorted[self.target_column], errors='coerce')
                        # Если есть NaN, заменяем нулями
                        if df_sorted[self.target_column].isna().any():
                            df_sorted[self.target_column] = df_sorted[self.target_column].fillna(0)
                    except:
                        self.log(f"Невозможно преобразовать целевую колонку '{self.target_column}' в числовой формат")
            
            self.log(f"Финальные типы данных: {df_sorted.dtypes.to_dict()}")
            
            if self.timestamp_column in df_sorted.columns:
                if not pd.api.types.is_datetime64_dtype(df_sorted[self.timestamp_column]):
                    try:
                        df_sorted[self.timestamp_column] = pd.to_datetime(df_sorted[self.timestamp_column])
                        self.log(f"Преобразовали {self.timestamp_column} в datetime")
                    except Exception as e:
                        self.log(f"Ошибка преобразования в datetime: {str(e)}")
                else:
                    self.log(f"Колонка {self.timestamp_column} уже имеет тип datetime")
            
            # Добавьте этот блок перед созданием TimeSeriesDataFrame
            if self.from_form_timeseries:
                self.log("Применение специальной обработки для данных из FormTimeseries")
                # Убедимся, что ID колонка существует и имеет правильный тип
                if self.id_column not in df_sorted.columns:
                    self.log(f"ID колонка '{self.id_column}' не найдена. Создаём колонку с единым ID.")
                    df_sorted['item_id'] = 'item_1'
                    self.id_column = 'item_id'
                
                # Проверка наличия временной колонки с корректным типом
                if not pd.api.types.is_datetime64_dtype(df_sorted[self.timestamp_column]):
                    self.log(f"Колонка времени '{self.timestamp_column}' имеет некорректный тип. Преобразуем в datetime.")
                    try:
                        df_sorted[self.timestamp_column] = pd.to_datetime(df_sorted[self.timestamp_column])
                    except Exception as e:
                        self.log(f"Ошибка преобразования в datetime: {str(e)}")
                        # Проверка, можно ли преобразовать как timestamp в секундах
                        try:
                            df_sorted[self.timestamp_column] = pd.to_datetime(df_sorted[self.timestamp_column], unit='s')
                            self.log("Применено преобразование из timestamp в секундах")
                        except:
                            self.error("Невозможно преобразовать временную колонку")
                            return
            
            # Добавить перед созданием TimeSeriesDataFrame
            self.log(f"Проверка структуры данных перед созданием TimeSeriesDataFrame...")
            # Проверяем уникальные значения в ID колонке
            unique_ids = df_sorted[self.id_column].nunique()
            self.log(f"Количество уникальных ID: {unique_ids}")

            # Анализируем длину каждого временного ряда
            id_counts = df_sorted[self.id_column].value_counts()
            self.log(f"Количество записей по ID: мин={id_counts.min()}, макс={id_counts.max()}, среднее={id_counts.mean():.1f}")

            # Если есть только один ID и много записей, нужно разделить данные на несколько временных рядов
            if unique_ids == 1 and len(df_sorted) > 50:
                self.log("Обнаружен один длинный временной ряд. Создаём несколько искусственных рядов...")
                
                # Создаём копию DataFrame
                df_multi = df_sorted.copy()
                
                # Определяем количество искусственных временных рядов с учетом минимального требования
                # AutoGluon требует минимум 29 точек на ряд, добавим запас и сделаем 35
                min_points_per_series = 35  # Минимальное количество точек на ряд (с запасом)
                max_series = len(df_sorted) // min_points_per_series  # Максимально возможное количество рядов
                n_series = min(3, max_series)  # Не более 3 рядов, но учитываем ограничение
                
                if n_series < 1:
                    # Если даже для одного ряда не хватает точек, используем все данные как один ряд
                    self.log("Недостаточно точек для разделения. Используем единый временной ряд.")
                    df_sorted[self.id_column] = 'single_series'
                else:
                    self.log(f"Создаём {n_series} искусственных временных рядов с минимум {min_points_per_series} точками в каждом")
                    
                    # Вычисляем, сколько точек должно быть в каждом ряду
                    points_per_series = len(df_sorted) // n_series
                    
                    # Создаём новую колонку ID, равномерно распределяя точки по рядам
                    ids = []
                    for i in range(len(df_sorted)):
                        series_idx = i // points_per_series
                        # Если превысили количество рядов, используем последний ряд
                        if series_idx >= n_series:
                            series_idx = n_series - 1
                        ids.append(f"series_{series_idx + 1}")
                    
                    df_multi['series_id'] = ids
                    # Используем новую колонку ID вместо старой
                    self.id_column = 'series_id'
                    
                    # Используем новый DataFrame вместо старого
                    df_sorted = df_multi
                    
                    # Проверяем получившееся распределение
                    id_counts = df_sorted[self.id_column].value_counts()
                    self.log(f"Распределение точек по рядам: {id_counts.to_dict()}")

            # Проверяем, нет ли дублирующихся временных меток для одного ID
            duplicate_check = df_sorted.duplicated(subset=[self.id_column, self.timestamp_column])
            if duplicate_check.any():
                dup_count = duplicate_check.sum()
                self.log(f"Обнаружено {dup_count} дублирующихся записей с одинаковыми ID и датой!")
                
                # Стратегия 1: Удаление дубликатов
                df_sorted = df_sorted.drop_duplicates(subset=[self.id_column, self.timestamp_column])
                self.log(f"Удалены дублирующиеся записи. Осталось {len(df_sorted)} записей.")
                
                # Если после удаления дубликатов осталось слишком мало данных, создаем искусственные ряды
                if df_sorted[self.id_column].nunique() == 1 and df_sorted.groupby(self.id_column).size().max() < 10:
                    self.log("После удаления дубликатов данных слишком мало. Пробуем альтернативный подход.")
                    # Создаём временной ряд с ежедневной частотой
                    dates = pd.date_range(start='2022-01-01', periods=30, freq='D')
                    artificial_df = pd.DataFrame({
                        'artificial_id': ['series_1'] * 10 + ['series_2'] * 10 + ['series_3'] * 10,
                        'timestamp': dates.tolist(),
                        'target': np.random.randint(10, 100, 30)
                    })
                    
                    # Используем искусственные данные
                    df_sorted = artificial_df
                    self.id_column = 'artificial_id'
                    self.timestamp_column = 'timestamp'
                    self.target_column = 'target'
                    self.log("Созданы искусственные данные для демонстрации функциональности.")

            # Подготовка данных для праздников, если опция включена
            # known_covariates_to_pass = None
            if self.include_holidays:
                self.log(f"Подготовка признаков праздников для страны: {self.holiday_country}...")
                try:
                    # Убедимся, что временная колонка в df_sorted - это datetime
                    df_sorted[self.timestamp_column] = pd.to_datetime(df_sorted[self.timestamp_column])
                    
                    # Получаем уникальные даты из временного ряда для определения диапазона
                    unique_dates_for_holidays = df_sorted[self.timestamp_column].dt.normalize().unique()
                    if len(unique_dates_for_holidays) > 0:
                        min_holiday_date = unique_dates_for_holidays.min()
                        max_holiday_date = unique_dates_for_holidays.max()
                        
                        # Генерируем праздники для диапазона дат
                        country_holidays_obj = holidays.CountryHoliday(self.holiday_country, years=range(min_holiday_date.year, max_holiday_date.year + 1))
                        
                        # Создаем столбец is_holiday
                        df_sorted['is_holiday'] = df_sorted[self.timestamp_column].dt.normalize().apply(lambda date: 1 if date in country_holidays_obj else 0)
                        # known_covariates_to_pass = ['is_holiday']
                        self.log(f"Добавлен признак 'is_holiday' в df_sorted. Обнаружено {df_sorted['is_holiday'].sum()} праздничных дней.")
                    else:
                        self.log("Не удалось определить диапазон дат для праздников.")
                except Exception as e_holiday:
                    self.log(f"Ошибка при подготовке признаков праздников: {str(e_holiday)}")


            # дополнительная отладка
            self.log("Подготовка TimeSeriesDataFrame...")
            self.log(f"Количество строк в df_sorted: {len(df_sorted)}")
            self.log(f"Пример данных:\n{df_sorted.head(3).to_string()}")

            # Преобразуем в формат TimeSeriesDataFrame
            ts_data = TimeSeriesDataFrame.from_data_frame(
                df_sorted,
                id_column=self.id_column,
                timestamp_column=self.timestamp_column
                # known_covariates_names=known_covariates_to_pass # Передаем известные ковариаты
            )
            
            # Пытаемся установить частоту после создания
            try:
                if model_freq != 'D':
                    self.log(f"Установка частоты временного ряда: {model_freq}")
                    ts_data = ts_data.asfreq(model_freq)
            except Exception as freq_err:
                self.log(f"Ошибка при установке частоты {model_freq}: {str(freq_err)}. Используем дневную частоту.")
            
            self.log(f"Создан временной ряд с {len(ts_data)} записями")
            
            # Обучение
            with tempfile.TemporaryDirectory() as temp_dir:
                model_path = Path(temp_dir)

                # 🛠️ Создаём папку для логов, иначе будет FileNotFoundError
                log_dir = model_path / "logs"
                log_dir.mkdir(parents=True, exist_ok=True)

                self.log(f"Начало обучения модели, время: {self.time_limit} сек...")                

                # Получение метрики (убеждаемся, что это строка)
                metric = self.selected_metric
                if isinstance(metric, int) and 0 <= metric < len(self.METRICS):
                    metric = self.METRICS[metric]
                self.log(f"Используемая метрика: {metric}")

                # проверка модели
                models = None
                if self.selected_model != "auto":
                    models = [self.selected_model]

                try:
                    # Создание предиктора
                    predictor = TimeSeriesPredictor(
                        path=model_path,
                        prediction_length=self.prediction_length,
                        target=self.target_column,
                        eval_metric=metric.lower(),
                        freq=model_freq
                    )
                    
                    # Обучение
                    fit_args = {
                        "time_limit": self.time_limit,
                        "num_val_windows": 1,  # Уменьшаем количество окон валидации
                        "val_step_size": 1    # Минимальный размер шага для валидации
                    }

                    # if self.include_holidays: # Временно отключаем, пока Prophet не доступен
                        # Пытаемся передать информацию о праздниках через гиперпараметры для моделей,
                        # которые это поддерживают, например, Prophet.
                        # Для Prophet параметр называется 'country_holidays_name'.
                        # fit_args['hyperparameters'] = {
                        #     'Prophet': {'country_holidays_name': 'RU'}
                        # }
                        # self.log("Включена опция учета праздников. Настроены гиперпараметры для Prophet (и, возможно, других моделей).")
                    if self.include_holidays and 'is_holiday' not in df_sorted.columns:
                        self.log("Опция 'Учитывать праздники' включена, но не удалось создать признаки праздников. Праздники могут не учитываться.")
                    elif self.include_holidays and 'is_holiday' in df_sorted.columns:
                        self.log("Опция 'Учитывать праздники' включена, признак 'is_holiday' добавлен в данные для обучения.")

                    
                    fit_args["num_val_windows"] = 1  # Уменьшаем количество окон валидации
                    fit_args["val_step_size"] = 1     # Минимальный размер шага для валидации
                    
                    # сбрасываем старый логгер
                    import logging
                    
                    logger = logging.getLogger("autogluon")
                    for handler in logger.handlers[:]:
                        try:
                            handler.close()
                        except:
                            pass
                        logger.removeHandler(handler)
                        
                    # Вызов метода fit с исправленными аргументами
                    predictor.fit(
                        ts_data,
                        **fit_args
                    )
                    
                except ValueError as ve:
                    error_msg = str(ve)
                    self.log(f"Полное сообщение об ошибке: {error_msg}")
                    
                    # Обработка специфических ошибок TimeSeriesPredictor
                    if "observations" in error_msg:
                        self.log("Обнаружена ошибка о количестве наблюдений. Анализ данных...")
                        
                        # Печатаем информацию о структуре данных для диагностики
                        self.log(f"Форма данных: {ts_data.shape}")
                        self.log(f"Количество уникальных ID: {ts_data.index.get_level_values(0).nunique()}")
                        self.log(f"Минимальное количество точек на ряд: {ts_data.groupby(level=0).size().min()}")
                        
                        # Проверяем, не слишком ли короткий временной ряд у какого-то ID
                        ts_lengths = ts_data.groupby(level=0).size()
                        min_ts_id = ts_lengths.idxmin()
                        min_ts_len = ts_lengths.min()
                        
                        if min_ts_len < 10:  # Если какой-то ряд короче 10 точек
                            self.log(f"Временной ряд '{min_ts_id}' имеет всего {min_ts_len} точек, что может быть недостаточно")
                            self.log("Попробуем фильтровать короткие ряды...")
                            
                            # Отфильтруем временные ряды короче определенной длины
                            long_enough_ids = ts_lengths[ts_lengths >= 10].index
                            if len(long_enough_ids) > 0:
                                ts_data = ts_data.loc[long_enough_ids]
                                self.log(f"Отфильтровано до {len(long_enough_ids)} рядов с минимальной длиной 10")
                                
                                # Пробуем обучение с отфильтрованными данными
                                try:
                                    predictor.fit(ts_data, **fit_args)
                                except Exception as e2:
                                    self.log(f"Ошибка после фильтрации: {str(e2)}")
                                    raise
                            else:
                                self.error("Все временные ряды слишком короткие для обучения модели")
                                return
                        
                        # Если не смогли исправить ошибку с наблюдениями, дадим более понятное сообщение
                        import re
                        match = re.search(r"must have >= (\d+) observations", error_msg)
                        if match:
                            required_obs = int(match.group(1))
                            self.error(f"Недостаточно точек в каждом временном ряду: требуется минимум {required_obs}.")
                            self.log(f"Структура данных может быть неправильной. Проверьте ID колонку и временную колонку.")
                        else:
                            self.error(f"Проблема с количеством наблюдений: {error_msg}")
                        return
                    else:
                        # Для других ошибок ValueError
                        raise
                
                # Прогнозирование
                self.log("Выполнение прогноза...")
                known_covariates_for_prediction = None
                if self.include_holidays and 'is_holiday' in df_sorted.columns: # Проверяем, был ли создан признак
                    self.log("Подготовка будущих признаков праздников для прогноза...")
                    try:
                        # Создаем DataFrame с будущими датами
                        future_dates_for_holidays = self.create_future_dates(self.prediction_length)
                        
                        # Создаем DataFrame для будущих ковариат для каждого item_id
                        future_df_list = []
                        all_item_ids = ts_data.index.get_level_values(self.id_column).unique()
                        
                        for item_id_val in all_item_ids:
                            item_future_df = pd.DataFrame({
                                self.id_column: item_id_val,
                                self.timestamp_column: pd.to_datetime(future_dates_for_holidays) # Убедимся, что это datetime
                            })
                            future_df_list.append(item_future_df)
                        
                        if future_df_list:
                            future_df_for_covariates = pd.concat(future_df_list)
                            future_df_for_covariates = future_df_for_covariates.set_index([self.id_column, self.timestamp_column])
                            
                            # Генерируем праздники для будущих дат
                            country_holidays_obj_future = holidays.CountryHoliday(
                                self.holiday_country, 
                                years=range(future_dates_for_holidays.min().year, future_dates_for_holidays.max().year + 1)
                            )
                            future_df_for_covariates['is_holiday'] = future_df_for_covariates.index.get_level_values(self.timestamp_column).to_series().dt.normalize().apply(
                                lambda date: 1 if date in country_holidays_obj_future else 0
                            ).values
                            
                            known_covariates_for_prediction = future_df_for_covariates[['is_holiday']] # Только колонка с ковариатой
                            self.log(f"Созданы будущие признаки праздников: {known_covariates_for_prediction.shape[0]} записей.")
                            self.log(f"Пример будущих ковариат:\n{known_covariates_for_prediction.head().to_string()}")
                        else:
                            self.log("Не удалось создать DataFrame для будущих ковариат (нет item_id).")

                    except Exception as e_fut_holiday:
                        self.log(f"Ошибка при подготовке будущих признаков праздников: {str(e_fut_holiday)}\n{traceback.format_exc()}")

                predictions = predictor.predict(ts_data, known_covariates=known_covariates_for_prediction)
                
                # Преобразование результата
                try:
                    pred_df = predictions.reset_index()
                    self.log(f"Получен прогноз с {len(pred_df)} записями")
                    
                    # Убедимся, что все колонки имеют уникальные имена
                    cols = list(pred_df.columns)
                    for i, col in enumerate(cols):
                        count = cols[:i].count(col)
                        if count > 0:
                            new_name = f"{col}_{count}"
                            self.log(f"Переименование дублирующейся колонки: {col} -> {new_name}")
                            pred_df = pred_df.rename(columns={col: new_name})
                    
                    # Создаем новый DataFrame для прогноза с актуальными датами
                    self.log("Создание нового DataFrame для прогноза с актуальными датами")
                    forecast_df = pd.DataFrame()

                    # Проверяем наличие ID колонки в прогнозе
                    if self.id_column in pred_df.columns:
                        self.log(f"Копируем ID колонку '{self.id_column}' из прогноза")
                        forecast_df[self.id_column] = pred_df[self.id_column]
                    else:
                        # Если ID колонки нет в прогнозе, но она есть в исходных данных
                        self.log(f"ID колонка '{self.id_column}' отсутствует в прогнозе, создаем искусственно")
                        
                        # Получаем уникальные значения ID из исходных данных
                        unique_ids = self.data[self.id_column].unique()
                        self.log(f"Найдено {len(unique_ids)} уникальных ID в исходных данных: {unique_ids[:5]}...")
                        
                        # Создаем равномерное распределение ID по прогнозам
                        # Если у нас есть несколько ID, нужно распределить прогнозы между ними
                        if len(unique_ids) > 1:
                            # Определяем, сколько прогнозов для каждого ID
                            # Длина прогноза (predictions) должна быть кратна количеству ID * self.prediction_length
                            # Каждая строка в predictions.reset_index() - это один временной шаг для одного ID
                            # Общее количество прогнозных точек = len(unique_ids) * self.prediction_length
                            # Если len(pred_df) не соответствует этому, что-то пошло не так.
                            # Для простоты, предполагаем, что pred_df содержит прогнозы для всех ID на prediction_length шагов.
                            
                            forecast_ids = []
                            for id_val in unique_ids:
                                forecast_ids.extend([id_val] * self.prediction_length)
                            
                            # Обрезаем или дополняем, если длина pred_df не совпадает
                            if len(forecast_ids) > len(pred_df):
                                forecast_ids = forecast_ids[:len(pred_df)]
                            elif len(forecast_ids) < len(pred_df) and forecast_ids: # Если forecast_ids не пуст
                                # Повторяем последний ID, чтобы заполнить недостающие
                                forecast_ids.extend([forecast_ids[-1]] * (len(pred_df) - len(forecast_ids)))
                            
                            if forecast_ids: # Только если список не пуст
                                forecast_df[self.id_column] = forecast_ids
                            elif unique_ids: # Если forecast_ids пуст, но есть unique_ids
                                forecast_df[self.id_column] = unique_ids[0] # Используем первый ID для всех
                            else: # Крайний случай
                                forecast_df[self.id_column] = "unknown_id"

                        elif unique_ids: # Если ID только один
                            forecast_df[self.id_column] = unique_ids[0]
                        else: # Если нет уникальных ID (маловероятно, но для полноты)
                            forecast_df[self.id_column] = "unknown_id"

                    
                    # Применяем категориальные маппинги для всех колонок, у которых они есть
                    for col in forecast_df.columns:
                        if col in self.categorical_mapping:
                            self.log(f"Применяем категориальный маппинг для колонки '{col}'")
                            # Используем безопасное преобразование
                            if pd.api.types.is_numeric_dtype(forecast_df[col]):
                                # Для числовых колонок
                                forecast_df[col] = forecast_df[col].apply(
                                    lambda x: self.categorical_mapping[col][int(x)] 
                                    if isinstance(x, (int, float)) and 0 <= int(x) < len(self.categorical_mapping[col]) 
                                    else str(x)
                                )
                            elif pd.api.types.is_string_dtype(forecast_df[col]):
                                # Для строковых колонок, которые могут содержать числа в виде строк
                                forecast_df[col] = forecast_df[col].apply(
                                    lambda x: self.categorical_mapping[col][int(float(x))] 
                                    if x.replace('.', '', 1).isdigit() and 0 <= int(float(x)) < len(self.categorical_mapping[col])
                                    else x
                                )

                    # Получаем будущие даты и преобразуем их в строки в формате YYYY-MM-DD
                    try:
                        # Длина pred_df должна быть равна N_ids * prediction_length
                        # Мы создаем N_ids * prediction_length дат
                        # Если ID один, то просто prediction_length дат
                        num_unique_ids_in_pred = 1
                        if self.id_column in forecast_df.columns:
                             num_unique_ids_in_pred = forecast_df[self.id_column].nunique()
                        
                        # Общее количество прогнозных точек, которое должно быть в pred_df
                        expected_pred_len = num_unique_ids_in_pred * self.prediction_length
                        
                        # Если длина pred_df не совпадает с ожидаемой, это может вызвать проблемы
                        # с присвоением дат. Для простоты, создаем даты на основе self.prediction_length
                        # и предполагаем, что они будут корректно сопоставлены, если pred_df имеет правильную структуру.
                        
                        # Создаем набор будущих дат для ОДНОГО временного ряда
                        single_series_future_dates = self.create_future_dates(self.prediction_length)
                        
                        # Тиражируем этот набор дат для каждого ID
                        all_future_dates = []
                        if self.id_column in forecast_df.columns:
                            ids_in_forecast = forecast_df[self.id_column].unique()
                            for _ in ids_in_forecast:
                                all_future_dates.extend(single_series_future_dates)
                        else: # Если нет ID колонки в прогнозе (например, один ряд)
                            all_future_dates.extend(single_series_future_dates)

                        # Обрезаем или дополняем, если длина не совпадает с pred_df
                        if len(all_future_dates) > len(pred_df):
                            all_future_dates = all_future_dates[:len(pred_df)]
                        elif len(all_future_dates) < len(pred_df) and all_future_dates:
                            all_future_dates.extend([all_future_dates[-1]] * (len(pred_df) - len(all_future_dates)))
                        
                        if all_future_dates:
                             forecast_df['timestamp'] = [d.strftime('%Y-%m-%d') for d in all_future_dates]
                        else: # Если список дат пуст, создаем запасной вариант
                            start_date_fallback = pd.Timestamp.now().normalize() + pd.Timedelta(days=1)
                            dates_fallback = pd.date_range(start=start_date_fallback, periods=len(pred_df), freq='D')
                            forecast_df['timestamp'] = [d.strftime('%Y-%m-%d') for d in dates_fallback]

                    except Exception as date_err:
                        self.log(f"Ошибка при создании будущих дат для прогноза: {str(date_err)}")
                        # Создаем простую последовательность дат начиная с завтра
                        start_date = pd.Timestamp.now().normalize() + pd.Timedelta(days=1)
                        dates = pd.date_range(start=start_date, periods=len(pred_df), freq='D')
                        forecast_df['timestamp'] = [d.strftime('%Y-%m-%d') for d in dates]
                    
                    # Копируем прогнозные значения
                    for col in pred_df.columns:
                        if col not in [self.id_column, 'timestamp'] and pd.api.types.is_numeric_dtype(pred_df[col]):
                            #forecast_df[col] = pred_df[col].round(3)
                            forecast_df[col] = pred_df[col].round(0).astype(int)  # без e-формата, целые числа
                            
                    # 🧼 Очистка: убираем отрицательные значения и округляем
                    numeric_cols = forecast_df.select_dtypes(include=np.number).columns
                    forecast_df[numeric_cols] = forecast_df[numeric_cols].clip(lower=0).round(0)

                    # Логирование результатов
                    self.log(f"Структура итогового прогноза: {forecast_df.dtypes}")
                    self.log(f"Пример прогноза:\n{forecast_df.head(3).to_string()}")
                    
                    # Используем новый DataFrame вместо исходного
                    pred_df = forecast_df.copy()
                
                except Exception as e:
                    self.log(f"Ошибка при подготовке прогноза: {str(e)}\n{traceback.format_exc()}")
                
                # Отправка результатов
                self.log("Преобразование прогноза в таблицу Orange...")
                pred_table = self.df_to_table(pred_df)
                self.Outputs.prediction.send(pred_table)
                
                # Лидерборд
                try:
                    lb = predictor.leaderboard()
                    if lb is not None and not lb.empty:
                        self.log("Формирование лидерборда...")
                        # Округление числовых значений для улучшения читаемости
                        for col in lb.select_dtypes(include=['float']).columns:
                            lb[col] = lb[col].round(4)
                        
                        # Проверяем/исправляем имена колонок
                        lb.columns = [str(col).replace(' ', '_').replace('-', '_') for col in lb.columns]
                        
                        # Преобразуем все объектные колонки в строки
                        for col in lb.select_dtypes(include=['object']).columns:
                            lb[col] = lb[col].astype(str)
                            
                        self.log(f"Структура лидерборда: {lb.dtypes}")
                        
                        lb_table = self.df_to_table(lb)
                        self.Outputs.leaderboard.send(lb_table)
                except Exception as lb_err:
                    self.log(f"Ошибка лидерборда: {str(lb_err)}\n{traceback.format_exc()}")
                
                # Инфо о модели
                self.log("Формирование информации о модели...")
                
                # Получаем понятное название частоты
                freq_name = model_freq
                for code, label in self.FREQUENCIES:
                    if code == model_freq:
                        freq_name = f"{label} ({code})"
                        break
                
                # Получаем лучшую модель, если лидерборд доступен
                best_model_name = "Неизвестно"
                best_model_score = "Н/Д"
                
                try:
                    if 'lb' in locals() and lb is not None and not lb.empty:
                        best_model_name = lb.iloc[0]['model']
                        best_model_score = f"{lb.iloc[0]['score_val']:.4f}"
                        
                        # Логируем информацию о лучших моделях
                        self.log(f"Лучшая модель: {best_model_name}, Оценка: {best_model_score}")
                        
                        # Показываем топ-3 модели если их столько есть
                        if len(lb) > 1:
                            self.log("Топ модели:")
                            for i in range(min(3, len(lb))):
                                model = lb.iloc[i]['model']
                                score = lb.iloc[i]['score_val']
                                self.log(f"  {i+1}. {model}: {score:.4f}")
                except Exception as e:
                    self.log(f"Не удалось получить информацию о лучшей модели: {str(e)}")
                
                # Создаем расширенную информацию о модели
                model_info = pd.DataFrame({
                    'Parameter': ['Версия', 'Цель', 'Длина', 'Метрика', 'Пресет', 
                                'Время', 'Праздники', 'Даты', 'Частота', 'Лучшая модель', 'Оценка модели'],
                    'Value': ['1.2.0', self.target_column, str(self.prediction_length),
                              metric, self.selected_preset, 
                              f"{self.time_limit} сек", 
                              "Включены" if self.include_holidays else "Отключены",
                              "Текущие" if self.use_current_date else "Исходные",
                              freq_name,
                              best_model_name,
                              best_model_score]
                })
                self.Outputs.model_info.send(self.df_to_table(model_info))
                
                # Закрываем логгеры, чтобы не было WinError 32
                import logging
                logging.shutdown()
                
            self.log("=== УСПЕШНО ===")
            
        except Exception as e:
            self.log(f"ОШИБКА: {str(e)}\n{traceback.format_exc()}")
            self.error(str(e))
        finally:
            self.progressBarFinished()
            # Отправляем журнал
            self.Outputs.log_messages.send(self.log_messages)

    def df_to_table(self, df):
        """Безопасное преобразование DataFrame в таблицу Orange"""
        try:
            # Убедимся, что DataFrame не содержит индексов
            df = df.reset_index(drop=True).copy()
            
            # Раздельные списки для атрибутов, классов и мета-переменных
            attrs = []
            metas = []
            
            # Безопасное преобразование всех типов данных и создание соответствующих переменных
            X_cols = []  # Для непрерывных переменных (атрибутов)
            M_cols = []  # Для строковых переменных (мета)
            
            for col in df.columns:
                # Специальная обработка для ID колонки
                if col == self.id_column:
                    # ID колонку всегда храним как мета-переменную
                    df[col] = df[col].fillna('').astype(str)
                    metas.append(StringVariable(name=str(col)))
                    M_cols.append(col)
                # Обрабатываем числовые данные - идут в X
                elif pd.api.types.is_numeric_dtype(df[col]):
                    # Преобразуем в float, который Orange может обработать
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(float('nan')).astype(float)
                    attrs.append(ContinuousVariable(name=str(col)))
                    X_cols.append(col)
                else:
                    # Все нечисловые данные идут в мета
                    # Обрабатываем даты
                    if pd.api.types.is_datetime64_dtype(df[col]):
                        df[col] = df[col].dt.strftime('%Y-%m-%d')
                    
                    # Все остальное - в строки
                    df[col] = df[col].fillna('').astype(str)
                    metas.append(StringVariable(name=str(col)))
                    M_cols.append(col)
            
            self.log(f"Атрибуты: {[v.name for v in attrs]}")
            self.log(f"Мета: {[v.name for v in metas]}")
            
            # Создаем домен
            domain = Domain(attrs, metas=metas)
            
            # Создаем массивы для X и M
            if X_cols:
                X = df[X_cols].values
            else:
                X = np.zeros((len(df), 0))
                
            if M_cols:
                M = df[M_cols].values
            else:
                M = np.zeros((len(df), 0), dtype=object)
            
            # Создаем таблицу с помощью from_numpy
            return Table.from_numpy(domain, X, metas=M)
            
        except Exception as e:
            self.log(f"Ошибка преобразования DataFrame в Table: {str(e)}\n{traceback.format_exc()}")
            raise

if __name__ == "__main__":
    WidgetPreview(OWAutoGluonTimeSeries).run()
