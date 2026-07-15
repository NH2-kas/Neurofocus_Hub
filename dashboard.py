import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import json
import subprocess
from datetime import datetime

# Заголовок страницы
st.set_page_config(page_title="NeuroFocus Hub", layout="wide")
st.title("NeuroFocus Hub – Мониторинг концентрации")

# Загружаем конфиг (для порога тревоги, списка студентов)
@st.cache_data
def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()
alert_threshold = config.get("alert_threshold", 30)

# Функция загрузки CSV
def load_data():
    if not os.path.exists("session.csv"):
        return None
    df = pd.read_csv("session.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

# Основная логика отображения
st.sidebar.header("Управление")
if st.sidebar.button("🔄 Обновить данные"):
    # Запускаем simulate.py
    with st.spinner("Генерация новых данных..."):
        result = subprocess.run(["python", "simulate.py"], capture_output=True, text=True)
        if result.returncode == 0:
            st.sidebar.success("Данные обновлены!")
        else:
            st.sidebar.error("Ошибка при генерации данных")

# Загрузка данных
df = load_data()

if df is None:
    st.warning("Файл session.csv не найден. Пожалуйста, сначала сгенерируйте данные (нажмите кнопку «Обновить данные» или запустите simulate.py вручную).")
else:
    # Показываем актуальное время данных
    last_time = df["timestamp"].max()
    st.info(f"Последние данные от: {last_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Линейный график концентрации по студентам
    st.subheader("Динамика концентрации по студентам")
    fig_line = px.line(df, x="timestamp", y="concentration", color="student",
                       title="Концентрация во времени")
    # Добавляем горизонтальную линию порога тревоги
    fig_line.add_hline(y=alert_threshold, line_dash="dot", line_color="red",
                       annotation_text="Тревожный порог", annotation_position="bottom right")
    fig_line.update_layout(xaxis_title="Время", yaxis_title="Концентрация (%)")
    st.plotly_chart(fig_line, use_container_width=True)

    # Таблица последних значений (последний момент времени для каждого студента)
    st.subheader("Текущий статус студентов")
    # Находим последний timestamp
    latest_ts = df["timestamp"].max()
    latest_data = df[df["timestamp"] == latest_ts][["student", "concentration"]]
    # Переименовываем колонки для красоты
    latest_data = latest_data.rename(columns={"student": "Студент", "concentration": "Концентрация %"})
    st.dataframe(latest_data, hide_index=True)

    # Тепловая карта (heatmap)
    st.subheader("Тепловая карта концентрации")
    # Строим сводную таблицу: строки = временные метки, столбцы = студенты, значения = концентрация
    pivot = df.pivot(index="timestamp", columns="student", values="concentration")
    # Преобразуем индекс в строку для более чистого отображения на оси
    pivot.index = pivot.index.strftime("%H:%M:%S")
    fig_heatmap = px.imshow(pivot.T,  # транспонируем, чтобы студенты были по вертикали
                            labels=dict(x="Время", y="Студент", color="Концентрация"),
                            aspect="auto",
                            color_continuous_scale="RdYlGn",
                            title="Тепловая карта по студентам")
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Дополнительно можно показать сырые данные (опционально)
    with st.expander("Показать все данные"):
        st.dataframe(df)