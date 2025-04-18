# Приложение для анализа и прогнозирования цен материалов

## Что делает приложение

Данное приложение предназначено для комплексного анализа исторических данных о ценах материалов и подготовки их к прогнозированию. Оно обеспечивает полный цикл работы с данными:

1. **Загрузка и подготовка данных**:  
   Приложение принимает CSV-файлы с историей цен материалов, проводит их предварительную обработку, очистку и нормализацию.

2. **Исследовательский анализ данных**:  
   Визуализирует динамику цен, распределение материалов по различным параметрам, выявляет закономерности и тренды.

3. **Сегментация материалов**:  
   Разделяет материалы на группы в зависимости от характеристик ценовых рядов и их пригодности для различных методов прогнозирования.

4. **Выявление аномалий и рисков**:  
   Анализирует данные на предмет необычных паттернов, резких скачков цен и подозрительной активности.

5. **Подготовка к прогнозированию**:  
   Формирует наборы данных, которые можно использовать для построения прогнозных моделей.

6. **Экспорт результатов**:  
   Позволяет экспортировать обработанные данные, сегменты материалов и результаты анализа в различных форматах.

---

## Сегментация материалов

Приложение классифицирует материалы на шесть основных сегментов, исходя из характеристик их ценовых рядов. Эта сегментация помогает определить, какие методы прогнозирования подходят для каждого материала и выявить проблемные участки данных.

### 1. ML-прогнозирование (1 685 материалов)

**Что это:**  
Материалы, которые оптимально подходят для прогнозирования с использованием продвинутых методов машинного обучения (ML).

**Логика отбора:**
- Имеют достаточное количество исторических данных (не менее 24 записей).
- Показывают умеренную волатильность (коэффициент вариации не более 30%).
- Имеют исторические данные за достаточно длительный период (не менее 30 дней).
- Активно используются (были закупки в течение последнего года).

**Пример:**  
Материал "Подшипник 6305", для которого есть данные о 36 закупках за последние 2 года. Цена менялась в диапазоне от 450 до 550 рублей, что дает волатильность около 8%. Последняя закупка была 3 месяца назад.  
Этот материал идеально подходит для ML-прогнозирования, так как имеет достаточную историю, стабильные, но не слишком предсказуемые изменения цены, и актуальные данные.

---

### 2. Наивные методы (37 722 материала)

**Что это:**  
Материалы, для которых рекомендуется использовать более простые (наивные) методы прогнозирования.

**Логика отбора:**
- Имеют недостаточно данных для ML-методов (от 5 до 23 записей).  
  **ИЛИ**  
- Имеют высокую волатильность (более 30%), но при этом достаточное количество данных.
- Активно используются (были закупки в течение последнего года).

**Пример:**  
Материал "Клапан обратный DN50". Для него есть только 8 записей о закупках за последние 3 года, хотя цены относительно стабильны. Последняя закупка была 2 месяца назад.  
Для такого материала лучше использовать простые методы прогнозирования, такие как скользящее среднее или наивный прогноз (где прогноз = последнему значению), так как данных для сложных ML-алгоритмов недостаточно.

---

### 3. Постоянная цена (758 материалов)

**Что это:**  
Материалы, цена которых практически не меняется с течением времени.

**Логика отбора:**
- Коэффициент вариации цены менее 1%.
- Активно используются (были закупки в течение последнего года).

**Пример:**  
Материал "Бумага офисная А4" закупается по фиксированному долгосрочному контракту и имеет цену 280 рублей за пачку, которая не менялась в течение 18 месяцев, несмотря на 15 различных закупок.  
Для такого материала прогнозирование тривиально: будущая цена, скорее всего, останется той же самой до окончания действия контракта.

---

### 4. Неактивные (110 148 материалов)

**Что это:**  
Материалы, которые не закупались в течение длительного периода времени.

**Логика отбора:**
- Не было закупок в течение последнего года (более 365 дней с последней закупки).

**Пример:**  
Материал "Датчик давления ТМ-510" последний раз закупался 498 дней назад. Компания перешла на использование другой модели, и данный материал больше не используется.  
Такие материалы исключаются из прогнозирования, так как данные устарели и, скорее всего, не отражают текущую рыночную ситуацию.

---

### 5. Недостаточно истории (24 774 материала)

**Что это:**  
Материалы с очень малым количеством данных о закупках.

**Логика отбора:**
- Имеют менее 5 записей о закупках.
- При этом могут быть активными (закупки в течение последнего года).

**Пример:**  
Недавно введенный в ассортимент материал "Смазка специальная XZ-12" был закуплен всего 2 раза - 8 месяцев назад и 2 месяца назад. Цены составили 1200 и 1250 рублей соответственно.  
Для такого материала невозможно построить надежный прогноз, так как данных слишком мало для выявления каких-либо закономерностей.

---

### 6. Высокая волатильность

**Что это:**  
Материалы с крайне нестабильными ценами, резкими скачками и высокой изменчивостью.

**Логика отбора:**
- Коэффициент вариации цены более 30%.  
  **ИЛИ**  
- У них есть специфические аномальные паттерны в данных.  
- При этом материалы имеют менее 5 записей, что делает их непригодными даже для наивных методов.

---

## Дополнительная функциональность

### Анализ безопасности

Приложение включает специальный модуль для выявления потенциальных мошеннических схем и аномалий в данных о закупках. Он анализирует:
- Материалы с необъяснимо высокой волатильностью цен.
- Паттерны потенциального дробления закупок.
- Активность в конце отчетных периодов.
- Аномально стабильные цены на волатильных рынках.
- Нехарактерные сезонные закупки.

---

### Экспорт данных

Приложение позволяет экспортировать данные в различных форматах:
- По отдельным сегментам (Excel, CSV).
- Массовый экспорт всех сегментов (ZIP-архив).
- Настраиваемый экспорт по заданным критериям.

---

### Визуализация данных

Приложение предоставляет богатый набор визуализаций для анализа:
- Динамика цен во времени.
- Тепловые карты активности по месяцам и годам.
- Распределение интервалов между закупками.
- Гистограммы распределения цен.
- Графики с подсветкой аномальных значений.

---

## Практическое применение

### Для специалистов по закупкам:
- Определение оптимального времени для новых закупок.
- Планирование бюджета на основе прогнозов.
- Выявление материалов с нестабильными ценами.

### Для финансового планирования:
- Прогнозирование затрат на закупку материалов.
- Оценка волатильности затрат по категориям.
- Выявление возможностей для оптимизации расходов.

### Для служб информационной безопасности:
- Выявление подозрительных паттернов в закупках.
- Анализ потенциальных мошеннических схем.
- Мониторинг аномальной активности в конце отчетных периодов.

---

## Запуск через Docker

Для запуска приложения с использованием Docker выполните следующие шаги:

1.  **Установите Docker:**  
    Загрузите и установите Docker Desktop для вашей операционной системы:
    - **Windows:** [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
    - **macOS:** [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
    - **Linux:** Следуйте инструкциям для вашего дистрибутива на [официальном сайте Docker](https://docs.docker.com/engine/install/).

2.  **Клонируйте репозиторий:**
    ```bash
    git clone <URL репозитория>
    cd <папка репозитория>
    ```

3.  **Создайте Dockerfile:** (Если его еще нет в репозитории)  
    Создайте файл `Dockerfile` в корневой папке проекта со следующим содержимым (пример):
    ```dockerfile
    # Используем базовый образ Python
    FROM python:3.10-slim

    # Устанавливаем рабочую директорию
    WORKDIR /app

    # Копируем файлы зависимостей и устанавливаем их
    COPY requirements.txt requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt

    # Копируем остальные файлы приложения
    COPY . .

    # Указываем порт, который будет слушать Streamlit
    EXPOSE 8501

    # Команда для запуска приложения Streamlit
    CMD ["streamlit", "run", "app.py"] 
    ```
    *Примечание: Замените `app.py` на имя вашего основного скрипта Streamlit.*

4.  **Соберите Docker-образ:**
    В терминале, находясь в корневой папке проекта, выполните:
    ```bash
    docker build -t price-forecasting-app .
    ```

5.  **(Рекомендуется) Создайте том для хранения данных:**
    Чтобы данные (загруженные файлы, результаты) сохранялись между запусками контейнера, создайте Docker Volume:
    ```bash
    docker volume create app_data
    ```
    *Примечание: Управление размером тома зависит от конфигурации Docker и хост-системы.* 

6.  **Запустите контейнер:**
    Используйте следующую команду для запуска контейнера с выделением ресурсов и монтированием тома:
    ```bash
    docker run -d -p 8501:8501 --memory="16g" --cpus="14" --mount source=app_data,target=/app/data price-forecasting-app
    ```
    - `-d`: фоновый режим
    - `-p 8501:8501`: проброс порта
    - `--memory="16g"`: лимит RAM 16 ГБ
    - `--cpus="14"`: лимит CPU 14 ядер
    - `--mount source=app_data,target=/app/data`: подключение тома `app_data` к папке `/app/data` внутри контейнера (если ваше приложение использует другой путь для данных, измените `target`)
    - `price-forecasting-app`: имя созданного образа

7.  **Откройте приложение:**
    После запуска контейнера приложение будет доступно в вашем браузере по адресу `http://localhost:8501`.

---

## Системные требования

**Минимальные требования:**
- **Операционная система:** Windows, macOS, Linux
- **Docker:** Установлен и запущен

**Рекомендуемые требования для обработки больших файлов (более 900 тыс. строк):**
- **Оперативная память (RAM):** 16 ГБ
- **Процессор (CPU):** 6 ядер
- **Место на жестком диске:** 50 ГБ свободного места (для данных, образа Docker и временных файлов)

---

## Технические требования

- **Python** 3.10+
- **Streamlit**
- **Pandas**, **NumPy**
- **Plotly**, **Matplotlib**
- Библиотеки для работы с Excel: **XlsxWriter**, **openpyxl**
- Дополнительные библиотеки: **statsmodels**, **scikit-learn**, **chardet**