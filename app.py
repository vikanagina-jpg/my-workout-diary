import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# Настройка страницы под мобильные телефоны
st.set_page_config(page_title="Дневник тренировок", page_icon="🎀", layout="wide")

# ============================================================
# 🎀 РОЗОВЫЙ ДИЗАЙН (только оформление, логика ниже не тронута)
# ============================================================
PINK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@500;700;800&family=Pacifico&display=swap');

:root {
    --bg: #FFF0F6;
    --card: #FFFFFF;
    --pink-soft: #FFD9E8;
    --pink-mid: #FF9EC4;
    --pink-main: #F0568F;
    --pink-deep: #C2306C;
    --text: #5A1B3A;
}

html, body, [class*="css"], .stApp, .stMarkdown, label, p, span, div {
    font-family: 'Nunito', 'Segoe UI', Arial, sans-serif;
}

/* Фон приложения: нежный розовый с лёгкими сердечками-пятнами */
.stApp {
    background:
        radial-gradient(circle at 12% 8%, #FFE0EE 0, transparent 38%),
        radial-gradient(circle at 92% 30%, #FFE8F2 0, transparent 34%),
        var(--bg);
    color: var(--text);
}

/* Убираем лишнее у Streamlit и ограничиваем ширину для удобного чтения */
header[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }
.block-container {
    max-width: 760px !important;
    padding: 1rem 0.9rem 3rem 0.9rem !important;
}

/* Шапка с котиком */
.cat-header {
    display: flex; align-items: center; gap: 14px;
    background: linear-gradient(135deg, #FFC2DA 0%, #FF9EC4 100%);
    border-radius: 26px;
    padding: 14px 18px;
    margin: 4px 0 18px 0;
    box-shadow: 0 8px 20px rgba(240, 86, 143, 0.25);
    border: 3px solid #FFFFFF;
}
.cat-header svg { flex: 0 0 auto; width: 84px; height: 76px; }
.cat-header .title {
    font-family: 'Pacifico', cursive;
    font-size: 26px; line-height: 1.15;
    color: #FFFFFF;
    text-shadow: 0 2px 0 rgba(194, 48, 108, 0.45);
}
.cat-header .subtitle {
    font-size: 14px; font-weight: 700; color: #7A1F48; margin-top: 4px;
}

/* Подзаголовки */
h2, h3, [data-testid="stHeading"] h3 {
    color: var(--pink-deep) !important;
    font-weight: 800 !important;
}

/* Вкладки: большие розовые «таблетки», удобно нажимать пальцем */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px; background: transparent; border-bottom: none;
}
.stTabs [data-baseweb="tab"] {
    flex: 1 1 0;
    height: 48px;
    justify-content: center;
    background: #FFFFFF;
    border: 2px solid var(--pink-soft);
    border-radius: 16px;
    color: var(--pink-deep);
    font-weight: 800;
}
.stTabs [data-baseweb="tab"] p { font-size: 15px; font-weight: 800; }
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FF8DBA, #F0568F) !important;
    border-color: #F0568F !important;
}
.stTabs [aria-selected="true"] p { color: #FFFFFF !important; }
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none; }

/* Форма добавления — как розовая карточка */
[data-testid="stForm"] {
    background: var(--card);
    border: 2px solid var(--pink-soft);
    border-radius: 24px;
    padding: 18px 16px;
    box-shadow: 0 8px 22px rgba(240, 86, 143, 0.12);
}

/* Подписи к полям */
label, [data-testid="stWidgetLabel"] p {
    color: var(--text) !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

/* Поля ввода: крупный шрифт (на iPhone нет авто-зума) и скруглённые углы */
input, textarea, [data-baseweb="select"] div {
    font-size: 16px !important;
}
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="select"] > div {
    background-color: #FFF8FB !important;
    border-radius: 14px !important;
    border-color: var(--pink-soft) !important;
}
[data-baseweb="input"]:focus-within, [data-baseweb="select"] > div:focus-within {
    border-color: var(--pink-main) !important;
    box-shadow: 0 0 0 3px rgba(240, 86, 143, 0.2) !important;
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
    border: 2px solid var(--pink-main) !important;
    transition: transform 0.1s ease;
}
.stButton > button:active, .stDownloadButton > button:active,
[data-testid="stFormSubmitButton"] > button:active { transform: scale(0.97); }

/* Главная кнопка «Записать» */
button[kind="primary"], button[kind="primaryFormSubmit"] {
    background: linear-gradient(135deg, #FF8DBA, #F0568F) !important;
    color: #FFFFFF !important;
    box-shadow: 0 6px 16px rgba(240, 86, 143, 0.35);
}
/* Второстепенные кнопки */
button[kind="secondary"], .stDownloadButton > button {
    background: #FFFFFF !important;
    color: var(--pink-deep) !important;
}

/* Сообщения */
[data-testid="stAlert"] {
    border-radius: 16px;
    border: 2px solid var(--pink-soft);
    background: #FFFFFF;
    color: var(--text);
}

/* Разделители */
hr { border-color: var(--pink-soft) !important; }
</style>
"""
st.markdown(PINK_CSS, unsafe_allow_html=True)

# Шапка: котик с бантиком (рисунок встроен прямо в код, интернет не нужен)
CAT_HEADER = (
    '<div class="cat-header">'
    '<svg viewBox="0 0 120 110" xmlns="http://www.w3.org/2000/svg">'
    '<polygon points="16,44 20,6 54,28" fill="#FFF7FA" stroke="#7A1F48" stroke-width="3" stroke-linejoin="round"/>'
    '<polygon points="104,44 100,6 66,28" fill="#FFF7FA" stroke="#7A1F48" stroke-width="3" stroke-linejoin="round"/>'
    '<polygon points="25,36 27,17 44,29" fill="#FFB6D2"/>'
    '<polygon points="95,36 93,17 76,29" fill="#FFB6D2"/>'
    '<ellipse cx="60" cy="66" rx="46" ry="38" fill="#FFF7FA" stroke="#7A1F48" stroke-width="3"/>'
    '<circle cx="42" cy="64" r="5.5" fill="#5A1B3A"/><circle cx="78" cy="64" r="5.5" fill="#5A1B3A"/>'
    '<circle cx="44" cy="62" r="1.8" fill="#FFFFFF"/><circle cx="80" cy="62" r="1.8" fill="#FFFFFF"/>'
    '<ellipse cx="31" cy="76" rx="7" ry="4.5" fill="#FF9EC4" opacity="0.65"/>'
    '<ellipse cx="89" cy="76" rx="7" ry="4.5" fill="#FF9EC4" opacity="0.65"/>'
    '<polygon points="55,73 65,73 60,79" fill="#F0568F"/>'
    '<path d="M60 79 q-4 7 -10 3 M60 79 q4 7 10 3" fill="none" stroke="#7A1F48" stroke-width="2.5" stroke-linecap="round"/>'
    '<path d="M10 66 l20 4 M10 78 l20 -3 M110 66 l-20 4 M110 78 l-20 -3" stroke="#7A1F48" stroke-width="2" stroke-linecap="round"/>'
    '<polygon points="88,18 68,8 68,28" fill="#F0568F" stroke="#C2306C" stroke-width="2" stroke-linejoin="round"/>'
    '<polygon points="88,18 108,8 108,28" fill="#F0568F" stroke="#C2306C" stroke-width="2" stroke-linejoin="round"/>'
    '<circle cx="88" cy="18" r="5.5" fill="#FF9EC4" stroke="#C2306C" stroke-width="2"/>'
    '</svg>'
    '<div><div class="title">Мой Блокнот Тренировок</div>'
    '<div class="subtitle">Каждый подход делает тебя сильнее 🎀</div></div>'
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

st.markdown(CAT_HEADER, unsafe_allow_html=True)

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
            custom_table_html = f"""<div style="overflow-x: auto; max-width: 100%; border: 2px solid #FFC2DA; border-radius: 20px; background: #FFFFFF; box-shadow: 0 8px 22px rgba(240, 86, 143, 0.15);">
<style>
.workout-table {{ width: 100%; border-collapse: separate; border-spacing: 0; font-family: 'Nunito', sans-serif; font-size: 15px; color: #5A1B3A; }}
.workout-table th {{ background: linear-gradient(135deg, #FF9EC4, #F0568F); color: #FFFFFF; padding: 12px 12px; font-weight: 800; text-align: left; white-space: nowrap; border-bottom: 2px solid #FFFFFF; }}
.workout-table td {{ padding: 12px 12px; border-bottom: 1px solid #FFE0EE; text-align: left; vertical-align: top; line-height: 1.5; white-space: nowrap; }}
.workout-table tbody tr:nth-child(even) td {{ background-color: #FFF5F9; }}
.workout-table tbody tr:last-child td {{ border-bottom: none; }}
.workout-table th:first-child, .workout-table td:first-child {{
    position: sticky; left: 0; background-color: #FFE8F2; font-weight: 800; z-index: 2; border-right: 2px solid #FFC2DA; color: #C2306C; white-space: normal; min-width: 110px;
}}
.workout-table th:first-child {{ background: #F0568F; color: #FFFFFF; z-index: 3; }}
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
        st.info("🐱 Таблица пуста. Перейдите на вкладку 'Добавить запись', чтобы внести первые данные.")

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
