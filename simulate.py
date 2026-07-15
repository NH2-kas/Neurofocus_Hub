import csv
import random
import json  # для работы с JSON-файлами
from datetime import datetime, timedelta

def load_config(config_path="config.json"):
    """Читает настройки из JSON-файла и возвращает словарь."""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_timestamps(start_time, duration_minutes, interval_seconds):
    timestamps = []
    current_time = start_time
    end_time = start_time + timedelta(minutes=duration_minutes)
    while current_time < end_time:
        ts_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        timestamps.append(ts_str)
        current_time += timedelta(seconds=interval_seconds)
    return timestamps

def generate_concentration():
    if random.random() < 0.7:
        return round(random.uniform(40, 80), 1)
    else:
        if random.random() < 0.5:
            return round(random.uniform(0, 30), 1)
        else:
            return round(random.uniform(70, 100), 1)

def generate_session(students, duration_minutes=10, interval_seconds=5):
    start_time = datetime.now().replace(microsecond=0)
    timestamps = generate_timestamps(start_time, duration_minutes, interval_seconds)
    rows = []
    for ts in timestamps:
        for student in students:
            concentration = generate_concentration()
            rows.append({
                "timestamp": ts,
                "student": student,
                "concentration": concentration
            })
    return rows

def save_to_csv(rows, filename="session.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        fieldnames = ["timestamp", "student", "concentration"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Файл {filename} создан. Записей: {len(rows)}")

if __name__ == "__main__":
    # Загружаем конфиг
    config = load_config()
    students_list = config["students"]
    duration = config.get("session_duration_minutes", 10)
    interval = config.get("sample_interval_seconds", 5)

    print(f"Генерация данных для {len(students_list)} студентов...")
    data = generate_session(students_list, duration_minutes=duration, interval_seconds=interval)
    save_to_csv(data, "session.csv")
    print("Готово!")