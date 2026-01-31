import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ========== НАСТРОЙКА СТРАНИЦЫ ==========
st.set_page_config(
    page_title="📊 E-commerce Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== КАСТОМНЫЙ CSS ==========
st.markdown("""
<style>
    /* Основные стили */
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    
    /* Заголовки */
    h1 {
        color: #2E86AB;
        border-bottom: 3px solid #A23B72;
        padding-bottom: 10px;
    }
    
    h2 {
        color: #2E86AB;
        margin-top: 30px !important;
    }
    
    /* Карточки метрик */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: bold !important;
        color: #2E86AB !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    
    /* Улучшение таблиц */
    .dataframe {
        border-radius: 10px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        border: 1px solid #ddd !important;
    }
    
    /* Кнопки */
    .stButton > button {
        background: linear-gradient(90deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(46, 134, 171, 0.4);
    }
    
    /* Боковая панель */
    .css-1d391kg {
        background-color: #2E86AB;
    }
</style>
""", unsafe_allow_html=True)

# ========== СИДЕБАР С ФИЛЬТРАМИ ==========
with st.sidebar:
    st.title("⚙️ Фильтры и настройки")
    st.markdown("---")
    
    # Фильтр по дате
    st.subheader("📅 Период")
    date_option = st.radio(
        "Выберите период:",
        ["Последние 3 месяца", "Последние 6 месяцев", "Весь год", "Произвольный"]
    )
    
    if date_option == "Произвольный":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("С", value=datetime(2024, 1, 1))
        with col2:
            end_date = st.date_input("По", value=datetime(2024, 4, 30))
    
    # Фильтр по категориям
    st.subheader("📦 Категории")
    categories = st.multiselect(
        "Выберите категории:",
        ["📱 Электроника", "👕 Одежда", "📚 Книги", "🎮 Игрушки", "💄 Косметика", "🏠 Дом"],
        default=["📱 Электроника", "👕 Одежда"]
    )
    
    # Фильтр по регионам
    st.subheader("🌍 Регион")
    region = st.selectbox(
        "Выберите регион:",
        ["Все регионы", "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань"]
    )
    
    # Кнопки управления
    st.markdown("---")
    apply_btn = st.button("✅ Применить фильтры", type="primary", use_container_width=True)
    reset_btn = st.button("🔄 Сбросить фильтры", use_container_width=True)
    
    if reset_btn:
        st.rerun()
    
    # Информация
    st.markdown("---")
    st.info("""
    **ℹ️ Информация:**
    - Данные обновляются ежедневно
    - Все суммы в тысячах рублей
    - GMT+3 Московское время
    """)

# ========== ЗАГОЛОВОК ==========
st.title("📊 Аналитика продаж e-commerce")
st.markdown("Дашборд для мониторинга ключевых метрик и анализа эффективности")
st.markdown("---")

# ========== КЛЮЧЕВЫЕ МЕТРИКИ (4 КОЛОНКИ) ==========
st.header("📈 Ключевые показатели")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Общая выручка",
        value="2.8M ₽",
        delta="+12.5%",
        delta_color="normal",
        help="Выручка за выбранный период"
    )

with col2:
    st.metric(
        label="👥 Всего клиентов",
        value="1,245",
        delta="+8.2%",
        help="Уникальные клиенты"
    )

with col3:
    st.metric(
        label="📦 Заказов",
        value="3,458",
        delta="+15.3%",
        help="Общее количество заказов"
    )

with col4:
    st.metric(
        label="📊 Средний чек",
        value="2,450 ₽",
        delta="-3.1%",
        delta_color="inverse",
        help="Средняя сумма заказа"
    )

st.markdown("---")

# ========== ДАННЫЕ ИЗ БАЗЫ (ТАБЛИЦА) ==========
st.header("📋 Детальные данные")

# Создаем DataFrame с данными
data = {
    'Месяц': ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь'],
    'Выручка, тыс. ₽': [450, 520, 680, 620, 710, 780],
    'Клиенты': [320, 380, 420, 410, 460, 500],
    'Заказы': [850, 920, 1150, 1050, 1200, 1300],
    'Конверсия, %': [2.1, 2.3, 2.8, 2.5, 2.7, 2.9],
    'Средний чек, ₽': [2350, 2410, 2560, 2480, 2520, 2600]
}

df = pd.DataFrame(data)

# Красивое отображение таблицы
st.dataframe(
    df.style
    .background_gradient(subset=['Выручка, тыс. ₽', 'Клиенты'], cmap='Blues')
    .background_gradient(subset=['Конверсия, %'], cmap='YlOrRd')
    .format({'Выручка, тыс. ₽': '{:.0f}', 'Средний чек, ₽': '{:.0f}', 'Конверсия, %': '{:.1f}'})
    .set_properties(**{
        'text-align': 'center',
        'font-size': '14px'
    })
    .set_table_styles([
        {'selector': 'th', 'props': [
            ('background-color', '#2E86AB'),
            ('color', 'white'),
            ('font-weight', 'bold'),
            ('text-align', 'center')
        ]},
        {'selector': 'td', 'props': [
            ('border', '1px solid #ddd')
        ]}
    ]),
    use_container_width=True,
    height=300
)

# Кнопка скачивания
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Скачать CSV",
    data=csv,
    file_name="ecommerce_data.csv",
    mime="text/csv",
    type="primary"
)

st.markdown("---")

# ========== ГРАФИКИ (2 КОЛОНКИ) ==========
st.header("📊 Визуализация данных")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Линейный график продаж
    st.subheader("📈 Динамика выручки")
    
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(
        x=df['Месяц'],
        y=df['Выручка, тыс. ₽'],
        mode='lines+markers+text',
        name='Выручка',
        line=dict(color='#2E86AB', width=4),
        marker=dict(size=10, color='white', line=dict(width=2, color='#2E86AB')),
        text=df['Выручка, тыс. ₽'],
        textposition="top center",
        fill='tozeroy',
        fillcolor='rgba(46, 134, 171, 0.1)'
    ))
    
    fig1.add_trace(go.Bar(
        x=df['Месяц'],
        y=df['Клиенты'],
        name='Клиенты',
        marker_color='#A23B72',
        opacity=0.6,
        yaxis='y2'
    ))
    
    fig1.update_layout(
        height=400,
        template='plotly_white',
        hovermode='x unified',
        showlegend=True,
        yaxis=dict(title='Выручка, тыс. ₽', titlefont=dict(color='#2E86AB')),
        yaxis2=dict(
            title='Клиенты',
            titlefont=dict(color='#A23B72'),
            overlaying='y',
            side='right'
        ),
        plot_bgcolor='rgba(248, 249, 250, 1)',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    # Круговая диаграмма категорий
    st.subheader("📦 Распределение по категориям")
    
    categories_data = pd.DataFrame({
        'Категория': ['Электроника', 'Одежда', 'Книги', 'Игрушки', 'Косметика'],
        'Доля %': [38, 25, 15, 12, 10],
        'Выручка, тыс. ₽': [1064, 700, 420, 336, 280]
    })
    
    fig2 = px.pie(
        categories_data,
        values='Доля %',
        names='Категория',
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4,
        custom_data=['Выручка, тыс. ₽']
    )
    
    fig2.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Доля: %{percent}<br>Выручка: %{customdata[0]} тыс. ₽"
    )
    
    fig2.update_layout(
        height=400,
        showlegend=False,
        annotations=[dict(
            text='Категории',
            x=0.5, y=0.5,
            font_size=14,
            showarrow=False
        )]
    )
    
    st.plotly_chart(fig2, use_container_width=True)

# ========== ДОПОЛНИТЕЛЬНАЯ АНАЛИТИКА ==========
st.header("🔍 Дополнительная аналитика")

tab1, tab2, tab3 = st.tabs(["📋 Подробная статистика", "📈 Тренды", "💡 Инсайты"])

with tab1:
    st.subheader("Статистика по месяцам")
    
    # Создаем расширенную статистику
    stats_df = df.copy()
    stats_df['Выручка на клиента'] = stats_df['Выручка, тыс. ₽'] * 1000 / stats_df['Клиенты']
    stats_df['Заказов на клиента'] = stats_df['Заказы'] / stats_df['Клиенты']
    
    st.dataframe(
        stats_df.style
        .format({
            'Выручка на клиента': '{:.0f} ₽',
            'Заказов на клиента': '{:.1f}'
        }),
        use_container_width=True
    )

with tab2:
    st.subheader("Тренды и прогноз")
    
    # Простой прогноз (линейная экстраполяция)
    months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен']
    forecast = [450, 520, 680, 620, 710, 780, 850, 920, 980]  # Прогноз
    
    fig3 = go.Figure()
    
    fig3.add_trace(go.Scatter(
        x=months[:6],
        y=df['Выручка, тыс. ₽'],
        mode='lines+markers',
        name='Факт',
        line=dict(color='#2E86AB', width=3)
    ))
    
    fig3.add_trace(go.Scatter(
        x=months[5:],
        y=forecast[5:],
        mode='lines+markers',
        name='Прогноз',
        line=dict(color='#A23B72', width=3, dash='dash')
    ))
    
    fig3.update_layout(
        title='Прогноз выручки на следующие месяцы',
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.subheader("Ключевые инсайты")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        ### ✅ Положительные тренды:
        
        **1. Рост выручки на 73%**  
        С января по июнь выручка выросла с 450K до 780K ₽
        
        **2. Увеличение клиентской базы**  
        +180 клиентов за 6 месяцев (+56%)
        
        **3. Повышение конверсии**  
        Конверсия выросла с 2.1% до 2.9%
        """)
    
    with col2:
        st.warning("""
        ### ⚠️ Внимание на:
        
        **1. Снижение среднего чека**  
        В апреле наблюдается падение на 3.1%
        
        **2. Сезонность спроса**  
        Пик продаж в марте, спад в апреле
        
        **3. Зависимость от электроники**  
        38% выручки от одной категории
        """)
    
    st.info("""
    ### 💡 Рекомендации:
    
    1. **Диверсифицируйте категории** — развивайте другие товарные группы
    2. **Запустите акцию в апреле** — для сглаживания сезонного спада
    3. **Внедрите программу лояльности** — для повышения среднего чека
    """)

# ========== ФУТЕР ==========
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>📊 <b>E-commerce Analytics Dashboard</b> | Данные обновлены: 2024-06-30 23:59 | Версия 1.2.0</p>
    <p style='font-size: 0.9em;'>Для вопросов и предложений: analytics@company.com</p>
</div>
""", unsafe_allow_html=True)

# ========== СКРЫТАЯ СЕКЦИЯ ДЛЯ ОТЛАДКИ ==========
with st.expander("🔧 Отладочная информация"):
    st.write("**Параметры фильтров:**")
    st.write(f"- Категории: {categories}")
    st.write(f"- Регион: {region}")
    st.write(f"- Период: {date_option}")
    
    st.write("**Техническая информация:**")
    st.write(f"- Размер DataFrame: {df.shape[0]} строк, {df.shape[1]} столбцов")
    st.write(f"- Типы данных: {df.dtypes.to_dict()}")
# Updated via GitHub

