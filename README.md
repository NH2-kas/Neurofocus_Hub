# NeuroFocus Hub (MVP)

Инструмент для преподавателей для мониторинга концентрации студентов в реальном времени (симулированные данные).

## Возможности

- Генератор учебных сессий (`simulate.py`) создаёт CSV с данными концентрации 5 студентов.
- Streamlit-дашборд (`dashboard.py`) визуализирует:
  - динамику концентрации,
  - текущий статус каждого студента,
  - тепловую карту.
- Настройки группы (имена, порог тревоги) вынесены в `config.json`.

## Как запустить

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/ТВОЙ-ЛОГИН/neurofocus-hub.git
   cd neurofocus-hub

2. Создать и активировать виртуальное окружение:

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate

3. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   (Файл requirements.txt нужно создать: см. ниже)

4. Сгенерировать тестовые данные:

   ```bash
   python simulate.py

5. Запустить дашборд:

   ```bash
   streamlit run dashboard.py
   
6.Открыть в браузере http://localhost:8501.

## Структура проекта
**simulate.py** — генератор CSV с данными.

**dashboard.py** — дашборд на Streamlit.

**config.json** — список студентов и параметры.

**session.csv** — сгенерированные данные (не хранится в репозитории).

## Технологии
Python, Streamlit, Pandas, Plotly, NumPy.

## Автор
Амин Касимов
