import streamlit as st

# --- Настройки страницы ---
st.set_page_config(
    page_title="Калькулятор Хлебных Единиц",
    page_icon="🍞",
    layout="centered"
)

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

# --- Кнопки ---
col1, col2, col3 = st.columns([1,1,1])
with col1:
    calculate = st.button("Рассчитать ХЕ", use_container_width=True, type="primary")
with col2:
    st.button("Сбросить поля", on_click=reset_fields, use_container_width=True)
with col3:
    st.button("Очистить историю", on_click=clear_history, use_container_width=True)

# --- Логика расчёта ---
if calculate:
    calories = (carbs * 4) + (protein * 4) + (fat * 9)
    xe_carbs = carbs / 10
    xe_calories = calories / 100
    xe_total = xe_carbs + xe_calories

    st.success("✅ Результаты расчёта:")
    st.metric("Общая калорийность", f"{calories:.1f} ккал")
    st.metric("ХЕ по углеводам", f"{xe_carbs:.2f}")
    st.metric("ХЕ по калорийности", f"{xe_calories:.2f}")
    st.metric("💠 Общая сумма ХЕ", f"{xe_total:.2f}")

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

# --- История расчётов ---
if st.session_state.history:
    st.markdown("### 📜 История последних расчётов")
    for i, entry in enumerate(reversed(st.session_state.history[-5:]), 1):  # Показываем последние 5
        st.write(f"**Расчёт {i}:**")
        st.write(f"Углеводы: {entry['Углеводы']} г, Белки: {entry['Белки']} г, Жиры: {entry['Жиры']} г")
        st.write(f"Калорийность: {entry['Калорийность']:.1f} ккал")
        st.write(f"ХЕ по углеводам: {entry['ХЕ по углеводам']:.2f}, ХЕ по калорийности: {entry['ХЕ по калорийности']:.2f}")
        st.write(f"💠 Общая ХЕ: {entry['Общая ХЕ']:.2f}")
        st.markdown("---")

# --- Подпись ---
st.markdown("---")
st.caption("📘 Формулы: 10 г углеводов = 1 ХE | 100 ккал = 1 ХЕ")
st.caption("1 г белка = 4 ккал | 1 г жира = 9 ккал")
st.caption("Разработано с ❤️ с помощью Streamlit")

