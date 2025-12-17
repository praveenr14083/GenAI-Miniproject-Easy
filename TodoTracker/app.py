import streamlit as st
import pandas as pd

st.set_page_config(page_title="Habit Tracker", layout="centered")

st.title("Daily Habit Tracker")


if "habits" not in st.session_state:
    st.session_state.habits = {}

new_habit = st.text_input("Add a new habit")

if st.button("Add Habit"):
    if new_habit:
        st.session_state.habits[new_habit] = False

st.divider()

st.subheader("Today's Habits")


completed = 0
for habit in st.session_state.habits:
    st.session_state.habits[habit] = st.checkbox(
        habit, st.session_state.habits[habit]
    )
    if st.session_state.habits[habit]:
        completed += 1

total = len(st.session_state.habits)


if total > 0:
    progress = completed / total
    st.progress(progress)
    st.write(f"**Progress:** {completed}/{total} habits completed")

st.divider()


st.subheader("Weekly Completion")

data = {
    "Day": [ "Wed", "Thu", "Fri", "Sat", "Sun","Mon", "Tue"],
    "Completed Habits": [completed,0,0,0,0,0,0]
}

df = pd.DataFrame(data)
st.bar_chart(df.set_index("Day"))
