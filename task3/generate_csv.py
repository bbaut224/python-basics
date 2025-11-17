"""
generate_csv.py — Генерация примера CSV для учебного задания
Создаёт файл students.csv с 10 студентами
"""

import csv

# Данные студентов: ID, Имя, Оценка
students = [
    [1, "Иван Иванов", 85],
    [2, "Мария Петрова", 92],
    [3, "Алексей Сидоров", 78],
    [4, "Елена Кузнецова", 88],
    [5, "Дмитрий Смирнов", 91],
    [6, "Светлана Орлова", 74],
    [7, "Никита Васильев", 82],
    [8, "Ольга Козлова", 95],
    [9, "Владимир Новиков", 69],
    [10, "Анна Фролова", 87],
]

# Имя файла
filename = "students.csv"

# Запись в CSV
with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for student in students:
        writer.writerow(student)

print(f"Файл {filename} успешно создан с {len(students)} студентами.")
