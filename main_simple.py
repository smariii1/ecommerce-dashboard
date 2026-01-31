# main_simple.py - работает на Streamlit Cloud
import streamlit as st
import duckdb

st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

st.title("📊 E-commerce Sales Dashboard")
st.markdown("**Курсовой проект - анализ продаж**")

# Создаем базу в памяти
conn = duckdb.connect(':memory:')

# Создаем тестовые данные
conn.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        month TEXT,
        category TEXT,
        revenue REAL,
        orders INTEGER
    )
""")

conn.execute("""
    INSERT INTO sales VALUES
    ('2023-01', 'Смартфоны', 10000, 50),
    ('2023-02', 'Ноутбуки', 15000, 30),
    ('2023-03', 'Наушники', 8000, 80),
    ('2023-04', 'Планшеты', 12000, 40),
    ('2023-05', 'Аксессуары', 5000, 100)
""")

st.markdown("---")

# 1. Ключевые метрики
st.subheader("📈 Ключевые показатели")

col1, col2, col3 = st.columns(3)

with col1:
    total_rev = conn.execute("SELECT SUM(revenue) FROM sales").fetchone()[0]
    st.metric("Общая выручка", f"${total_rev:,.2f}")

with col2:
    total_orders = conn.execute("SELECT SUM(orders) FROM sales").fetchone()[0]
    st.metric("Всего заказов", total_orders)

with col3:
    avg_order = conn.execute("SELECT AVG(revenue/orders) FROM sales").fetchone()[0]
    st.metric("Средний чек", f"${avg_order:.2f}")

st.markdown("---")

# 2. Фильтры
st.sidebar.title("🔧 Фильтры")

categories = conn.execute("SELECT DISTINCT category FROM sales").fetchall()
categories = ["Все"] + [c[0] for c in categories]
selected_cat = st.sidebar.selectbox("Категория", categories)

# 3. Таблица данных
st.subheader("📋 Данные о продажах")

if selected_cat == "Все":
    data = conn.execute("SELECT * FROM sales ORDER BY month").fetchdf()
else:
    data = conn.execute(f"SELECT * FROM sales WHERE category='{selected_cat}' ORDER BY month").fetchdf()

st.dataframe(data)

# 4. Простая визуализация
st.subheader("📊 Визуализация")

# Столбчатая диаграмма (встроенная в Streamlit)
if not data.empty:
    chart_data = data[['month', 'revenue']].set_index('month')
    st.bar_chart(chart_data)

# 5. Дополнительный анализ
st.subheader("📝 Анализ по категориям")

col1, col2 = st.columns(2)

with col1:
    st.write("**Выручка по категориям:**")
    cat_revenue = conn.execute("""
        SELECT category, SUM(revenue) as total
        FROM sales 
        GROUP BY category
        ORDER BY total DESC
    """).fetchdf()
    st.dataframe(cat_revenue)

with col2:
    st.write("**Заказы по месяцам:**")
    monthly = conn.execute("""
        SELECT month, SUM(orders) as orders
        FROM sales
        GROUP BY month
        ORDER BY month
    """).fetchdf()
    st.dataframe(monthly)

conn.close()

st.markdown("---")
st.success("✅ Дашборд работает на Streamlit Cloud!")
st.info("📁 Полный код: https://github.com/smariii1/ecommerce-dashboard")
