import streamlit as st
import duckdb

st.set_page_config(page_title="DuckDB Project")
st.title("📦 DuckDB база данных")

# подключение к базе данных
con = duckdb.connect("database.db")

# создание таблицы
con.execute("""
CREATE TABLE IF NOT EXISTS products (
  id INTEGER,
  name TEXT,
  price INTEGER
)
""")

# добавление данных (если таблица пустая)
count = con.execute("SELECT COUNT(*) FROM products").fetchone()[0]

if count == 0:
  con.execute("""
  INSERT INTO products VALUES
  (1, 'Phone', 500),
  (2, 'Laptop', 1200),
  (3, 'Headphones', 150)
  """)

st.success("База данных создана и заполнена")

# вывод данных
st.subheader("📊 Данные из базы")

df = con.execute("SELECT * FROM products").df()
st.dataframe(df)

# простой SQL-запрос
st.subheader("🔍 SQL запрос")

query = st.text_input(
  "Введите SQL запрос",
  "SELECT name, price FROM products WHERE price > 300"
)

if st.button("Выполнить"):
  try:
    res = con.execute(query).df()
    st.dataframe(res)
  except Exception as e:
    st.error("Ошибка в SQL запросе")


# Updated via GitHub






