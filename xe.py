import streamlit as st

# --- Настройки страницы с иконкой ---
st.set_page_config(
    page_title="Калькулятор Хлебных Единиц",
    page_icon="https://cdn-icons-png.flaticon.com/512/1046/1046784.png",  # иконка хлеба
    layout="centered"
)


# --- Вставка apple-touch-icon для iOS и PWA ---
st.markdown("""
<link rel="apple-touch-icon" sizes="180x180" href="https://cdn-icons-png.flaticon.com/512/1046/1046784.png">
<link rel="icon" type="image/png" sizes="32x32" href="https://cdn-icons-png.flaticon.com/512/1046/1046784.png">
<link rel="icon" type="image/png" sizes="16x16" href="https://cdn-icons-png.flaticon.com/512/1046/1046784.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
""", unsafe_allow_html=True)



# --- Заголовок ---
st.title("🍞 Калькулятор Хлебных Единиц (ХЕ)")
st.write("Введите данные и получите расчёт ХЕ по углеводам, калорийности и общую сумму.")

# --- Инициализация session_state ---
for key in ["carbs", "protein", "fat", "history"]:
    if key not in st.session_state:
        st.session_state[key] = 0.0 if key != "history" else []

# --- Функции ---
def reset_fields():
    st.session_state.carbs = 0.0
    st.session_state.protein = 0.0
    st.session_state.fat = 0.0

def clear_history():
    st.session_state.history = []

# --- Поля ввода ---
carbs = st.number_input("Углеводы (г):", min_value=0.0, step=1.0, value=st.session_state.carbs, key="carbs")
protein = st.number_input("Белки (г):", min_value=0.0, step=1.0, value=st.session_state.protein, key="protein")
fat = st.number_input("Жиры (г):", min_value=0.0, step=1.0, value=st.session_state.fat, key="fat")
portions = st.number_input("Количество порций:", min_value=1, step=1, value=1)

# --- Кнопки ---
col1, col2, col3 = st.columns([1,1,1])
with col1:
    calculate = st.button("Рассчитать ХЕ", use_container_width=True, type="primary")
with col2:
    st.button("Сбросить поля", on_click=reset_fields, use_container_width=True)


# --- Логика расчёта ---
if calculate:
    # --- Общие значения на одну порцию ---
    calories_single = (carbs*4 + protein*4 + fat*9)
    xe_carbs_single = carbs / 10
    xe_calories_single = calories_single / 100
    xe_total_single = xe_carbs_single + xe_calories_single

    # --- Умножаем на количество порций для общего значения ---
    calories_total = calories_single * portions
    xe_carbs_total = xe_carbs_single * portions
    xe_calories_total = xe_calories_single * portions
    xe_total_total = xe_total_single * portions

    # --- Значения на порцию ---
    calories_per_portion = calories_total / portions
    xe_carbs_per_portion = xe_carbs_total / portions
    xe_calories_per_portion = xe_calories_total / portions
    xe_total_per_portion = xe_total_total / portions

    # --- Отображение результатов ---
    st.success(f"✅ Общие результаты (для {portions} порций):")
    st.metric("Общая калорийность", f"{calories_total:.1f} ккал")
    st.metric("ХЕ по углеводам", f"{xe_carbs_total:.2f}")
    st.metric("ХЕ по калорийности", f"{xe_calories_total:.2f}")
    st.metric("💠 Общая сумма ХЕ", f"{xe_total_total:.2f}")

    st.info("На одну порцию:")
    st.write(f"Калорийность: {calories_per_portion:.1f} ккал")
    st.write(f"ХЕ по углеводам: {xe_carbs_per_portion:.2f}")
    st.write(f"ХЕ по калорийности: {xe_calories_per_portion:.2f}")
    st.write(f"💠 Общая ХЕ: {xe_total_per_portion:.2f}")

    # --- Добавляем в историю ---
    st.session_state.history.append({
        "Углеводы": carbs,
        "Белки": protein,
        "Жиры": fat,
        "Порции": portions,
        "Калорийность (всего)": calories_total,
        "ХЕ по углеводам (всего)": xe_carbs_total,
        "ХЕ по калорийности (всего)": xe_calories_total,
        "Общая ХЕ (всего)": xe_total_total
    })

    # --- Добавление записи в историю ---
    st.session_state.history.append({
        "Углеводы": carbs,
        "Белки": protein,
        "Жиры": fat,
        "Калорийность": calories,
        "ХЕ по углеводам": xe_carbs,
        "ХЕ по калорийности": xe_calories,
        "Общая ХЕ": xe_total
    })




# --- Вкладки: основная и инструкция по БЖЕ ---
tab1, tab2 = st.tabs(["📘 Как компенсировать БЖЕ?", "📜 История расчётов"])

with tab1:
    st.markdown("""
    ### 💉 Как компенсировать БЖЕ?
    1БЖЕ = 1ХЕ.  
    Дозу нужно растягивать, либо подкалывать через 1–2–3 часа после еды.

    #### ⏳ Как растягивать:
    • 1 БЖЕ — на **3 часа**  
    • 2 БЖЕ — на **4 часа**  
    • 3 БЖЕ — на **5 часов**  
    • Более 4 БЖЕ — от **5 до 10+ часов**

    #### 💡 Если вы на помпе:
    Сложите дозы на ХЕ и БЖЕ, разделите пополам:  
    - 50% введите **нормальным болюсом** перед едой  
    - 50% растяните на **4–5 часов**

    #### 💉 Если вы на ручках:
    Сделайте то же самое, но:  
    - 50% — **подколка перед едой**  
    - 50% — **через 1.5–3 часа**
    """)

with tab2:
    if st.session_state.history:
        with st.expander("📜 Показать историю последних расчётов", expanded=False):
            st.button("Очистить историю", on_click=clear_history, use_container_width=True)
            for i, entry in enumerate(reversed(st.session_state.history[-5:]), 1):
                st.write(f"**Расчёт {i}:**")
                st.write(f"Углеводы: {entry['Углеводы']} г, Белки: {entry['Белки']} г, Жиры: {entry['Жиры']} г")
                st.write(f"Калорийность: {entry['Калорийность']:.1f} ккал")
                st.write(f"ХЕ по углеводам: {entry['ХЕ по углеводам']:.2f}, ХЕ по калорийности: {entry['ХЕ по калорийности']:.2f}")
                st.write(f"💠 Общая ХЕ: {entry['Общая ХЕ']:.2f}")
                st.markdown("---")
    else:
        st.info("История пока пуста. Сделайте расчёт, чтобы она появилась 🧮")

        
# --- Подпись ---
st.markdown("---")
st.caption("📘 Формулы: 10 г углеводов = 1 ХE | 100 ккал = 1 ХЕ")
st.caption("1 г белка = 4 ккал | 1 г жира = 9 ккал")


