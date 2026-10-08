import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Имя файла для базы данных
DATA_FILE = "workout_diary.csv"

# Настройка страницы под мобильные телефоны
st.set_page_config(page_title="Дневник тренировок", page_icon="🏋️‍♂️", layout="wide")

# Загрузка или создание базы данных
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df["Дата"] = df["Дата"].astype(str)
else:
    df = pd.DataFrame(columns=["Дата", "Упражнение", "Результат"])

st.title("🏋️‍♂️ Мой Блокнот Тренировок")

# Создаем вкладки для телефона
tab_view, tab_add = st.tabs(["📋 Таблица тренировок", "➕ Добавить запись"])

# --- ВКЛАДКА 1: ОТОБРАЖЕНИЕ ТАБЛИЦЫ (КАК В БЛОКНОТЕ) ---
with tab_view:
    st.subheader("Журнал по дням")
    
    if not df.empty:
        try:
            # Превращаем список в таблицу "Упражнение | Дата1 | Дата2..."
            pivot_df = df.pivot(index="Упражнение", columns="Дата", values="Результат").reset_index()
            
            # Сортируем даты-столбцы по порядку (новые дни будут добавляться справа)
            date_cols = sorted([col for col in pivot_df.columns if col != "Упражнение"])
            final_cols = ["Упражнение"] + date_cols
            pivot_df = pivot_df[final_cols]
            
            # Заменяем пустые тренировки на прочерки
            pivot_df = pivot_df.fillna("—")
            
            # Вывод таблицы с закрепленным левым столбцом
            st.data_editor(
                pivot_df, 
                use_container_width=True, 
                hide_index=True,
                disabled=True, # Защита от случайного редактирования при скролле пальцем
                column_config={
                    "Упражнение": st.column_config.TextColumn(
                        "Упражнение", 
                        pinned=True, # Закрепляем столбец с названиями намертво
                        width="medium"
                    )
                }
            )
            
        except Exception as e:
            # Если за один день ввели одно упражнение несколько раз (например, разминка и рабочий вес)
            grouped = df.groupby(["Упражнение", "Дата"])["Результат"].apply(lambda x: " | ".join(x)).reset_index()
            pivot_df = grouped.pivot(index="Упражнение", columns="Дата", values="Результат").reset_index()
            pivot_df = pivot_df.fillna("—")
            
            st.data_editor(
                pivot_df, 
                use_container_width=True, 
                hide_index=True,
                disabled=True,
                column_config={
                    "Упражнение": st.column_config.TextColumn(
                        "Упражнение", 
                        pinned=True, 
                        width="medium"
                    )
                }
            )
            
        st.write("") 
        if st.button("❌ Удалить самую последнюю запись", type="secondary", use_container_width=True):
            df = df.drop(df.index[-1])
            df.to_csv(DATA_FILE, index=False)
            st.rerun()
    else:
        st.info("Таблица пуста. Перейдите на вкладку 'Добавить запись', чтобы внесить первые данные.")

# --- ВКЛАДКА 2: ВВОД ДАННЫХ С ТЕЛЕФОНА ---
with tab_add:
    st.subheader("Новый подход / упражнение")
    
    with st.form("add_form", clear_on_submit=True):
        date_input = st.date_input("Дата тренировки", datetime.now())
        date_str = date_input.strftime("%d.%m") # Формат "05.10", "07.10"
        
        unique_exercises = sorted(df["Упражнение"].unique().tolist()) if not df.empty else []
        exercise_type = st.radio("Выбрать упражнение:", ["Из существующих", "Написать новое"], horizontal=True)
        
        if exercise_type == "Из существующих" and unique_exercises:
            exercise = st.selectbox("Выберите упражнение", unique_exercises)
        else:
            exercise = st.text_input("Введите название упражнения", placeholder="Например: Становая")
            
        st.write("---")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            sets = st.number_input("Подходы", min_value=1, value=2, step=1)
        with col2:
            reps = st.number_input("Повторы", min_value=1, value=8, step=1)
        with col3:
            weight = st.number_input("Вес (кг)", min_value=0.0, value=0.0, step=0.5)
            
        comment = st.selectbox("Примечание (необязательно)", ["", "разминка", "рабочий вес"])
        
        submit_btn = st.form_submit_button("💾 Записать в таблицу", use_container_width=True, type="primary")
        
        if submit_btn:
            if not exercise or not exercise.strip():
                st.error("Упражнение не может быть пустым!")
            else:
                weight_str = f"{int(weight)}" if weight.is_integer() else f"{weight}"
                res_string = f"{sets}/{reps} {weight_str}"
                if comment:
                    res_string += f" ({comment})"
                
                new_row = pd.DataFrame([[date_str, exercise.strip(), res_string]], columns=["Дата", "Упражнение", "Результат"])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success(f"Добавлено: {exercise} -> {res_string}")
                st.rerun()
