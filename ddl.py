"""
Модуль для создания базы данных DuckDB.
"""
import duckdb
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("Создание базы данных для интернет-магазина...")

# Создаем подключение к базе данных
conn = duckdb.connect('my.db')

# 1. Создаем таблицы из SQL файла
with open('queries/01_create_tables.sql', 'r') as f:
    create_tables_sql = f.read()
    conn.execute(create_tables_sql)

print("✓ Таблицы созданы")

# 2. Создаем тестовые данные
# Клиенты
customers_data = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'first_name': ['Иван', 'Мария', 'Алексей', 'Ольга', 'Дмитрий'],
    'last_name': ['Иванов', 'Петрова', 'Сидоров', 'Смирнова', 'Кузнецов'],
    'email': ['ivan@mail.com', 'maria@mail.com', 'alex@mail.com', 'olga@mail.com', 'dmitry@mail.com'],
    'age': [25, 30, 35, 28, 40],
    'city': ['Москва', 'Санкт-Петербург', 'Казань', 'Москва', 'Новосибирск'],
    'registration_date': ['2023-01-15', '2023-02-20', '2023-03-10', '2023-04-05', '2023-05-12']
})

# Товары
products_data = pd.DataFrame({
    'product_id': [101, 102, 103, 104, 105],
    'product_name': ['iPhone 14', 'Ноутбук Dell', 'Наушники Sony', 'Планшет Samsung', 'Чехол для телефона'],
    'category': ['Смартфоны', 'Ноутбуки', 'Наушники', 'Планшеты', 'Аксессуары'],
    'price': [999.99, 1299.99, 199.99, 499.99, 29.99],
    'cost': [600.00, 800.00, 100.00, 300.00, 15.00],
    'stock_quantity': [50, 30, 100, 40, 200]
})

# Заказы
orders_data = pd.DataFrame({
    'order_id': [1001, 1002, 1003, 1004, 1005],
    'customer_id': [1, 2, 3, 1, 4],
    'product_id': [101, 102, 103, 104, 105],
    'order_date': ['2023-06-01', '2023-06-15', '2023-07-01', '2023-07-15', '2023-08-01'],
    'quantity': [1, 1, 2, 1, 3],
    'total_amount': [999.99, 1299.99, 399.98, 499.99, 89.97],
    'status': ['completed', 'completed', 'pending', 'completed', 'completed']
})

# Загружаем данные в таблицы
conn.execute("INSERT INTO customers SELECT * FROM customers_data")
conn.execute("INSERT INTO products SELECT * FROM products_data")
conn.execute("INSERT INTO orders SELECT * FROM orders_data")

print("✓ Тестовые данные добавлены")

# 3. Создаем представления (views)
with open('queries/02_create_views.sql', 'r') as f:
    create_views_sql = f.read()
    conn.execute(create_views_sql)

print("✓ Представления созданы")

# Проверяем
print("\n📊 Проверка данных:")
print(f"Клиенты: {conn.execute('SELECT COUNT(*) FROM customers').fetchone()[0]}")
print(f"Товары: {conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]}")
print(f"Заказы: {conn.execute('SELECT COUNT(*) FROM orders').fetchone()[0]}")

conn.close()
print("\n✅ База данных успешно создана: my.db")

print("\nСледующий шаг: запустите дашборд командой:")

print("streamlit run main.py")

# Updated via GitHub


