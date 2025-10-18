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

# --- Поля ввода ---
carbs = st.number_input("Углеводы (г):", min_value=0.0, step=1.0, placeholder="Введите количество")
protein = st.number_input("Белки (г):", min_value=0.0, step=1.0, placeholder="Введите количество")
fat = st.number_input("Жиры (г):", min_value=0.0, step=1.0, placeholder="Введите количество")

# --- Кнопки ---
col1, col2 = st.columns(2)

with col1:
    calculate = st.button("Рассчитать ХЕ", use_container_width=True, type="primary")
with col2:
    reset = st.button("Сбросить", use_container_width=True)

# --- Логика ---
if reset:
   st.rerun(scope="app")


if calculate:
    # Расчёт калорийности
    calories = (carbs * 4) + (protein * 4) + (fat * 9)
    xe_carbs = carbs / 10
    xe_calories = calories / 100
    xe_total = xe_carbs + xe_calories

    st.success("✅ Результаты расчёта:")
    st.metric("Общая калорийность", f"{calories:.1f} ккал")
    st.metric("ХЕ по углеводам", f"{xe_carbs:.2f}")
    st.metric("ХЕ по калорийности", f"{xe_calories:.2f}")
    st.metric("💠 Общая сумма ХЕ", f"{xe_total:.2f}")

# --- Подпись ---
st.markdown("---")
st.caption("📘 Формулы: 10 г углеводов = 1 ХE | 100 ккал = 1 ХЕ")
st.caption("1 г белка = 4 ккал | 1 г жира = 9 ккал")
st.caption("Разработано с ❤️ с помощью Streamlit")
