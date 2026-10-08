import streamlit as st
import pandas as pd
from datetime import datetime
import html
import io
import os

# Настройка страницы под мобильные телефоны
st.set_page_config(
    page_title="Дневник тренировок",
    page_icon="🎃",
    layout="wide"
)

# ============================================================
# 🍂 ОСЕННИЙ ДИЗАЙН
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

.pumpkin-header {
    display: flex;
    align-items: center;
    gap: 14px;
    background: linear-gradient(135deg, #7A3B14 0%, #4A2511 100%);
    border-radius: 26px;
    padding: 14px 18px;
    margin: 4px 0 18px 0;
    box-shadow: 0 8px 20px rgba(74, 37, 17, 0.35);
    border: 3px solid #F5B13C;
}

.pumpkin-header svg {
    flex: 0 0 auto;
    width: 84px;
    height: 78px;
}

.pumpkin-header .title {
    font-family: 'Lobster', cursive;
    font-size: 27px;
    line-height: 1.15;
    color: #FFC76B;
    text-shadow: 0 2px 0 rgba(0, 0, 0, 0.35);
}

.pumpkin-header .subtitle {
    font-size: 14px;
    font-weight: 700;
    color: #FFE3BC;
    margin-top: 4px;
}

h2, h3, [data-testid="stHeading"] h3 {
    color: var(--pumpkin-deep) !important;
    font-weight: 800 !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
    border-bottom: none;
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

.stTabs [data-baseweb="tab"] p {
    font-size: 15px;
    font-weight: 800;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #F5A03A, #E2650F) !important;
    border-color: #E2650F !important;
}

.stTabs [aria-selected="true"] p { color: #FFFFFF !important; }

.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none; }

[data-testid="stRadio"] [role="radiogroup"] {
    gap: 8px;
    flex-wrap: wrap;
}

[data-testid="stRadio"] label {
    background: #FFFFFF;
    border: 2px solid var(--sand);
    border-radius: 14px;
    padding: 8px 14px;
    margin: 0 !important;
}

[data-testid="stRadio"] label > div:first-child { display: none; }

[data-testid="stRadio"] label p {
    font-weight: 800;
    color: var(--pumpkin-deep);
}

[data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg, #F5A03A, #E2650F);
    border-color: #E2650F;
}

[data-testid="stRadio"] label:has(input:checked) p {
    color: #FFFFFF !important;
}

[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 2px solid var(--sand) !important;
    border-radius: 18px !important;
    margin-bottom: 8px;
    overflow: hidden;
}

[data-testid="stExpander"] summary { padding: 12px 14px; }

[data-testid="stExpander"] summary p {
    font-weight: 800;
    font-size: 16px;
    color: var(--pumpkin-deep);
}

.grp {
    background: #FFF8EC;
    border: 2px solid var(--sand);
    border-radius: 16px;
    padding: 10px 12px 8px 12px;
    margin-bottom: 10px;
}

.grp-title {
    font-weight: 800;
    font-size: 16px;
    color: var(--pumpkin-deep);
    margin-bottom: 8px;
}

.result-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #FFE6C4;
    color: var(--brown);
    border-radius: 12px;
    padding: 7px 9px;
    margin: 0 5px 5px 0;
    font-weight: 700;
    font-size: 14px;
}

.delete-row {
    display: flex;
    align-items: center;
    background: #FFE6C4;
    border-radius: 12px;
    min-height: 44px;
    padding-left: 12px;
}

[data-testid="stForm"] {
    background: var(--card);
    border: 2px solid var(--sand);
    border-radius: 24px;
    padding: 18px 16px;
    box-shadow: 0 8px 22px rgba(184, 72, 11, 0.12);
}

label,
[data-testid="stWidgetLabel"] p {
    color: var(--brown) !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

input,
textarea,
[data-baseweb="select"] div { font-size: 16px !important; }

[data-baseweb="input"],
[data-baseweb="base-input"],
[data-baseweb="select"] > div {
    background-color: #FFFAF2 !important;
    border-radius: 14px !important;
    border-color: var(--sand) !important;
}

[data-baseweb="input"]:focus-within,
[data-baseweb="select"] > div:focus-within {
    border-color: var(--pumpkin) !important;
    box-shadow: 0 0 0 3px rgba(238, 122, 31, 0.25) !important;
}

[data-testid="stHorizontalBlock"] { gap: 8px !important; }

[data-testid="stColumn"],
[data-testid="column"] { min-width: 0 !important; }

.stButton > button,
.stDownloadButton > button,
[data-testid="stFormSubmitButton"] > button {
    border-radius: 18px !important;
    min-height: 48px;
    font-weight: 800 !important;
    font-size: 16px !important;
    border: 2px solid var(--pumpkin) !important;
    transition: transform 0.1s ease;
}

.stButton > button:active,
.stDownloadButton > button:active,
[data-testid="stFormSubmitButton"] > button:active {
    transform: scale(0.97);
}

button[kind="primary"],
button[kind="primaryFormSubmit"] {
    background: linear-gradient(135deg, #F5A03A, #E2650F) !important;
    color: #FFFFFF !important;
    box-shadow: 0 6px 16px rgba(226, 101, 15, 0.35);
}

button[kind="secondary"],
.stDownloadButton > button {
    background: #FFFFFF !important;
    color: var(--pumpkin-deep) !important;
}

.delete-button button {
    min-height: 42px !important;
    width: 42px !important;
    padding: 0 !important;
    border-radius: 12px !important;
}

[data-testid="stAlert"] {
    border-radius: 16px;
    border: 2px solid var(--sand);
    background: #FFFFFF;
    color: var(--brown);
}

hr { border-color: var(--sand) !important; }

@media (max-width: 600px) {
    .block-container {
        padding-left: 0.55rem !important;
        padding-right: 0.55rem !important;
    }
    .pumpkin-header { padding: 10px 12px; border-radius: 20px; gap: 9px; }
    .pumpkin-header svg { width: 64px; height: 62px; }
    .pumpkin-header .title { font-size: 22px; }
    .pumpkin-header .subtitle { font-size: 12px; }
    .stTabs [data-baseweb="tab"] { height: 44px; }
    .stTabs [data-baseweb="tab"] p { font-size: 13px; }
    [data-testid="stRadio"] label { padding: 7px 9px; }
    [data-testid="stRadio"] label p { font-size: 13px !important; }
    .grp { padding: 9px 9px 6px 9px; }
    .grp-title { font-size: 15px; }
    .result-chip { font-size: 13px; padding: 7px 8px; }
    [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; }
}
</style>
"""

st.markdown(AUTUMN_CSS, unsafe_allow_html=True)


# ============================================================
# 🎃 ШАПКА
# ============================================================

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
    '<div>'
    '<div class="title">Мой Блокнот Тренировок</div>'
    '<div class="subtitle">Мама может всё, а сильная мама – ещё больше! 🍂</div>'
    '</div>'
    '</div>'
)

st.markdown(PUMPKIN_HEADER, unsafe_allow_html=True)


# ============================================================
# 💾 ХРАНЕНИЕ
# ============================================================

DATA_FILE = "workout_diary_storage.csv"

if "workout_db" not in st.session_state:
    if os.path.exists(DATA_FILE):
        try:
            st.session_state.workout_db = pd.read_csv(
                DATA_FILE,
                dtype={"Дата": str, "Упражнение": str, "Результат": str}
            )
        except Exception:
            st.session_state.workout_db = pd.DataFrame(
                columns=["Дата", "Упражнение", "Результат"]
            )
    else:
        st.session_state.workout_db = pd.DataFrame(
            columns=["Дата", "Упражнение", "Результат"]
        )

if not st.session_state.workout_db.empty:
    st.session_state.workout_db["Дата"] = (
        st.session_state.workout_db["Дата"].astype(str).replace("8.1", "08.10")
    )
    st.session_state.workout_db["Упражнение"] = (
        st.session_state.workout_db["Упражнение"].astype(str)
    )
    st.session_state.workout_db["Результат"] = (
        st.session_state.workout_db["Результат"].astype(str)
    )


# ============================================================
# 🔧 ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def date_key(d):
    """Ключ сортировки для дат вида ДД.ММ."""
    try:
        day, month = str(d).split(".")[:2]
        return (int(month), int(day))
    except Exception:
        return (0, 0)


def save_database():
    """Сохраняет текущую базу."""
    st.session_state.workout_db.to_csv(DATA_FILE, index=False)


def delete_record(index):
    """Удаляет запись по её текущему индексу."""
    db = st.session_state.workout_db.copy()
    if index < 0 or index >= len(db):
        return
    deleted_row = db.iloc[index].copy()
    st.session_state.last_deleted = {
        "index": index,
        "row": deleted_row.to_dict()
    }
    st.session_state.workout_db = db.drop(db.index[index]).reset_index(drop=True)
    save_database()


def undo_delete():
    """Возвращает последнюю удалённую запись."""
    saved = st.session_state.get("last_deleted")
    if not saved:
        return
    db = st.session_state.workout_db.copy()
    index = saved["index"]
    row = saved["row"]
    index = min(index, len(db))
    restored_row = pd.DataFrame([row])
    st.session_state.workout_db = pd.concat(
        [db.iloc[:index], restored_row, db.iloc[index:]],
        ignore_index=True
    )
    save_database()
    st.session_state.last_deleted = None


def render_groups(sub, group_col, view_key, delete_mode=False):
    """Показывает упражнения компактными карточками."""
    for name, grp in sub.groupby(group_col, sort=False):
        title = html.escape(str(name))

        if not delete_mode:
            chips = ""
            for result in grp["Результат"]:
                chips += (
                    f'<span class="result-chip">'
                    f'{html.escape(str(result))}'
                    f'</span>'
                )
            st.markdown(
                f'<div class="grp">'
                f'<div class="grp-title">{title}</div>'
                f'<div>{chips}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            with st.container():
                st.markdown(
                    f'<div class="grp">'
                    f'<div class="grp-title">{title}</div>',
                    unsafe_allow_html=True
                )
                for idx in grp.index:
                    result = grp.loc[idx, "Результат"]
                    c1, c2 = st.columns([6, 1], vertical_alignment="center")
                    with c1:
                        st.markdown(
                            f'<div class="delete-row">'
                            f'{html.escape(str(result))}'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    with c2:
                        st.markdown(
                            '<div class="delete-button">',
                            unsafe_allow_html=True
                        )
                        st.button(
                            "🗑️",
                            key=f"delete_{view_key}_{idx}",
                            on_click=delete_record,
                            args=(idx,),
                            use_container_width=True
                        )
                        st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)


def build_pivot(data):
    """Собирает кросс-таблицу Упражнение | Дата1 | Дата2…"""
    df_view = data.copy()
    df_view["Дата"] = df_view["Дата"].astype(str)
    df_view["Упражнение"] = df_view["Упражнение"].astype(str)
    df_view["Результат"] = df_view["Результат"].astype(str)

    grouped = (
        df_view
        .groupby(["Упражнение", "Дата"])["Результат"]
        .apply(lambda x: "<br>".join(x))
        .reset_index()
    )

    pivot = (
        grouped
        .pivot(index="Упражнение", columns="Дата", values="Результат")
        .reset_index()
    )
    pivot.columns.name = None

    cols = sorted(
        [c for c in pivot.columns if c != "Упражнение"],
        key=date_key
    )
    pivot = pivot[["Упражнение"] + cols]
    pivot = pivot.fillna("—")
    return pivot, cols


# ============================================================
# 📌 АКТУАЛЬНАЯ БАЗА
# ============================================================

df = st.session_state.workout_db


# ============================================================
# ВКЛАДКИ
# ============================================================

tab_view, tab_add = st.tabs(["📋 Тренировки", "➕ Добавить запись"])


# ============================================================
# 📋 ВКЛАДКА ТРЕНИРОВОК
# ============================================================

with tab_view:

    # Отмена последнего удаления
    last = st.session_state.get("last_deleted")
    if last:
        row = last["row"]
        st.button(
            f"↩️ Вернуть удалённое: {row['Упражнение']} · {row['Результат']}",
            on_click=undo_delete,
            use_container_width=True,
            key="undo_delete_button"
        )

    if df.empty:
        st.info(
            "🎃 Записей нет. Перейдите на вкладку "
            "'Добавить запись', чтобы внести первые данные."
        )
    else:
        view_mode = st.radio(
            "Вид",
            ["📅 Дни", "💪 Упражнения", "📊 Таблица"],
            horizontal=True,
            label_visibility="collapsed",
            key="view_mode_radio"
        )

        if view_mode != "📊 Таблица":
            delete_mode = st.toggle(
                "🗑 Режим удаления (появятся кнопки у каждой записи)",
                key="delete_mode_toggle"
            )
        else:
            delete_mode = False

        # ---- ВИД 1: ПО ДНЯМ ----
        if view_mode == "📅 Дни":
            st.subheader("Журнал по дням")
            dates = sorted(
                df["Дата"].unique().tolist(),
                key=date_key,
                reverse=True
            )
            for i, d in enumerate(dates):
                sub = df[df["Дата"] == d]
                n = sub["Упражнение"].nunique()
                with st.expander(
                    f"📅 {d} · упражнений: {n}",
                    expanded=(i == 0)
                ):
                    render_groups(sub, "Упражнение", f"d{d}", delete_mode)

        # ---- ВИД 2: ПО УПРАЖНЕНИЯМ ----
        elif view_mode == "💪 Упражнения":
            st.subheader("История упражнения")
            exercises = sorted(df["Упражнение"].unique().tolist())
            chosen = st.selectbox(
                "Выберите упражнение",
                exercises,
                key="exercise_select"
            )
            sub = df[df["Упражнение"] == chosen].copy()
            sub["_k"] = sub["Дата"].map(date_key)
            sub = sub.sort_values("_k", ascending=False, kind="stable")
            st.caption(f"Дней с этим упражнением: {sub['Дата'].nunique()}")
            render_groups(sub, "Дата", "ex", delete_mode)

        # ---- ВИД 3: ОБЩАЯ ТАБЛИЦА ----
        elif view_mode == "📊 Таблица":
            st.subheader("Общая таблица")
            st.caption(
                "Чтобы удалить запись, откройте вид "
                "«Дни» или «Упражнения» и включите режим удаления."
            )

            try:
                pivot_df, date_cols = build_pivot(df)

                html_raw = pivot_df.to_html(index=False, escape=False)

                custom_table_html = (
                    '<div style="overflow-x: auto; max-width: 100%; '
                    'border: 2px solid #FFDDB0; border-radius: 20px; '
                    'background: #FFFFFF; '
                    'box-shadow: 0 8px 22px rgba(184, 72, 11, 0.15);">'
                    '<style>'
                    '.workout-table { width: 100%; border-collapse: separate; '
                    'border-spacing: 0; font-family: Nunito, sans-serif; '
                    'font-size: 15px; color: #4A2511; }'
                    '.workout-table th { background: linear-gradient(135deg, #F5A03A, #D9600C); '
                    'color: #FFFFFF; padding: 12px 12px; font-weight: 800; '
                    'text-align: left; white-space: nowrap; '
                    'border-bottom: 2px solid #FFFFFF; }'
                    '.workout-table td { padding: 12px 12px; '
                    'border-bottom: 1px solid #FFE9CC; text-align: left; '
                    'vertical-align: top; line-height: 1.5; white-space: nowrap; }'
                    '.workout-table tbody tr:nth-child(even) td { background-color: #FFF7EA; }'
                    '.workout-table tbody tr:last-child td { border-bottom: none; }'
                    '.workout-table th:first-child, .workout-table td:first-child { '
                    'position: sticky; left: 0; background-color: #FFEBD0; '
                    'font-weight: 800; z-index: 2; '
                    'border-right: 2px solid #FFDDB0; color: #B8480B; '
                    'white-space: normal; min-width: 110px; }'
                    '.workout-table th:first-child { background: #B8480B; '
                    'color: #FFFFFF; z-index: 3; }'
                    '</style>'
                    + html_raw.replace('class="dataframe"', 'class="workout-table"')
                    + '</div>'
                )

                st.write(custom_table_html, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Ошибка при сборке таблицы: {e}")
                st.dataframe(df)
                pivot_df = None
                date_cols = []

            # Скачивание в Excel
            if pivot_df is not None:
                st.write("---")
                excel_pivot = pivot_df.copy()
                for col in date_cols:
                    excel_pivot[col] = excel_pivot[col].str.replace("<br>", "\n")

                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    excel_pivot.to_excel(
                        writer,
                        index=False,
                        sheet_name='Тренировки'
                    )

                st.download_button(
                    label="📥 Скачать таблицу в Excel",
                    data=buffer.getvalue(),
                    file_name=(
                        f"workout_report_"
                        f"{datetime.now().strftime('%d_%m_%Y')}.xlsx"
                    ),
                    mime=(
                        "application/vnd.openxmlformats-"
                        "officedocument.spreadsheetml.sheet"
                    ),
                    use_container_width=True,
                    key="download_excel_button"
                )


# ============================================================
# ➕ ВКЛАДКА ДОБАВЛЕНИЯ
# ============================================================

with tab_add:

    st.subheader("Новый подход / упражнение")

    with st.form("add_form", clear_on_submit=True):

        date_input = st.date_input("Дата тренировки", datetime.now())
        date_str = date_input.strftime("%d.%m")

        existing_exercises = (
            sorted(df["Упражнение"].unique().tolist())
            if not df.empty
            else []
        )

        exercise = st.selectbox(
            "Начните вводить или выберите упражнение:",
            options=[""] + existing_exercises,
            index=0,
            key="exercise_selectbox"
        )

        custom_exercise = st.text_input(
            "ИЛИ введите НОВОЕ упражнение:",
            placeholder="Например: Жим лежа",
            key="custom_exercise_input"
        )

        st.write("---")

        col1, col2, col3 = st.columns(3)

        with col1:
            sets = st.number_input(
                "Подходы",
                min_value=1,
                value=3,
                step=1,
                key="sets_input"
            )

        with col2:
            reps = st.number_input(
                "Повторы",
                min_value=1,
                value=8,
                step=1,
                key="reps_input"
            )

        with col3:
            weight = st.number_input(
                "Вес (кг)",
                min_value=0.0,
                value=0.0,
                step=0.5,
                key="weight_input"
            )

        comment = st.selectbox(
            "Примечание (необязательно)",
            ["", "разминка", "рабочий вес"],
            key="comment_select"
        )

        submit_btn = st.form_submit_button(
            "💾 Записать в таблицу",
            use_container_width=True,
            type="primary"
        )

        if submit_btn:
            final_exercise = (
                custom_exercise.strip()
                if custom_exercise.strip()
                else exercise
            )

            if not final_exercise:
                st.error("Пожалуйста, выберите или введите упражнение!")
            else:
                weight_str = (
                    f"{int(weight)}"
                    if weight.is_integer()
                    else f"{weight}"
                )
                res_string = f"{sets}/{reps} {weight_str}"
                if comment:
                    res_string += f" ({comment})"

                new_row = pd.DataFrame(
                    [[str(date_str), str(final_exercise), str(res_string)]],
                    columns=["Дата", "Упражнение", "Результат"]
                )

                st.session_state.workout_db = pd.concat(
                    [st.session_state.workout_db, new_row],
                    ignore_index=True
                )

                save_database()
                st.success(f"✅ Записано: {final_exercise} — {res_string}")
