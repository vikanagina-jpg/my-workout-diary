import streamlit as st
import pandas as pd
import sqlite3
from datetime import date


# ============================================================
# НАСТРОЙКА СТРАНИЦЫ
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
# ЗАГРУЗКА ТРЕНИРОВОК
# ============================================================

def load_workouts():
    conn = get_connection()

    df = pd.read_sql_query(
        """
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
        """,
        conn
    )

    conn.close()

    return df


# ============================================================
# ДОБАВЛЕНИЕ ТРЕНИРОВКИ
# ============================================================

def add_workout(
    workout_date,
    exercise,
    sets,
    reps,
    weight,
    comment
):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO workouts
        (
            workout_date,
            exercise,
            sets,
            reps,
            weight,
            comment
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            workout_date,
            exercise,
            sets,
            reps,
            weight,
            comment
        )
    )

    conn.commit()
    conn.close()


# ============================================================
# УДАЛЕНИЕ ТРЕНИРОВКИ
# ============================================================

def delete_workout(workout_id):
    conn = get_connection()

    conn.execute(
        "DELETE FROM workouts WHERE id = ?",
        (workout_id,)
    )

    conn.commit()
    conn.close()


# ============================================================
# УДАЛЕНИЕ ВСЕХ ТРЕНИРОВОК
# ============================================================

def delete_all_workouts():
    conn = get_connection()

    conn.execute("DELETE FROM workouts")

    conn.commit()
    conn.close()


# ============================================================
# ЗАГРУЖАЕМ ДАННЫЕ
# ============================================================

df = load_workouts()


# ============================================================
# ЗАГОЛОВОК
# ============================================================

st.title("🏋️‍♂️ Мой дневник тренировок")

st.caption(
    "Добавляй упражнения, подходы, повторения и вес. "
    "Все записи сохраняются."
)


# ============================================================
# ВКЛАДКИ
# ============================================================

tab_add, tab_table, tab_history = st.tabs(
    [
        "➕ Добавить",
        "📋 Все записи",
        "📈 История"
    ]
)


# ============================================================
# ВКЛАДКА: ДОБАВИТЬ
# ============================================================

with tab_add:

    st.subheader("➕ Новая запись")

    # Получаем список уже существующих упражнений
    if not df.empty:
        exercises = sorted(
            df["exercise"]
            .dropna()
            .unique()
            .tolist()
        )
    else:
        exercises = []

    with st.form(
        "add_workout_form",
        clear_on_submit=True
    ):

        # ----------------------------------------------------
        # ДАТА
        # ----------------------------------------------------

        workout_date = st.date_input(
            "📅 Дата тренировки",
            value=date.today()
        )

        # ----------------------------------------------------
        # УПРАЖНЕНИЕ
        # ----------------------------------------------------

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
                    placeholder="Например: Жим лёжа"
                )

        else:

            exercise = st.text_input(
                "Название упражнения",
                placeholder="Например: Жим лёжа"
            )

        st.divider()

        # ----------------------------------------------------
        # ПОДХОДЫ И ПОВТОРЫ
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            sets = st.number_input(
                "🔢 Подходы",
                min_value=1,
                max_value=100,
                value=3,
                step=1
            )

        with col2:

            reps = st.number_input(
                "🔁 Повторы",
                min_value=1,
                max_value=1000,
                value=8,
                step=1
            )

        # ----------------------------------------------------
        # ВЕС
        # ----------------------------------------------------

        weight = st.number_input(
            "🏋️ Вес (кг)",
            min_value=0.0,
            max_value=1000.0,
            value=0.0,
            step=0.5
        )

        # ----------------------------------------------------
        # КОММЕНТАРИЙ
        # ----------------------------------------------------

        comment = st.selectbox(
            "📝 Примечание",
            [
                "",
                "разминка",
                "рабочий вес",
                "тяжело",
                "легко",
                "до отказа"
            ]
        )

        # ----------------------------------------------------
        # КНОПКА
        # ----------------------------------------------------

        save_button = st.form_submit_button(
            "💾 СОХРАНИТЬ ЗАПИСЬ",
            use_container_width=True,
            type="primary"
        )

        # ----------------------------------------------------
        # СОХРАНЕНИЕ
        # ----------------------------------------------------

        if save_button:

            exercise = exercise.strip()

            if not exercise:

                st.error(
                    "❌ Введите название упражнения."
                )

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
                    f"✅ Добавлено: {exercise} — "
                    f"{sets} × {reps} × {weight:g} кг"
                )

                st.rerun()


# ============================================================
# ВКЛАДКА: ВСЕ ЗАПИСИ
# ============================================================

with tab_table:

    st.subheader("📋 Все записи")

    if df.empty:

        st.info(
            "Пока нет тренировок. "
            "Добавь первую запись во вкладке «➕ Добавить»."
        )

    else:

        display_df = df.copy()

        # Формат даты
        display_df["Дата"] = pd.to_datetime(
            display_df["workout_date"]
        ).dt.strftime("%d.%m.%Y")

        # Формат результата
        display_df["Результат"] = (
            display_df["sets"].astype(str)
            + " × "
            + display_df["reps"].astype(str)
            + " × "
            + display_df["weight"].map(
                lambda x: f"{x:g}"
            )
            + " кг"
        )

        display_df["Примечание"] = (
            display_df["comment"]
            .fillna("")
        )

        # Оставляем только нужные столбцы
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
# ВКЛАДКА: ИСТОРИЯ
# ============================================================

with tab_history:

    st.subheader("📈 История упражнения")

    if df.empty:

        st.info(
            "Добавь хотя бы одну тренировку, "
            "чтобы появилась история."
        )

    else:

        exercises = sorted(
            df["exercise"]
            .unique()
            .tolist()
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
            + exercise_df["weight"].map(
                lambda x: f"{x:g}"
            )
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
        # СТАТИСТИКА
        # ----------------------------------------------------

        max_weight = exercise_df["weight"].max()

        total_workouts = len(
            exercise_df["workout_date"].unique()
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🏆 Максимальный вес",
                f"{max_weight:g} кг"
            )

        with col2:

            st.metric(
                "📅 Дней тренировок",
                total_workouts
            )


# ============================================================
# УПРАВЛЕНИЕ ЗАПИСЯМИ
# ============================================================

st.divider()

with st.expander("⚙️ Управление дневником"):

    if df.empty:

        st.write(
            "Записей пока нет."
        )

    else:

        # ----------------------------------------------------
        # ВЫБОР ЗАПИСИ ДЛЯ УДАЛЕНИЯ
        # ----------------------------------------------------

        delete_options = []

        for _, row in df.iterrows():

            weight_text = f"{row['weight']:g}"

            label = (
                f"{row['workout_date']} — "
                f"{row['exercise']} — "
                f"{row['sets']}×{row['reps']} — "
                f"{weight_text} кг"
            )

            delete_options.append(
                (
                    int(row["id"]),
                    label
                )
            )

        selected_delete = st.selectbox(
            "Выберите запись",
            delete_options,
            format_func=lambda x: x[1]
        )

        # ----------------------------------------------------
        # УДАЛИТЬ ОДНУ ЗАПИСЬ
        # ----------------------------------------------------

        if st.button(
            "🗑️ Удалить выбранную запись",
            use_container_width=True
        ):

            delete_workout(
                selected_delete[0]
            )

            st.success(
                "Запись удалена."
            )

            st.rerun()

        st.divider()

        # ----------------------------------------------------
        # УДАЛИТЬ ВСЁ
        # ----------------------------------------------------

        st.warning(
            "Осторожно: следующая кнопка удалит "
            "все записи дневника."
        )

        if st.button(
            "💥 Удалить весь дневник",
            use_container_width=True
        ):

            delete_all_workouts()

            st.success(
                "Все записи удалены."
            )

            st.rerun()
