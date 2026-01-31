import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="Простой анализ продаж", layout="wide")
st.title("📊 Простой анализ продаж")

# подключение к DuckDB
con = duckdb.connect("sales.db")

# создаём таблицу с данными
con.execute("""
CREATE TABLE IF NOT EXISTS sales (
    month TEXT,
    sales INTEGER,
    clients INTEGER
)
""")

# проверяем, есть ли данные, если нет — добавляем
count = con.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
if count == 0:
    con.execute("""
    INSERT INTO sales VALUES
    ('Янв', 100, 50),
    ('Фев', 150, 60),
    ('Мар', 200, 70),
    ('Апр', 180, 65)
    """)

# читаем данные из базы
df = con.execute("SELECT * FROM sales").df()

# таблица
st.subheader("Данные из базы")
st.dataframe(df)

# график
st.subheader("График продаж")
st.line_chart(df.set_index("month"))

# ключевые цифры
st.subheader("Ключевые цифры")
total_sales = df["sales"].sum()
total_clients = df["clients"].sum()
avg_check = total_sales / total_clients if total_clients > 0 else 0

c1, c2, c3 = st.columns(3)
c1.metric("Всего продаж", total_sales)
c2.metric("Средний чек", f"${int(avg_check)}")
c3.metric("Клиентов", total_clients)



# Updated via GitHub







