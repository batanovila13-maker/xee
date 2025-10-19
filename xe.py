import streamlit as st

# --- Настройки страницы ---
st.set_page_config(
    page_title="Калькулятор Хлебных Единиц",
    page_icon="🍞",
    layout="wide"
)

# --- Инициализация состояния ---
for key in ["carbs", "protein", "fat", "portions", "history"]:
    if key not in st.session_state:
        st.session_state[key] = 0.0 if key in ["carbs", "protein", "fat"] else 1 if key == "portions" else []

# --- Заголовок ---
st.title("🍞 Калькулятор Хлебных Единиц (ХЕ)")

# --- Функции ---
def reset_fields():
    st.session_state.carbs = 0.0
    st.session_state.protein = 0.0
    st.session_state.fat = 0.0
    st.session_state.portions = 1

def clear_history():
    st.session_state.history = []

# --- ВКЛАДКИ ---
tab1, tab2 = st.tabs(["🧮 Основной расчёт", "⚖️ Расчёт по продукту"])

# === 🧮 Вкладка 1 — Основной расчёт ===
with tab1:
    st.subheader("Расчёт по порциям")

    carbs = st.number_input("Углеводы (г):", min_value=0.0, step=1.0, key="carbs")
    protein = st.number_input("Белки (г):", min_value=0.0, step=1.0, key="protein")
    fat = st.number_input("Жиры (г):", min_value=0.0, step=1.0, key="fat")
    portions = st.number_input("Количество порций:", min_value=1, step=1, key="portions")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        calc_main = st.button("Рассчитать ХЕ", use_container_width=True, type="primary", key="calc_main")
    with col_btn2:
        st.button("Сбросить", on_click=reset_fields, use_container_width=True)

    if calc_main:
        # Расчёты
        calories_single = carbs * 4 + protein * 4 + fat * 9
        xe_carbs_single = carbs / 10
        bje_single = (protein * 4 + fat * 9) / 100
        xe_total_single = xe_carbs_single + bje_single

        calories_total = calories_single * portions
        xe_carbs_total = xe_carbs_single * portions
        bje_total = bje_single * portions
        xe_total_total = xe_total_single * portions

        with st.container(border=True):
            st.success(f"✅ Результаты (для {portions} порций):")
            st.metric("Общая калорийность", f"{calories_total:.1f} ккал")
            st.metric("ХЕ по углеводам", f"{xe_carbs_total:.2f}")
            st.metric("БЖЕ", f"{bje_total:.2f}")
            st.metric("💠 Общая ХЕ", f"{xe_total_total:.2f}")

            st.info("На 1 порцию:")
            st.write(f"Ккал: {calories_total / portions:.1f}")
            st.write(f"ХЕ по углеводам: {xe_carbs_total / portions:.2f}")
            st.write(f"БЖЕ: {bje_total / portions:.2f}")
            st.write(f"💠 Общая ХЕ: {xe_total_total / portions:.2f}")

        # Добавляем в историю
        st.session_state.history.append({
            "Тип расчёта": "Основной",
            "Углеводы": carbs,
            "Белки": protein,
            "Жиры": fat,
            "Порции": portions,
            "Калорийность (всего)": calories_total,
            "ХЕ по углеводам (всего)": xe_carbs_total,
            "БЖЕ (всего)": bje_total,
            "Общая ХЕ (всего)": xe_total_total
        })

# === ⚖️ Вкладка 2 — Расчёт по продукту ===
with tab2:
    st.subheader("Расчёт по продукту (на 100 г)")

    carbs_100 = st.number_input("Углеводы (г/100 г):", min_value=0.0, step=0.1, key="carbs_100")
    protein_100 = st.number_input("Белки (г/100 г):", min_value=0.0, step=0.1, key="protein_100")
    fat_100 = st.number_input("Жиры (г/100 г):", min_value=0.0, step=0.1, key="fat_100")
    mass = st.number_input("Масса продукта (г):", min_value=1.0, step=1.0, key="mass")

    if st.button("Рассчитать по продукту", type="primary", use_container_width=True, key="calc_product"):
        # Пересчёт на массу
        carbs_total = carbs_100 * mass / 100
        protein_total = protein_100 * mass / 100
        fat_total = fat_100 * mass / 100

        calories_total = (carbs_total * 4) + (protein_total * 4) + (fat_total * 9)
        xe_carbs = carbs_total / 10
        bje = (protein_total * 4 + fat_total * 9) / 100
        xe_total = xe_carbs + bje

        with st.container(border=True):
            st.success("✅ Результаты для продукта:")
            st.metric("Масса", f"{mass:.0f} г")
            st.metric("ХЕ по углеводам", f"{xe_carbs:.2f}")
            st.metric("БЖЕ", f"{bje:.2f}")
            st.metric("💠 Общая ХЕ", f"{xe_total:.2f}")
            st.metric("Калорийность", f"{calories_total:.1f} ккал")

            st.info(f"""
            **Углеводов:** {carbs_total:.1f} г  
            **Белков:** {protein_total:.1f} г  
            **Жиров:** {fat_total:.1f} г
            """)

        # Добавляем в историю
        st.session_state.history.append({
            "Тип расчёта": "По продукту",
            "Углеводы": carbs_total,
            "Белки": protein_total,
            "Жиры": fat_total,
            "Порции": 1,
            "Калорийность (всего)": calories_total,
            "ХЕ по углеводам (всего)": xe_carbs,
            "БЖЕ (всего)": bje,
            "Общая ХЕ (всего)": xe_total
        })

# --- 📘 Справка ---
st.markdown("---")
st.header("📘 Как компенсировать БЖЕ")
st.markdown("""
1 БЖЕ = 1 ХЕ.  
Дозу нужно растягивать или подкалывать через 1–3 часа после еды.

#### ⏳ Пример:
- 1 БЖЕ → на 3 часа  
- 2 БЖЕ → на 4 часа  
- 3 БЖЕ → на 5 часов  
- Более 4 БЖЕ → на 6–10 часов  

#### 💉 Если вы на помпе:
• 50 % — обычный болюс перед едой  
• 50 % — растянуть на 4–5 ч  

#### 💉 Если вы на ручках:
• 50 % — подколка перед едой  
• 50 % — через 1.5–3 ч  
""")

# --- 📜 История расчётов ---
st.markdown("---")
st.header("📜 История последних расчётов")

if st.session_state.history:
    st.button("Очистить историю", on_click=clear_history, use_container_width=True)
    for i, entry in enumerate(reversed(st.session_state.history[-6:]), 1):
        st.write(f"**{i}. {entry['Тип расчёта']}**")
        st.write(f"Углеводы: {entry['Углеводы']:.1f} г | Белки: {entry['Белки']:.1f} г | Жиры: {entry['Жиры']:.1f} г")
        st.write(f"Калорийность: {entry['Калорийность (всего)']:.1f} ккал | ХЕ: {entry['ХЕ по углеводам (всего)']:.2f} | БЖЕ: {entry['БЖЕ (всего)']:.2f} | 💠 Общая ХЕ: {entry['Общая ХЕ (всего)']:.2f}")
        st.markdown("---")
else:
    st.info("История пока пуста.")

st.caption("📘 Формулы: 10 г углеводов = 1 ХE | 100 ккал от белков и жиров = 1 БЖЕ")
st.caption("1 г белка = 4 ккал | 1 г жира = 9 ккал")