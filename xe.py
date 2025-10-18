import streamlit as st
import matplotlib.pyplot as plt

# --- Настройки страницы ---
st.set_page_config(
    page_title="Калькулятор Хлебных Единиц",
    page_icon="https://cdn-icons-png.flaticon.com/512/1046/1046784.png",
    layout="centered"
)

# --- PWA HTML блок ---
st.markdown("""
<link rel="apple-touch-icon" sizes="180x180" href="https://cdn-icons-png.flaticon.com/512/1046/1046784.png">
<link rel="icon" type="image/png" sizes="32x32" href="https://cdn-icons-png.flaticon.com/512/1046/1046784.png">
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#ffffff">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function() {
    navigator.serviceWorker.register("service-worker.js")
    .then(reg => console.log("Service Worker зарегистрирован:", reg.scope))
    .catch(err => console.log("Ошибка регистрации Service Worker:", err));
  });
}
</script>
""", unsafe_allow_html=True)

# --- Инициализация состояния ---
for key in ["carbs", "protein", "fat", "portions", "history"]:
    if key not in st.session_state:
        st.session_state[key] = 0.0 if key in ["carbs", "protein", "fat"] else 1 if key=="portions" else []

# --- Заголовок ---
st.title("🍞 Калькулятор Хлебных Единиц (ХЕ)")
st.write("Введите данные, чтобы рассчитать количество ХЕ и калорийность.")

# --- Функции ---
def reset_fields():
    st.session_state.carbs = 0.0
    st.session_state.protein = 0.0
    st.session_state.fat = 0.0
    st.session_state.portions = 1

def clear_history():
    st.session_state.history = []

# --- Поля ввода с ключами ---
carbs = st.number_input("Углеводы (г):", min_value=0.0, step=1.0, key="carbs")
protein = st.number_input("Белки (г):", min_value=0.0, step=1.0, key="protein")
fat = st.number_input("Жиры (г):", min_value=0.0, step=1.0, key="fat")
portions = st.number_input("Количество порций:", min_value=1, step=1, key="portions")

# --- Кнопки ---
col1, col2 = st.columns(2)
with col1:
    calculate = st.button("Рассчитать ХЕ", use_container_width=True, type="primary")
with col2:
    st.button("Сбросить поля", on_click=reset_fields, use_container_width=True)

# --- Расчёт ---
if calculate:
    # --- Единичные значения ---
    calories_single = carbs*4 + protein*4 + fat*9
    xe_carbs_single = carbs / 10
    bje_single = (protein*4 + fat*9) / 100  # БЖЕ только белки и жиры
    xe_total_single = xe_carbs_single + bje_single

    # --- Общие значения с умножением на количество порций ---
    calories_total = calories_single * portions
    xe_carbs_total = xe_carbs_single * portions
    bje_total = bje_single * portions
    xe_total_total = xe_carbs_total + bje_total

    # --- Значения на порцию ---
    calories_per_portion = calories_total / portions
    xe_carbs_per_portion = xe_carbs_total / portions
    bje_per_portion = bje_total / portions
    xe_total_per_portion = xe_total_total / portions

    # --- Отображение ---
    st.success(f"✅ Общие результаты (для {portions} порций):")
    st.metric("Общая калорийность", f"{calories_total:.1f} ккал")
    st.metric("ХЕ по углеводам", f"{xe_carbs_total:.2f}")
    st.metric("БЖЕ", f"{bje_total:.2f}")
    st.metric("💠 Общая сумма ХЕ", f"{xe_total_total:.2f}")

    st.info("На одну порцию:")
    st.write(f"Калорийность: {calories_per_portion:.1f} ккал")
    st.write(f"ХЕ по углеводам: {xe_carbs_per_portion:.2f}")
    st.write(f"БЖЕ: {bje_per_portion:.2f}")
    st.write(f"💠 Общая ХЕ: {xe_total_per_portion:.2f}")

    # --- История ---
    st.session_state.history.append({
        "Углеводы": carbs,
        "Белки": protein,
        "Жиры": fat,
        "Порции": portions,
        "Калорийность (всего)": calories_total,
        "ХЕ по углеводам (всего)": xe_carbs_total,
        "БЖЕ (всего)": bje_total,
        "Общая ХЕ (всего)": xe_total_total
    })

    # --- Круговая диаграмма ---
    labels = ['ХЕ по углеводам', 'БЖЕ']
    sizes = [xe_total_total, bje_total]
    colors = ['#1E90FF', '#FFA500']  # ХЕ синий, БЖЕ оранжевый
    explode = (0.05, 0.05)

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=explode, shadow=True)
    ax.axis('equal')
    st.pyplot(fig)

# --- Вкладки ---
tab1, tab2 = st.tabs(["📘 Как компенсировать БЖЕ?", "📜 История расчётов"])

with tab1:
    st.markdown("""
    ### 💉 Как компенсировать БЖЕ?
    1 БЖЕ = 1 ХЕ. Дозу нужно растягивать, либо подкалывать через 1–2–3 часа после еды.

    #### ⏳ Как растягивать:
    • 1 БЖЕ — на 3 часа  
    • 2 БЖЕ — на 4 часа  
    • 3 БЖЕ — на 5 часов  
    • Более 4 БЖЕ — от 5 до 10+ часов  

    #### 💡 Если вы на помпе:
    Сложите дозы на ХЕ и БЖЕ, разделите пополам:  
    • 50 % — нормальный болюс перед едой  
    • 50 % — растяните на 4–5 часов  

    #### 💉 Если вы на ручках:
    Сделайте то же самое, но:  
    • 50 % — подколка перед едой  
    • 50 % — через 1.5–3 часа  
    """)

with tab2:
    if st.session_state.history:
        with st.expander("📜 Показать историю последних расчётов", expanded=False):
            st.button("Очистить историю", on_click=clear_history, use_container_width=True)
            for i, entry in enumerate(reversed(st.session_state.history[-5:]), 1):
                st.write(f"**Расчёт {i}:**")
                st.write(f"Углеводы: {entry['Углеводы']} г, Белки: {entry['Белки']} г, Жиры: {entry['Жиры']} г")
                st.write(f"Порции: {entry['Порции']}")
                st.write(f"Калорийность (всего): {entry['Калорийность (всего)']:.1f} ккал")
                st.write(f"ХЕ по углеводам (всего): {entry['ХЕ по углеводам (всего)']:.2f}")
                st.write(f"БЖЕ (всего): {entry['БЖЕ (всего)']:.2f}")
                st.write(f"💠 Общая ХЕ (всего): {entry['Общая ХЕ (всего)']:.2f}")

# --- Подпись ---
st.markdown("---")
st.caption("📘 Формулы: 10 г углеводов = 1 ХE | 100 ккал от белков и жиров = 1 БЖЕ")
st.caption("1 г белка = 4 ккал | 1 г жира = 9 ккал")