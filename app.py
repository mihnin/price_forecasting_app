import streamlit as st
import pandas as pd
import os
import sys

# Увеличиваем лимит элементов для отображения в Pandas Styler
pd.set_option("styler.render.max_elements", 1000000)  # Устанавливаем лимит в 1 миллион элементов

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем модули
from modules.data_loader import DataLoader
from modules.data_processor import DataProcessor
from modules.data_analyzer import DataAnalyzer
from modules.visualization import Visualizer
from modules.material_segmentation import MaterialSegmenter
from modules.forecasting_preparation import ForecastPreparation
from modules.security_analyzer import SecurityAnalyzer
from modules.utils import apply_custom_css, show_user_guide, show_performance_info, show_app_version

# Настройка страницы
st.set_page_config(
    page_title="Анализ и прогнозирование цен материалов",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Применяем пользовательский CSS
apply_custom_css()

# Создаем объекты модулей
data_loader = DataLoader()
data_processor = DataProcessor()
data_analyzer = DataAnalyzer()
visualizer = Visualizer()
material_segmenter = MaterialSegmenter()
forecast_preparation = ForecastPreparation()
security_analyzer = SecurityAnalyzer()

# Боковая панель
with st.sidebar:
    st.header("Навигация")
    page = st.radio(
        "Выберите раздел:",
        ["Информация", "Загрузка данных", "Общий анализ", "Анализ уникальности материалов", 
         "Временной анализ", "Анализ волатильности", "Стабильные материалы", 
         "Неактивные материалы", "Сегментация для прогнозирования", "Анализ безопасности", "Экспорт данных"]
    )
    
    st.divider()
    st.header("Статус")
    
    # Проверка наличия данных в сессии
    if 'data' in st.session_state:
        st.success(f"Данные загружены: {st.session_state.data.shape[0]} строк")
        if 'processed_data' in st.session_state:
            st.success("Данные обработаны")
        if 'materials_segments' in st.session_state:
            st.success("Материалы сегментированы")
            
            # Отображение статистики по сегментам
            segments_stats = st.session_state.get('segments_stats', {})
            if segments_stats:
                st.write("Распределение материалов:")
                for segment, count in segments_stats.items():
                    st.write(f"- {segment}: {count}")
    else:
        st.warning("Данные не загружены")

# Заголовок приложения
st.title("Анализ и прогнозирование цен материалов")

# Функция для отображения информации
def display_info():
    st.info("""
    Это приложение предназначено для анализа данных о материалах и их ценах, 
    а также для подготовки к прогнозированию цен с помощью различных методов машинного обучения.
    
    Загрузите CSV-файл с данными о материалах, и приложение выполнит анализ, 
    определит материалы, подходящие для прогнозирования, и подготовит данные для дальнейшего использования.
    """)
    
    # Добавляем руководство пользователя
    with st.expander("Руководство пользователя", expanded=False):
        show_user_guide()
        
    # Добавляем информацию для служб безопасности
    with st.expander("Информация для служб безопасности"):
        st.markdown("""
        ## Руководство для служб информационной безопасности
        
        Данное приложение включает специальный модуль для выявления подозрительных паттернов в данных, которые могут указывать на:
        - Потенциальные мошеннические схемы
        - Манипуляции с ценами
        - Дробление закупок для обхода процедур
        - Концентрацию активности в конце отчетных периодов
        - Нехарактерные изменения в закупочных процессах
        
        ### Ключевые индикаторы риска:
        
        1. **Высокая волатильность цен**
           - Материалы с коэффициентом вариации более 50%
           - Необъяснимые скачки цен между закупками
        
        2. **Дробление закупок**
           - Множество небольших закупок с короткими интервалами
           - Закупки на суммы ниже пороговых значений
        
        3. **Активность в конце периодов**
           - Концентрация закупок в конце месяца/квартала/года
           - Повышение цен в конце отчетных периодов
        
        4. **Аномальная стабильность цен**
           - Неестественно стабильные цены на волатильных рынках
           - Подозрительно округленные суммы
        
        5. **Нарушения сезонности**
           - Закупки в нехарактерные для товарной категории периоды
           - Противоречие общим рыночным тенденциям
        
        ### Как использовать модуль анализа безопасности:
        
        1. Загрузите и обработайте данные
        2. Выполните сегментацию материалов
        3. Перейдите в раздел "Анализ безопасности"
        4. Изучите материалы с высоким индексом подозрительности
        5. Выполните детальный анализ материалов из группы риска
        6. Экспортируйте отчет для дальнейшего расследования
        
        **Примечание:** Особое внимание следует уделить материалам из сегмента "Высокая волатильность", так как в этом сегменте наиболее часто обнаруживаются признаки потенциальных нарушений.
        """)

# Основное содержимое
if page == "Информация":
    display_info()

elif page == "Загрузка данных":
    data_loader.render()
    
    if 'data' in st.session_state:
        if st.button("Обработать данные"):
            with st.spinner("Обработка данных..."):
                st.session_state.processed_data = data_processor.process_data(st.session_state.data)
                st.success("Данные успешно обработаны!")
                
                # Показать образец обработанных данных
                st.subheader("Образец обработанных данных")
                st.dataframe(st.session_state.processed_data.head())

elif page == "Общий анализ":
    if 'processed_data' in st.session_state:
        data_analyzer.render_overview(st.session_state.processed_data)
    else:
        st.warning("Сначала загрузите и обработайте данные")

elif page == "Анализ уникальности материалов":
    if 'processed_data' in st.session_state:
        data_analyzer.render_materials_uniqueness(st.session_state.processed_data)
        visualizer.plot_materials_distribution(st.session_state.processed_data)
    else:
        st.warning("Сначала загрузите и обработайте данные")

elif page == "Временной анализ":
    if 'processed_data' in st.session_state:
        data_analyzer.render_time_analysis(st.session_state.processed_data)
        visualizer.plot_time_distribution(st.session_state.processed_data)
    else:
        st.warning("Сначала загрузите и обработайте данные")

elif page == "Анализ волатильности":
    if 'processed_data' in st.session_state:
        material_segmenter.analyze_volatility(st.session_state.processed_data)
        visualizer.plot_volatility(st.session_state.volatility_data)
    else:
        st.warning("Сначала загрузите и обработайте данные")

elif page == "Стабильные материалы":
    if 'processed_data' in st.session_state:
        material_segmenter.analyze_stability(st.session_state.processed_data)
        visualizer.plot_stability(st.session_state.stability_data)
    else:
        st.warning("Сначала загрузите и обработайте данные")

elif page == "Неактивные материалы":
    if 'processed_data' in st.session_state:
        material_segmenter.analyze_inactivity(st.session_state.processed_data)
        visualizer.plot_inactivity(st.session_state.inactivity_data)
    else:
        st.warning("Сначала загрузите и обработайте данные")

elif page == "Сегментация для прогнозирования":
    if 'processed_data' in st.session_state:
        st.header("Сегментация материалов для прогнозирования")
        
        # Параметры сегментации
        with st.expander("Параметры сегментации", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                min_data_points = st.slider("Минимальное количество точек данных", 5, 100, 24)
            
            with col2:
                max_volatility = st.slider("Максимальный коэффициент вариации (%)", 1, 100, 30)
            
            with col3:
                min_activity_days = st.slider("Минимальное количество дней активности", 30, 1000, 365)
        
        if st.button("Выполнить сегментацию"):
            with st.spinner("Сегментация материалов..."):
                segments, stats = forecast_preparation.segment_materials(
                    st.session_state.processed_data,
                    min_data_points=min_data_points,
                    max_volatility=max_volatility,
                    min_activity_days=min_activity_days
                )
                
                st.session_state.materials_segments = segments
                st.session_state.segments_stats = stats
                
                st.success("Сегментация завершена!")
                
                # Визуализация результатов сегментации
                visualizer.plot_segmentation_results(segments, stats)
    else:
        st.warning("Сначала загрузите и обработайте данные")
elif page == "Анализ безопасности":
    if 'processed_data' in st.session_state and 'materials_segments' in st.session_state:
        # Запускаем анализ ТОЛЬКО если результаты еще не сохранены в сессии
        if 'security_risks' not in st.session_state:
            with st.spinner("Анализ безопасности данных..."):
                st.session_state.security_risks = security_analyzer.analyze_security_risks(
                    st.session_state.processed_data, 
                    st.session_state.materials_segments
                )

        # Отображаем результаты анализа, если они есть
        if 'security_risks' in st.session_state and st.session_state.security_risks is not None:
            security_analyzer.display_security_analysis_results(st.session_state.security_risks)
        
            # Кнопка для детального анализа остается здесь, но использует сохраненные риски
            if not st.session_state.security_risks.empty and st.button("Показать детальный анализ для материала с высоким риском"):
                # Выбираем материал с наивысшим индексом подозрительности из СОХРАНЕННЫХ результатов
                high_risk_material = st.session_state.security_risks.iloc[0]['Материал']
                # Вызываем функцию детального анализа (она не создает кнопки скачивания, все в порядке)
                security_analyzer.highlight_suspicious_materials(st.session_state.processed_data, high_risk_material)
        else:
             st.info("Результаты анализа безопасности отсутствуют или не были сгенерированы.")

    elif 'processed_data' not in st.session_state:
        st.warning("Сначала загрузите и обработайте данные")
    else:
        st.warning("Сначала выполните сегментацию материалов в разделе 'Сегментация для прогнозирования'")
        
        if st.button("Перейти к сегментации"):
            st.session_state.page = "Сегментация для прогнозирования"
            st.experimental_rerun()
    
elif page == "Экспорт данных":
    if 'materials_segments' in st.session_state:
        st.header("Экспорт данных")
        
        st.markdown("""
        ## Экспорт данных для использования в других приложениях
        
        В этом разделе вы можете экспортировать данные различных сегментов материалов 
        в форматы CSV или Excel для дальнейшего использования в других приложениях.
        
        Доступные опции экспорта:
        - **Экспорт по сегментам** - экспорт данных отдельно для каждого сегмента
        - **Массовый экспорт** - экспорт всех сегментов в один ZIP-архив
        - **Настраиваемый экспорт** - экспорт с возможностью фильтрации по различным параметрам
        """)
        
        # Вызываем метод экспорта данных
        forecast_preparation.export_data_options(st.session_state.materials_segments)
    else:
        st.warning("Сначала выполните сегментацию материалов в разделе 'Сегментация для прогнозирования'")
        
        if st.button("Перейти к сегментации"):
            # Переключаемся на страницу сегментации
            st.session_state.page = "Сегментация для прогнозирования"
            st.experimental_rerun()

# Footer
st.divider()

# Отображение информации о производительности
show_performance_info()

# Отображение информации о версии
show_app_version()

st.caption("© 2025 Анализ и прогнозирование цен материалов")