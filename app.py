import streamlit as st
import pandas as pd
import os
from datetime import date

# =========================
# НАСТРОЙКИ
# =========================

st.set_page_config(
    page_title="Дневник тренировок",
    page_icon="🎃",
    layout="wide"
)

STORAGE_FILE = "workout_diary_storage.csv"

# =========================
# СТИЛИ
# =========================

st.markdown("""
<style>
    .stApp {
        background-color: #fffaf3;
    }

    h1, h2, h3 {
        color: #7a3e00;
    }

    .stButton > button {
        border-radius: 10px;
    }

    .exercise-card {
        background: #fff;
        border: 1px solid #f0d8b5;
        border-radius: 12px;
        padding: 10px 14px;
        margin-bottom: 8px;
    }

    .result-chip {
        display: inline-block;
        background: #fff1dc;
        border-radius: 8px;
        padding: 5px 9px;
        margin: 3px 3px 3px 0;
        font-size: 14px;
    }

    .small-text {
        color: #777;
        font-size: 13px;
    }

    @media (max-width: 700px) {
        .block-container {
            padding-left: 0.7rem;
            padding-right: 0.7rem;
            padding-top: 1rem;
        }

        h1 {
            font-size: 1.7rem;
        }

        .exercise-card {
            padding: 9px 10px;
        }

        .result-chip {
            font-size: 13px;
            padding: 4px 7px;
        }
    }
</style>
""", unsafe_allow_html=True)

# =========================
# ЗАГОЛОВОК
# =========================

st.markdown(
    """
    <div style="
        display:flex;
        align-items:center;
        gap:12px;
        margin-bottom:10px;
    ">
        <div style="font-size:45px;">🎃</div>
        <div>
            <h1 style="margin:0;">Дневник тренировок</h1>
            <div style="color:#8a5a32;">Записывай подходы и следи за прогрессом</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# ЗАГРУЗКА ДАННЫХ
# =========================

if "workout_db" not in st.session_state:

    if os.path.exists(STORAGE_FILE):
        try:
            df = pd.read_csv(STORAGE_FILE)

            required_columns = ["Дата", "Упражнение", "Результат"]

            for col in required_columns:
                if col not in df.columns:
                    df[col] = ""

            df = df[required_columns]

        except Exception:
            df = pd.DataFrame(
                columns=["Дата", "Упражнение", "Результат"]
            )

    else:
        df = pd.DataFrame(
            columns=["Дата", "Упражнение", "Результат"]
        )

    st.session_state.workout_db = df


# =========================
# СОХРАНЕНИЕ
# =========================

def save_data():
    st.session_state.workout_db.to_csv(
        STORAGE_FILE,
        index=False
    )


# =========================
# ДОБАВЛЕНИЕ ЗАПИСИ
# =========================

st.subheader("➕ Добавить упражнение")

with st.form("add_workout_form", clear_on_submit=True):

    col1, col2 = st.columns([1, 2])

    with col1:
        workout_date = st.date_input(
            "Дата",
            value=date.today()
        )

    with col2:
        exercise = st.text_input(
            "Упражнение",
            placeholder="Например: Жим лёжа"
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        sets = st.number_input(
            "Подходы",
            min_value=1,
            max_value=50,
            value=3,
            step=1
        )

    with col2:
        reps = st.number_input(
            "Повторения",
            min_value=1,
            max_value=100,
            value=10,
            step=1
        )

    with col3:
        weight = st.number_input(
            "Вес, кг",
            min_value=0.0,
            max_value=500.0,
            value=0.0,
            step=0.5
        )

    comment = st.selectbox(
        "Примечание (необязательно)",
        [
            "",
            "разминка",
            "рабочий вес"
        ]
    )

    submitted = st.form_submit_button(
        "💾 Сохранить",
        use_container_width=True
    )

    if submitted:

        if not exercise.strip():
            st.warning("Введите название упражнения.")

        else:

            if weight == int(weight):
                weight_str = str(int(weight))
            else:
                weight_str = str(weight)

            res_string = f"{sets}/{reps} {weight_str}"

            if comment:
                res_string += f" ({comment})"

            new_row = pd.DataFrame([{
                "Дата": workout_date.strftime("%Y-%m-%d"),
                "Упражнение": exercise.strip(),
                "Результат": res_string
            }])

            st.session_state.workout_db = pd.concat(
                [
                    st.session_state.workout_db,
                    new_row
                ],
                ignore_index=True
            )

            save_data()

            st.success("Запись добавлена!")
            st.rerun()


# =========================
# УДАЛЕНИЕ
# =========================

def delete_record(index):

    df = st.session_state.workout_db

    if index < 0 or index >= len(df):
        return

    deleted_row = df.iloc[index].copy()

    st.session_state.last_deleted = {
        "index": index,
        "row": deleted_row.to_dict()
    }

    st.session_state.workout_db = df.drop(
        index
    ).reset_index(drop=True)

    save_data()


def undo_delete():

    if "last_deleted" not in st.session_state:
        return

    deleted = st.session_state.last_deleted

    index = deleted["index"]
    row = deleted["row"]

    df = st.session_state.workout_db

    index = min(index, len(df))

    upper = df.iloc[:index]
    lower = df.iloc[index:]

    restored_row = pd.DataFrame([row])

    st.session_state.workout_db = pd.concat(
        [
            upper,
            restored_row,
            lower
        ],
        ignore_index=True
    )

    save_data()

    del st.session_state.last_deleted


# =========================
# ОТМЕНА УДАЛЕНИЯ
# =========================

if "last_deleted" in st.session_state:

    st.info("Последняя запись была удалена.")

    if st.button("↩️ Отменить удаление"):
        undo_delete()
        st.rerun()


# =========================
# ТЕКУЩИЕ ДАННЫЕ
# =========================

df = st.session_state.workout_db

if df.empty:

    st.info(
        "Пока нет записей. Добавь первое упражнение выше."
    )

    st.stop()


# =========================
# РЕЖИМЫ ПРОСМОТРА
# =========================

view_mode = st.radio(
    "Режим просмотра",
    [
        "📅 Дни",
        "💪 Упражнения"
    ],
    horizontal=True
)


# ============================================================
# ПРОСМОТР ПО ДНЯМ
# ============================================================

if view_mode == "📅 Дни":

    dates = sorted(
        df["Дата"].dropna().unique(),
        reverse=True
    )

    for day in dates:

        day_df = df[df["Дата"] == day]

        # Последний день раскрыт автоматически
        is_first = day == dates[0]

        with st.expander(
            f"📅 {day}",
            expanded=is_first
        ):

            for index, row in day_df.iterrows():

                exercise_name = row["Упражнение"]
                result = row["Результат"]

                col1, col2 = st.columns(
                    [5, 1]
                )

                with col1:

                    st.markdown(
                        f"""
                        <div class="exercise-card">
                            <b>{exercise_name}</b><br>
                            <span class="result-chip">
                                {result}
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col2:

                    if st.button(
                        "🗑️",
                        key=f"delete_day_{index}",
                        help="Удалить эту запись"
                    ):
                        delete_record(index)
                        st.rerun()


# ============================================================
# ПРОСМОТР ПО УПРАЖНЕНИЯМ
# ============================================================

elif view_mode == "💪 Упражнения":

    exercises = sorted(
        df["Упражнение"]
        .dropna()
        .unique()
    )

    selected_exercise = st.selectbox(
        "Выбери упражнение",
        exercises
    )

    exercise_df = df[
        df["Упражнение"] == selected_exercise
    ].sort_values(
        "Дата",
        ascending=False
    )

    st.subheader(
        f"💪 {selected_exercise}"
    )

    for index, row in exercise_df.iterrows():

        col1, col2 = st.columns(
            [5, 1]
        )

        with col1:

            st.markdown(
                f"""
                <div class="exercise-card">
                    <b>📅 {row["Дата"]}</b><br>
                    <span class="result-chip">
                        {row["Результат"]}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            if st.button(
                "🗑️",
                key=f"delete_exercise_{index}",
                help="Удалить эту запись"
            ):
                delete_record(index)
                st.rerun()
