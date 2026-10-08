import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# Настройка страницы под мобильные телефоны
st.set_page_config(page_title="Дневник тренировок", page_icon="🎃", layout="wide")

# ============================================================
# 🍂 ОСЕННИЙ ДИЗАЙН (только оформление, логика ниже не тронута)
# ============================================================
AUTUMN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@500;700;800&family=Lobster&display=swap');

:root {
    --bg: #FFF1DC;
    --card: #FFFFFF;
    --sand: #FFDDB0;
    --amber: #F5B13C;
    --pumpkin: #EE7A1F;
    --pumpkin-deep: #B8480B;
    --brown: #4A2511;
    --leaf: #6F7F2B;
}

html, body, [class*="css"], .stApp, .stMarkdown, label, p, span, div {
    font-family: 'Nunito', 'Segoe UI', Arial, sans-serif;
}

/* Фон: тёплый закат с пятнами осенних листьев */
.stApp {
    background:
        radial-gradient(circle at 10% 6%, #FFD9A6 0, transparent 36%),
        radial-gradient(circle at 94% 34%, #FFE7C2 0, transparent 34%),
        radial-gradient(circle at 20% 96%, #F9D49A 0, transparent 30%),
        var(--bg);
    color: var(--brown);
}

header[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }
.block-container {
    max-width: 760px !important;
    padding: 1rem 0.9rem 3rem 0.9rem !important;
}

/* Шапка с тыковкой */
.pumpkin-header {
    display: flex; align-items: center; gap: 14px;
    background: linear-gradient(135deg, #7A3B14 0%, #4A2511 100%);
    border-radius: 26px;
    padding: 14px 18px;
    margin: 4px 0 18px 0;
    box-shadow: 0 8px 20px rgba(74, 37, 17, 0.35);
    border: 3px solid #F5B13C;
}
.pumpkin-header svg { flex: 0 0 auto; width: 84px; height: 78px; }
.pumpkin-header .title {
    font-family: 'Lobster', cursive;
    font-size: 27px; line-height: 1.15;
    color: #FFC76B;
    text-shadow: 0 2px 0 rgba(0, 0, 0, 0.35);
}
.pumpkin-header .subtitle {
    font-size: 14px; font-weight: 700; color: #FFE3BC; margin-top: 4px;
}

/* Подзаголовки */
h2, h3, [data-testid="stHeading"] h3 {
    color: var(--pumpkin-deep) !important;
    font-weight: 800 !important;
}

/* Вкладки */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px; background: transparent; border-bottom: none;
}
.stTabs [data-baseweb="tab"] {
    flex: 1 1 0;
    height: 48px;
    justify-content: center;
    background: #FFFFFF;
    border: 2px solid var(--sand);
    border-radius: 16px;
    color: var(--pumpkin-deep);
    font-weight: 800;
}
.stTabs [data-baseweb="tab"] p { font-size: 15px; font-weight: 800; }
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #F5A03A, #E2650F) !important;
    border-color: #E2650F !important;
}
.stTabs [aria-selected="true"] p { color: #FFFFFF !important; }
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none; }

/* Форма добавления */
[data-testid="stForm"] {
    background: var(--card);
    border: 2px solid var(--sand);
    border-radius: 24px;
    padding: 18px 16px;
    box-shadow: 0 8px 22px rgba(184, 72, 11, 0.12);
}

/* Подписи к полям */
label, [data-testid="stWidgetLabel"] p {
    color: var(--brown) !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

/* Поля ввода */
input, textarea, [data-baseweb="select"] div {
    font-size: 16px !important;
}
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="select"] > div {
    background-color: #FFFAF2 !important;
    border-radius: 14px !important;
    border-color: var(--sand) !important;
}
[data-baseweb="input"]:focus-within, [data-baseweb="select"] > div:focus-within {
    border-color: var(--pumpkin) !important;
    box-shadow: 0 0 0 3px rgba(238, 122, 31, 0.25) !important;
}

/* Три колонки (Подходы / Повторы / Вес) остаются в ряд и на телефоне */
[data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 8px !important; }
[data-testid="stColumn"], [data-testid="column"] {
    min-width: 0 !important; flex: 1 1 0 !important; width: auto !important;
}

/* Кнопки */
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
    border-radius: 18px !important;
    min-height: 52px;
    font-weight: 800 !important;
    font-size: 16px !important;
    border: 2px solid var(--pumpkin) !important;
    transition: transform 0.1s ease;
}
.stButton > button:active, .stDownloadButton > button:active,
[data-testid="stFormSubmitButton"] > button:active { transform: scale(0.97); }

/* Главная кнопка «Записать» */
button[kind="primary"], button[kind="primaryFormSubmit"] {
    background: linear-gradient(135deg, #F5A03A, #E2650F) !important;
    color: #FFFFFF !important;
    box-shadow: 0 6px 16px rgba(226, 101, 15, 0.35);
}
/* Второстепенные кнопки */
button[kind="secondary"], .stDownloadButton > button {
    background: #FFFFFF !important;
    color: var(--pumpkin-deep) !important;
}

/* Сообщения */
[data-testid="stAlert"] {
    border-radius: 16px;
    border: 2px solid var(--sand);
    background: #FFFFFF;
    color: var(--brown);
}

hr { border-color: var(--sand) !important; }
</style>
"""
st.markdown(AUTUMN_CSS, unsafe_allow_html=True)

# Шапка: улыбающаяся тыковка с листочком (рисунок встроен в код, интернет не нужен)
PUMPKIN_HEADER = (
    '<div class="pumpkin-header">'
    '<svg viewBox="0 0 120 110" xmlns="http://www.w3.org/2000/svg">'
    '<ellipse cx="34" cy="68" rx="25" ry="33" fill="#E8701A" stroke="#8A3B0B" stroke-width="3"/>'
    '<ellipse cx="86" cy="68" rx="25" ry="33" fill="#E8701A" stroke="#8A3B0B" stroke-width="3"/>'
    '<ellipse cx="48" cy="68" rx="25" ry="36" fill="#F28A25" stroke="#8A3B0B" stroke-width="3"/>'
    '<ellipse cx="72" cy="68" rx="25" ry="36" fill="#F28A25" stroke="#8A3B0B" stroke-width="3"/>'
    '<ellipse cx="60" cy="68" rx="20" ry="38" fill="#FF9A33" stroke="#8A3B0B" stroke-width="3"/>'
    '<path d="M42 40 q-6 28 0 56 M78 40 q6 28 0 56" fill="none" stroke="#C4580F" stroke-width="2" stroke-linecap="round" opacity="0.7"/>'
    '<polygon points="40,58 50,58 45,50" fill="#4A2511"/>'
    '<polygon points="70,58 80,58 75,50" fill="#4A2511"/>'
    '<path d="M42 76 q18 20 36 0" fill="#4A2511" stroke="#4A2511" stroke-width="3" stroke-linejoin="round"/>'
    '<path d="M50 80 l4 -3 l4 3 l4 -3 l4 3 l4 -3" fill="none" stroke="#FFD25A" stroke-width="2.5" stroke-linejoin="round"/>'
    '<ellipse cx="33" cy="72" rx="6" ry="4" fill="#FF6B3A" opacity="0.55"/>'
    '<ellipse cx="87" cy="72" rx="6" ry="4" fill="#FF6B3A" opacity="0.55"/>'
    '<path d="M58 32 q-2 -14 8 -22 q4 -2 5 3 q-2 6 -4 10 q-2 6 -4 10 z" fill="#6B4423" stroke="#3E2410" stroke-width="2.5" stroke-linejoin="round"/>'
    '<path d="M64 24 q16 -16 30 -8 q-4 16 -26 14 z" fill="#7C8F2E" stroke="#4D5C18" stroke-width="2.5" stroke-linejoin="round"/>'
    '<path d="M66 26 q12 -6 22 -8" fill="none" stroke="#4D5C18" stroke-width="2" stroke-linecap="round"/>'
    '<path d="M62 22 q-14 -18 -26 -10" fill="none" stroke="#6F7F2B" stroke-width="3" stroke-linecap="round"/>'
    '</svg>'
    '<div><div class="title">Мой Блокнот Тренировок</div>'
    '<div class="subtitle">Тёплая осень, крепкие мышцы 🍂</div></div>'
    '</div>'
)

# Имя файла для персистентного хранения данных в облаке
DATA_FILE = "workout_diary_storage.csv"

# Логика загрузки данных
if "workout_db" not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state.workout_db = pd.read_csv(DATA_FILE, dtype={"Дата": str, "Упражнение": str, "Результат": str})
    else:
        st.session_state.workout_db = pd.DataFrame(columns=["Дата", "Упражнение", "Результат"])

# Принудительно чистим базу от старых американских искажений дат "8.1"
if not st.session_state.workout_db.empty:
    st.session_state.workout_db["Дата"] = st.session_state.workout_db["Дата"].astype(str).replace("8.1", "08.10")

df = st.session_state.workout_db

st.markdown(PUMPKIN_HEADER, unsafe_allow_html=True)

# Вкладки приложения
tab_view, tab_add = st.tabs(["📋 Таблица тренировок", "➕ Добавить запись"])

# --- ВКЛАДКА 1: ОТОБРАЖЕНИЕ ТАБЛИЦЫ ---
with tab_view:
    st.subheader("Журнал по дням")
    
    if not df.empty:
        try:
            df_view = df.copy()
            df_view["Дата"] = df_view["Дата"].astype(str)
            df_view["Упражнение"] = df_view["Упражнение"].astype(str)
            df_view["Результат"] = df_view["Результат"].astype(str)
            
            # Объединение подходов через HTML-тег <br> для гарантированного переноса строки внутри ячейки
            grouped = df_view.groupby(["Упражнение", "Дата"])["Результат"].apply(lambda x: "<br>".join(x)).reset_index()
            
            # Превращаем в кросс-таблицу "Упражнение | Дата1 | Дата2..."
            pivot_df = grouped.pivot(index="Упражнение", columns="Дата", values="Результат").reset_index()
            
            # ИСПРАВЛЕНИЕ: Удаляем слово "Дата" над левым верхним углом таблицы
            pivot_df.columns.name = None
            
            # Сортируем даты по порядку (новые будут добавляться справа)
            date_cols = sorted([col for col in pivot_df.columns if col != "Упражнение"])
            final_cols = ["Упражнение"] + date_cols
            pivot_df = pivot_df[final_cols]
            
            # Заменяем пустоты на прочерки
            pivot_df = pivot_df.fillna("—")
            
            # Строим чистую HTML таблицу без технических индексов 0 и 1
            html_raw = pivot_df.to_html(index=False, escape=False)
            
            # CSS-стили для красивого отображения и закрепления первого столбца на телефоне
            # (строки HTML без отступов, чтобы Markdown не принял их за блок кода)
            custom_table_html = f"""<div style="overflow-x: auto; max-width: 100%; border: 2px solid #FFDDB0; border-radius: 20px; background: #FFFFFF; box-shadow: 0 8px 22px rgba(184, 72, 11, 0.15);">
<style>
.workout-table {{ width: 100%; border-collapse: separate; border-spacing: 0; font-family: 'Nunito', sans-serif; font-size: 15px; color: #4A2511; }}
.workout-table th {{ background: linear-gradient(135deg, #F5A03A, #D9600C); color: #FFFFFF; padding: 12px 12px; font-weight: 800; text-align: left; white-space: nowrap; border-bottom: 2px solid #FFFFFF; }}
.workout-table td {{ padding: 12px 12px; border-bottom: 1px solid #FFE9CC; text-align: left; vertical-align: top; line-height: 1.5; white-space: nowrap; }}
.workout-table tbody tr:nth-child(even) td {{ background-color: #FFF7EA; }}
.workout-table tbody tr:last-child td {{ border-bottom: none; }}
.workout-table th:first-child, .workout-table td:first-child {{
    position: sticky; left: 0; background-color: #FFEBD0; font-weight: 800; z-index: 2; border-right: 2px solid #FFDDB0; color: #B8480B; white-space: normal; min-width: 110px;
}}
.workout-table th:first-child {{ background: #B8480B; color: #FFFFFF; z-index: 3; }}
</style>
{html_raw.replace('class="dataframe"', 'class="workout-table"')}
</div>"""
            
            # Выводим готовую таблицу на экран телефона
            st.write(custom_table_html, unsafe_allow_html=True)
            
            st.write("---")
            
            # КНОПКА СКАЧИВАНИЯ ТАБЛИЦЫ В EXCEL (внутри Excel переносы тоже будут работать через \n)
            excel_pivot = pivot_df.copy()
            for col in date_cols:
                excel_pivot[col] = excel_pivot[col].str.replace("<br>", "\n")
                
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                excel_pivot.to_excel(writer, index=False, sheet_name='Тренировки')
            
            st.download_button(
                label="📥 Скачать таблицу в Excel",
                data=buffer.getvalue(),
                file_name=f"workout_report_{datetime.now().strftime('%d_%m_%Y')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"Ошибка при сборке таблицы: {e}")
            st.dataframe(df)
            
        st.write("") 
        if st.button("❌ Удалить самую последнюю запись", type="secondary", use_container_width=True):
            if not df.empty:
                st.session_state.workout_db = df.drop(df.index[-1]).reset_index(drop=True)
                st.session_state.workout_db.to_csv(DATA_FILE, index=False)
                st.rerun()
    else:
        st.info("🎃 Таблица пуста. Перейдите на вкладку 'Добавить запись', чтобы внести первые данные.")

# --- ВКЛАДКА 2: ВВОД ДАННЫХ С ТЕЛЕФОНА ---
with tab_add:
    st.subheader("Новый подход / упражнение")
    
    with st.form("add_form", clear_on_submit=True):
        date_input = st.date_input("Дата тренировки", datetime.now())
        date_str = date_input.strftime("%d.%m") 
        
        existing_exercises = sorted(df["Упражнение"].unique().tolist()) if not df.empty else []
        
        exercise = st.selectbox(
            "Начните вводить или выберите упражнение:",
            options=[""] + existing_exercises,
            index=0
        )
        
        custom_exercise = st.text_input("ИЛИ введите НОВОЕ упражнение:", placeholder="Например: Жим лежа")
        
        st.write("---")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            sets = st.number_input("Подходы", min_value=1, value=3, step=1)
        with col2:
            reps = st.number_input("Повторы", min_value=1, value=8, step=1)
        with col3:
            weight = st.number_input("Вес (кг)", min_value=0.0, value=0.0, step=0.5)
            
        comment = st.selectbox("Примечание (необязательно)", ["", "разминка", "рабочий вес"])
        
        submit_btn = st.form_submit_button("💾 Записать в таблицу", use_container_width=True, type="primary")
        
        if submit_btn:
            final_exercise = custom_exercise.strip() if custom_exercise.strip() else exercise
            
            if not final_exercise:
                st.error("Пожалуйста, выберите или введите упражнение!")
            else:
                weight_str = f"{int(weight)}" if weight.is_integer() else f"{weight}"
                res_string = f"{sets}/{reps} {weight_str}"
                if comment:
                    res_string += f" ({comment})"
                
                new_row = pd.DataFrame([[str(date_str), str(final_exercise), str(res_string)]], columns=["Дата", "Упражнение", "Результат"])
                st.session_state.workout_db = pd.concat([st.session_state.workout_db, new_row], ignore_index=True)
                st.session_state.workout_db.to_csv(DATA_FILE, index=False)
                
                st.success(f"Добавлено: {final_exercise} -> {res_string}")
                st.rerun()
