import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Настройка страницы под мобильные телефоны
st.set_page_config(page_title="Дневник тренировок", page_icon="🏋️‍♂️", layout="wide")

# Имя файла для персистентного хранения данных в облаке
DATA_FILE = "workout_diary_storage.csv"

# Логика загрузки данных
if "workout_db" not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state.workout_db = pd.read_csv(DATA_FILE)
    else:
        st.session_state.workout_db = pd.DataFrame(columns=["Дата", "Упражнение", "Результат"])

df = st.session_state.workout_db

st.title("🏋️‍♂️ Мой Блокнот Тренировок")

# Вкладки приложения
tab_view, tab_add = st.tabs(["📋 Таблица тренировок", "➕ Добавить запись"])

# --- ВКЛАДКА 1: ОТОБРАЖЕНИЕ ТАБЛИЦЫ ---
with tab_view:
    st.subheader("Журнал по дням")
    
    if not df.empty:
        try:
            df["Дата"] = df["Дата"].astype(str)
            df["Упражнение"] = df["Упражнение"].astype(str)
            df["Результат"] = df["Результат"].astype(str)
            
            # ИСПРАВЛЕНИЕ: Теперь объединяем записи через перенос строки \n вместо палочки |
            grouped = df.groupby(["Упражнение", "Дата"])["Результат"].apply(lambda x: "\n".join(x)).reset_index()
            
            # Превращаем в кросс-таблицу
            pivot_df = grouped.pivot(index="Упражнение", columns="Дата", values="Результат").reset_index()
            
            # Сортируем даты по порядку
            date_cols = sorted([col for col in pivot_df.columns if col != "Упражнение"])
            final_cols = ["Упражнение"] + date_cols
            pivot_df = pivot_df[final_cols]
            
            # Заменяем пустоты на прочерки
            pivot_df = pivot_df.fillna("—")
            
            # Динамическая конфигурация столбцов для включения переноса строк
            col_config = {
                "Упражнение": st.column_config.TextColumn(
                    "Упражнение", 
                    pinned=True, 
                    width="medium"
                )
            }
            
            # Включаем многострочный режим отображения для каждого столбца с датой
            for col in date_cols:
                col_config[col] = st.column_config.TextColumn(col, wrap_text=True)
            
            # Вывод таблицы с поддержкой многострочного текста
            st.data_editor(
                pivot_df, 
                use_container_width=True, 
                hide_index=True,
                disabled=True, 
                column_config=col_config
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
        st.info("Таблица пуста. Перейдите на вкладку 'Добавить запись', чтобы внесить первые данные.")

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
                
                new_row = pd.DataFrame([[date_str, final_exercise, res_string]], columns=["Дата", "Упражнение", "Результат"])
                st.session_state.workout_db = pd.concat([st.session_state.workout_db, new_row], ignore_index=True)
                st.session_state.workout_db.to_csv(DATA_FILE, index=False)
                
                st.success(f"Добавлено: {final_exercise} -> {res_string}")
                st.rerun()
