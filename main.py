import streamlit as st
import pandas as pd

st.set_page_config(
  page_title="E-commerce Dashboard",
  layout="wide"
)

st.title("📊 E-commerce Dashboard")

# === Загрузка данных ===
@st.cache_data
def load_data():
  return pd.read_csv("data.csv")

try:
  df = load_data()
except FileNotFoundError:
  st.error("Файл data.csv не найден. Добавь его в репозиторий.")
  st.stop()

# === Просмотр данных ===
st.subheader("📦 Данные")
st.dataframe(df)

# === Базовая информация ===
st.subheader("ℹ️ Общая информация")

c1, c2, c3 = st.columns(3)

with c1:
  st.metric("Всего заказов", len(df))

with c2:
  if "price" in df.columns:
    st.metric("Общая выручка", f"{df['price'].sum():,.0f}")
  else:
    st.warning("Нет колонки price")

with c3:
  if "customer_id" in df.columns:
    st.metric("Клиентов", df["customer_id"].nunique())
  else:
    st.warning("Нет customer_id")

# === Фильтр ===
st.subheader("🔎 Фильтрация")

if "category" in df.columns:
  cats = st.multiselect(
    "Выбери категории",
    df["category"].unique()
  )
  if cats:
    df = df[df["category"].isin(cats)]

# === График ===
st.subheader("📈 Продажи")

if "date" in df.columns and "price" in df.columns:
  df["date"] = pd.to_datetime(df["date"])
  sales = df.groupby("date")["price"].sum()
  st.line_chart(sales)
else:
  st.warning("Для графика нужны колонки date и price")

# === Топ товаров ===
st.subheader("🔥 Топ товаров")

if "product" in df.columns and "price" in df.columns:
  top = (
    df.groupby("product")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
  )
  st.bar_chart(top)
else:
  st.warning("Нужны колонки product и price")

# Updated via GitHub





