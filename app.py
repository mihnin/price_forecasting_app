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
           *   **Что это:** Цена на один и тот же материал очень сильно колеблется между закупками без видимых рыночных причин.
           *   **Как измеряется:** Рассчитывается коэффициент вариации (CV). Высоким считается CV > 50% (цена в среднем отклоняется более чем на половину от средней цены).
           *   **Пример:** Цена на "Кабель силовой" вчера была 100 руб/метр, сегодня - 250 руб/метр, а через неделю - 80 руб/метр, при этом рыночных новостей о дефиците или резком подорожании меди не было. Это может указывать на манипуляции или ошибки.
        
        2. **Дробление закупок**
           *   **Что это:** Вместо одной крупной закупки проводится множество мелких, часто с небольшими интервалами времени. Цель может быть - обойти процедуру согласования или тендера, которая требуется для закупок свыше определенной суммы (порогового значения).
           *   **Как измеряется:** Анализируется частота закупок одного и того же материала на суммы, близкие к пороговым значениям (например, закупки на 49 900 руб при пороге в 50 000 руб).
           *   **Пример:** В течение недели закупается "Бумага А4" 5 раз по 45 000 руб, хотя можно было сделать одну закупку на 225 000 руб. Если порог для тендера - 50 000 руб, это подозрительно.
        
        3. **Активность в конце периодов**
           *   **Что это:** Непропорционально большое количество закупок или повышение цен происходит в последние дни отчетного периода (месяц, квартал, год).
           *   **Причина:** Может указывать на попытки срочно "освоить бюджет" или на спешку, ведущую к закупкам по завышенным ценам.
           *   **Пример:** 80% всех закупок "Принтеров" за квартал приходится на последние два дня марта. Или цена на "Услуги консалтинга" систематически повышается на 20% в декабре.
        
        4. **Аномальная стабильность цен**
           *   **Что это:** Цена на материал остается абсолютно одинаковой в течение длительного времени, даже если рыночные цены на аналогичные товары меняются. Также сюда относятся подозрительно "круглые" цены.
           *   **Причина:** Может указывать на сговор с поставщиком, фиктивные закупки или просто на отсутствие анализа рынка.
           *   **Пример:** Цена на "Металлические стеллажи" (товар с изменяющейся ценой металла) составляет ровно 10 000.00 руб за штуку на протяжении двух лет без изменений. Или цена всегда равна 5000.00, 15000.00 и т.д.
        
        5. **Нарушения сезонности**
           *   **Что это:** Закупка товаров происходит в периоды, когда спрос на них минимален или когда их производство/поставка обычно не осуществляется, либо динамика цен противоречит общим тенденциям.
           *   **Причина:** Может указывать на неэффективное планирование, закупку "про запас" по невыгодным ценам или на нестандартные схемы.
           *   **Пример:** Массовая закупка "Новогодних украшений" происходит в июне по высоким ценам. Или цена на "Кондиционеры" растет зимой, хотя обычно в это время она падает.
        
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
        # Проверяем, есть ли уже данные анализа волатильности
        if 'volatility_data' not in st.session_state:
            with st.spinner("Анализ волатильности..."):
                # Предполагаем, что эта функция сохраняет результат в st.session_state.volatility_data
                material_segmenter.analyze_volatility(st.session_state.processed_data)

        # Отображаем, если данные есть (были или только что рассчитаны)
        if 'volatility_data' in st.session_state:
            visualizer.plot_volatility(st.session_state.volatility_data)
        else:
            st.error("Не удалось выполнить или загрузить данные анализа волатильности.")
    else:
        st.warning("Сначала загрузите и обработайте данные")

elif page == "Стабильные материалы":
    if 'processed_data' in st.session_state:
        # Проверяем, есть ли уже данные анализа стабильности
        if 'stability_data' not in st.session_state:
            with st.spinner("Анализ стабильности материалов..."):
                 # Предполагаем, что эта функция сохраняет результат в st.session_state.stability_data
                material_segmenter.analyze_stability(st.session_state.processed_data)

        # Отображаем, если данные есть
        if 'stability_data' in st.session_state:
            visualizer.plot_stability(st.session_state.stability_data)
        else:
            st.error("Не удалось выполнить или загрузить данные анализа стабильности.")
    else:
        st.warning("Сначала загрузите и обработайте данные")

elif page == "Неактивные материалы":
    if 'processed_data' in st.session_state:
         # Проверяем, есть ли уже данные анализа неактивности
        if 'inactivity_data' not in st.session_state:
            with st.spinner("Анализ неактивных материалов..."):
                 # Предполагаем, что эта функция сохраняет результат в st.session_state.inactivity_data
                material_segmenter.analyze_inactivity(st.session_state.processed_data)

        # Отображаем, если данные есть
        if 'inactivity_data' in st.session_state:
            visualizer.plot_inactivity(st.session_state.inactivity_data)
        else:
             st.error("Не удалось выполнить или загрузить данные анализа неактивности.")
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

                # Очищаем состояние виджетов визуализации при новой сегментации
                keys_to_clear = ['vis_seg_details_select', 'vis_seg_page_size', 'vis_seg_page_number']
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                # Визуализацию вызываем ниже, после проверки наличия данных в сессии

        # Отображение результатов, если они есть в сессии
        if 'materials_segments' in st.session_state and 'segments_stats' in st.session_state:
             # Используем данные из session_state
             visualizer.plot_segmentation_results(
                 st.session_state.materials_segments,
                 st.session_state.segments_stats
             )
        # Сообщение, если сегментация еще не проводилась (но данные загружены)
        elif 'materials_segments' not in st.session_state:
             st.info("Задайте параметры и нажмите 'Выполнить сегментацию' для просмотра результатов.")

    else:
        st.warning("Сначала загрузите и обработайте данные")
elif page == "Анализ безопасности":
    if 'processed_data' in st.session_state and 'materials_segments' in st.session_state:

        # Кнопка для повторного запуска анализа
        if st.button("Повторить анализ"):
            if 'security_risks' in st.session_state:
                del st.session_state['security_risks']
            st.rerun()

        # Запускаем анализ ТОЛЬКО если результаты еще не сохранены в сессии
        if 'security_risks' not in st.session_state:
            with st.spinner("Анализ безопасности данных..."):
                st.session_state.security_risks = security_analyzer.analyze_security_risks(
                    st.session_state.processed_data,
                    st.session_state.materials_segments
                )

        # Отображаем результаты анализа, если они есть
        if 'security_risks' in st.session_state and st.session_state.security_risks is not None and not st.session_state.security_risks.empty:
            risk_df = st.session_state.security_risks
            security_analyzer.display_security_analysis_results(risk_df)

            st.divider()
            st.subheader("Детальный анализ материалов с высоким риском")

            high_risk_materials_df = risk_df[risk_df['Категория риска'] == 'Высокий']

            if not high_risk_materials_df.empty:
                high_risk_options = high_risk_materials_df['Материал'].tolist()
                
                selected_materials = st.multiselect(
                    "Выберите материалы для детального анализа:",
                    options=high_risk_options,
                    default=high_risk_options[:min(5, len(high_risk_options))] # По умолчанию выбираем первые 5 или меньше
                )

                if selected_materials:
                    # Генерируем данные для Excel
                    excel_data = security_analyzer.export_multiple_detailed_analysis(
                        st.session_state.processed_data, 
                        selected_materials
                    )
                    
                    if excel_data:
                        st.download_button(
                           label="Скачать детальный анализ для выбранных материалов (Excel)",
                           data=excel_data,
                           file_name="detailed_security_analysis_multiple.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                else:
                    st.info("Выберите хотя бы один материал для загрузки детального анализа.")
            else:
                st.info("Материалы с высоким риском не найдены.")

        elif 'security_risks' in st.session_state and st.session_state.security_risks is not None and st.session_state.security_risks.empty:
             st.info("Анализ безопасности завершен, но материалы с признаками риска не обнаружены.")
        else:
             st.info("Результаты анализа безопасности отсутствуют или не были сгенерированы.")

    elif 'processed_data' not in st.session_state:
        st.warning("Сначала загрузите и обработайте данные")
    else:
        st.warning("Сначала выполните сегментацию материалов в разделе 'Сегментация для прогнозирования'")
        
        if st.button("Перейти к сегментации"):
            st.session_state.page = "Сегментация для прогнозирования"
            st.rerun()
    
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
            st.rerun()

# Footer
st.divider()

# Отображение информации о производительности
show_performance_info()

# Отображение информации о версии
show_app_version()

st.caption("© 2025 Анализ и прогнозирование цен материалов")