# main_cloud.py - специально для Streamlit Cloud
import streamlit as st
import duckdb
import os

st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

st.title("📊 E-commerce Sales Dashboard")
st.markdown("**Курсовой проект - анализ продаж интернет-магазина**")

# Создаем базу данных в памяти (не используем файлы)
conn = duckdb.connect(':memory:')

# Создаем тестовые данные
conn.execute("""
    CREATE TABLE customers AS 
    SELECT * FROM (VALUES
        (1, 'Иван Иванов', 'Москва', 25),
        (2, 'Мария Петрова', 'СПб', 30),
        (3, 'Алексей Сидоров', 'Казань', 35)
    ) AS t(id, name, city, age)
""")

conn.execute("""
    CREATE TABLE products AS 
    SELECT * FROM (VALUES
        (101, 'iPhone 14', 'Смартфоны', 999.99),
        (102, 'Ноутбук Dell', 'Ноутбуки', 1299.99),
        (103, 'Наушники Sony', 'Наушники', 199.99)
    ) AS t(id, name, category, price)
""")

conn.execute("""
    CREATE TABLE orders AS 
    SELECT * FROM (VALUES
        (1001, 1, 101, '2023-06-01', 1, 999.99, 'completed'),
        (1002, 2, 102, '2023-06-15', 1, 1299.99, 'completed'),
        (1003, 3, 103, '2023-07-01', 2, 399.98, 'pending')
    ) AS t(order_id, customer_id, product_id, order_date, quantity, total_amount, status)
""")

st.markdown("---")

# 1. Ключевые метрики
st.subheader("📈 Ключевые показатели")

col1, col2, col3 = st.columns(3)

with col1:
    total_orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    st.metric("Всего заказов", total_orders)

with col2:
    total_revenue = conn.execute("SELECT SUM(total_amount) FROM orders WHERE status='completed'").fetchone()[0]
    st.metric("Общая выручка", f"${total_revenue:,.2f}")

with col3:
    avg_order = conn.execute("SELECT AVG(total_amount) FROM orders WHERE status='completed'").fetchone()[0]
    st.metric("Средний чек", f"${avg_order:.2f}")

st.markdown("---")

# 2. Фильтры
st.sidebar.title("🔧 Фильтры")

status_filter = st.sidebar.selectbox(
    "Статус заказа",
    ["Все", "completed", "pending"]
)

# 3. Таблицы с данными
st.subheader("📋 Данные из базы")

tab1, tab2, tab3 = st.tabs(["Заказы", "Товары", "Клиенты"])

with tab1:
    if status_filter == "Все":
        orders = conn.execute("SELECT * FROM orders").fetchdf()
    else:
        orders = conn.execute(f"SELECT * FROM orders WHERE status='{status_filter}'").fetchdf()
    st.dataframe(orders)

with tab2:
    products = conn.execute("SELECT * FROM products").fetchdf()
    st.dataframe(products)

with tab3:
    customers = conn.execute("SELECT * FROM customers").fetchdf()
    st.dataframe(customers)

# 4. Простой анализ
st.subheader("📊 Анализ данных")

col1, col2 = st.columns(2)

with col1:
    st.write("**Статусы заказов:**")
    status_data = conn.execute("SELECT status, COUNT(*) as count FROM orders GROUP BY status").fetchdf()
    st.dataframe(status_data)

with col2:
    st.write("**Товары по категориям:**")
    category_data = conn.execute("SELECT category, COUNT(*) as count FROM products GROUP BY category").fetchdf()
    st.dataframe(category_data)

conn.close()

st.markdown("---")
st.success("✅ Дашборд работает на Streamlit Cloud!")
st.info("📁 Полный код: https://github.com/smariii1/ecommerce-dashboard")
# Updated via GitHub




