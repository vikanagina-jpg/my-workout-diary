import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# Настройка страницы под мобильные телефоны
st.set_page_config(page_title="Дневник тренировок", page_icon="🏋️‍♂️", layout="wide")

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

st.title("🏋️‍♂️ Мой Блокнот Тренировок")

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
            custom_table_html = f"""
            <div style="overflow-x: auto; max-width: 100%; border: 1px solid #ccd1d9; border-radius: 4px;">
                <style>
                    .workout-table {{ width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px; }}
                    .workout-table th {{ background-color: #f0f2f6; padding: 12px 10px; border: 1px solid #ccd1d9; font-weight: bold; text-align: left; }}
                    .workout-table td {{ padding: 12px 10px; border: 1px solid #ccd1d9; text-align: left; vertical-align: top; line-height: 1.4; }}
                    /* Закрепляем первый столбец намертво при скролле вбок */
                    .workout-table th:first-child, .workout-table td:first-child {{
                        position: sticky; left: 0; background-color: #ffffff; font-weight: bold; z-index: 2; border-right: 2px solid #ccd1d9;
                    }}
                    .workout-table th:first-child {{ background-color: #f0f2f6; z-index: 3; }}
                </style>
                {html_raw.replace('class="dataframe"', 'class="workout-table"')}
            </div>
            """
            
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
                label="📥 Скачать таблицу в Excel (для отправки)",
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
                
                new_row = pd.DataFrame([[str(date_str), str(final_exercise), str(res_string)]], columns=["Дата", "Упражнение", "Результат"])
                st.session_state.workout_db = pd.concat([st.session_state.workout_db, new_row], ignore_index=True)
                st.session_state.workout_db.to_csv(DATA_FILE, index=False)
                
                st.success(f"Добавлено: {final_exercise} -> {res_string}")
                st.rerun()
