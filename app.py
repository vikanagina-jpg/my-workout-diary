```python
import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# ============================================================
# НАСТРОЙКИ
# ============================================================

st.set_page_config(
    page_title="Дневник тренировок",
    page_icon="🏋️‍♂️",
    layout="wide"
)

DB_FILE = "workout_diary.db"


# ============================================================
# БАЗА ДАННЫХ
# ============================================================

def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)


def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_date TEXT NOT NULL,
            exercise TEXT NOT NULL,
            sets INTEGER NOT NULL,
            reps INTEGER NOT NULL,
            weight REAL NOT NULL,
            comment TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


# ============================================================
# РАБОТА С ДАННЫМИ
# ============================================================

def load_workouts():
    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT
            id,
            workout_date,
            exercise,
            sets,
            reps,
            weight,
            comment
        FROM workouts
        ORDER BY workout_date DESC, id DESC
    """, conn)

    conn.close()
    return df


def add_workout(workout_date, exercise, sets, reps, weight, comment):
    conn = get_connection()

    conn.execute("""
        INSERT INTO workouts
        (workout_date, exercise, sets, reps, weight, comment)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        workout_date,
        exercise,
        sets,
        reps,
        weight,
        comment
    ))

    conn.commit()
    conn.close()


def delete_workout(workout_id):
    conn = get_connection()

    conn.execute(
        "DELETE FROM workouts WHERE id = ?",
        (workout_id,)
    )

    conn.commit()
    conn.close()


def delete_all_workouts():
    conn = get_connection()

    conn.execute("DELETE FROM workouts")

    conn.commit()
    conn.close()


# ============================================================
# ЗАГРУЗКА
# ============================================================

df = load_workouts()


# ============================================================
# ЗАГОЛОВОК
# ============================================================

st.title("🏋️‍♂️ Мой дневник тренировок")

st.caption(
    "Добавляй любые упражнения и сколько угодно подходов. "
    "Данные сохраняются в базе SQLite."
)


# ============================================================
# ВКЛАДКИ
# ============================================================

tab_add, tab_table, tab_history = st.tabs([
    "➕ Добавить",
    "📋 Таблица",
    "📅 История"
])


# ============================================================
# ДОБАВЛЕНИЕ
# ============================================================

with tab_add:

    st.subheader("Новая запись")

    # Все существующие упражнения
    if not df.empty:
        exercises = sorted(
            df["exercise"].dropna().unique().tolist()
        )
    else:
        exercises = []

    with st.form("add_workout", clear_on_submit=True):

        workout_date = st.date_input(
            "📅 Дата тренировки",
            value=date.today()
        )

        # Если упражнения уже есть — предлагаем выбрать
        if exercises:
            exercise_mode = st.radio(
                "Упражнение",
                [
                    "Выбрать существующее",
                    "Добавить новое"
                ],
                horizontal=True
            )

            if exercise_mode == "Выбрать существующее":
                exercise = st.selectbox(
                    "Выберите упражнение",
                    exercises
                )
            else:
                exercise = st.text_input(
                    "Название нового упражнения",
                    placeholder="Например: Становая тяга"
                )

        else:
            exercise = st.text_input(
                "Название упражнения",
                placeholder="Например: Жим лёжа"
            )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            sets = st.number_input(
                "Подходы",
                min_value=1,
                max_value=100,
                value=3,
                step=1
            )

        with col2:
            reps = st.number_input(
                "Повторы",
                min_value=1,
                max_value=1000,
                value=8,
                step=1
            )

        weight = st.number_input(
            "🏋️ Вес (кг)",
            min_value=0.0,
            max_value=1000.0,
            value=0.0,
            step=0.5
        )

        comment = st.selectbox(
            "Примечание",
            [
                "",
                "разминка",
                "рабочий вес",
                "тяжело",
                "легко",
                "до отказа"
            ]
        )

        save = st.form_submit_button(
            "💾 СОХРАНИТЬ",
            use_container_width=True,
            type="primary"
        )

        if save:

            exercise = exercise.strip()

            if not exercise:
                st.error("Введите название упражнения.")

            else:

                add_workout(
                    workout_date.strftime("%Y-%m-%d"),
                    exercise,
                    int(sets),
                    int(reps),
                    float(weight),
                    comment
                )

                st.success(
                    f"✅ Сохранено: {exercise} — "
                    f"{sets}×{reps} × {weight:g} кг"
                )

                st.rerun()


# ============================================================
# ОСНОВНАЯ ТАБЛИЦА
# ============================================================

with tab_table:

    st.subheader("📋 Все тренировки")

    if df.empty:

        st.info(
            "Пока нет записей. "
            "Перейди во вкладку «➕ Добавить»."
        )

    else:

        # Красивый формат результата
        display_df = df.copy()

        display_df["Дата"] = pd.to_datetime(
            display_df["workout_date"]
        ).dt.strftime("%d.%m.%Y")

        display_df["Результат"] = (
            display_df["sets"].astype(str)
            + " × "
            + display_df["reps"].astype(str)
            + " × "
            + display_df["weight"].map(lambda x: f"{x:g}")
            + " кг"
        )

        display_df["Примечание"] = (
            display_df["comment"].fillna("")
        )

        display_df = display_df[
            [
                "Дата",
                "exercise",
                "Результат",
                "Примечание"
            ]
        ]

        display_df.columns = [
            "Дата",
            "Упражнение",
            "Результат",
            "Примечание"
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# ИСТОРИЯ ПО УПРАЖНЕНИЯМ
# ============================================================

with tab_history:

    st.subheader("📅 История тренировок")

    if df.empty:

        st.info("История пока пустая.")

    else:

        exercises = sorted(
            df["exercise"].unique().tolist()
        )

        selected_exercise = st.selectbox(
            "Выберите упражнение",
            exercises
        )

        exercise_df = df[
            df["exercise"] == selected_exercise
        ].copy()

        exercise_df["Дата"] = pd.to_datetime(
            exercise_df["workout_date"]
        ).dt.strftime("%d.%m.%Y")

        exercise_df["Результат"] = (
            exercise_df["sets"].astype(str)
            + " × "
            + exercise_df["reps"].astype(str)
            + " × "
            + exercise_df["weight"].map(lambda x: f"{x:g}")
            + " кг"
        )

        history = exercise_df[
            [
                "Дата",
                "Результат",
                "comment"
            ]
        ].copy()

        history.columns = [
            "Дата",
            "Результат",
            "Примечание"
        ]

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # Максимальный вес
        # ----------------------------------------------------

        max_weight = exercise_df["weight"].max()

        st.metric(
            "🏆 Максимальный вес",
            f"{max_weight:g} кг"
        )


# ============================================================
# УПРАВЛЕНИЕ ЗАПИСЯМИ
# ============================================================

st.divider()

with st.expander("⚙️ Управление записями"):

    if df.empty:

        st.write("Нет записей для управления.")

    else:

        # Удаление конкретной записи

        delete_options = []

        for _, row in df.iterrows():

            weight_text = f"{row['weight']:g}"

            label = (
                f"{row['workout_date']} — "
                f"{row['exercise']} — "
                f"{row['sets']}×{row['reps']} "
                f"× {weight_text} кг"
            )

            delete_options.append(
                (row["id"], label)
            )

        selected_delete = st.selectbox(
            "Выберите запись для удаления",
            delete_options,
            format_func=lambda x: x[1]
        )

        if st.button(
            "🗑️ Удалить выбранную запись",
            use_container_width=True
        ):

            delete_workout(
                selected_delete[0]
            )

            st.success("Запись удалена.")

            st.rerun()

        st.divider()

        # Полное удаление

        st.warning(
            "Следующая кнопка удалит ВСЕ записи из дневника."
        )

        if st.button(
            "💥 Удалить весь дневник",
            use_container_width=True
        ):

            delete_all_workouts()

            st.success("Дневник очищен.")

            st.rerun()
```
