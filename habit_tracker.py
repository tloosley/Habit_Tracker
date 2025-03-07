# Dependencies: streamlit, datetime (built-in), random
import streamlit as st
from datetime import datetime, timedelta
import random

# Initialize session state to store habits
def init_session_state():
    if 'habits' not in st.session_state:
        st.session_state['habits'] = []

# Add a new habit with a start date
def add_habit_with_date(name, start_date, frequency_days):
    habit_id = len(st.session_state['habits']) + 1
    completions = []
    current_date = start_date
    yesterday = datetime.now().date() - timedelta(days=1)
    while current_date <= yesterday:
        completions.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=frequency_days)
    
    habit = {
        'id': habit_id,
        'name': name,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'frequency_days': frequency_days,
        'completions': completions
    }
    st.session_state['habits'].append(habit)

# Add a new habit with number of days
def add_habit_with_days(name, days, frequency_days):
    habit_id = len(st.session_state['habits']) + 1
    start_date = datetime.now().date() - timedelta(days=days)
    completions = []
    current_date = start_date
    yesterday = datetime.now().date() - timedelta(days=1)
    while current_date <= yesterday:
        completions.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=frequency_days)
    
    habit = {
        'id': habit_id,
        'name': name,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'frequency_days': frequency_days,
        'completions': completions,
        'streak_length_days': days
    }
    st.session_state['habits'].append(habit)

# Mark habit as completed today
def complete_habit_today(habit_id):
    for habit in st.session_state['habits']:
        if habit['id'] == habit_id:
            today = datetime.now().strftime('%Y-%m-%d')
            if today not in habit['completions']:
                habit['completions'].append(today)

# Delete a habit
def delete_habit(habit_id):
    st.session_state['habits'] = [habit for habit in st.session_state['habits'] if habit['id'] != habit_id]

# Get habit streak data
def get_habit_data(habit):
    streak_days = len(habit['completions'])
    start_date = datetime.strptime(habit['start_date'], '%Y-%m-%d').date()
    total_days = (datetime.now().date() - start_date).days + 1
    streak_length_days = habit.get('streak_length_days', total_days)
    return {
        'id': habit['id'],
        'name': habit['name'],
        'start_date': habit['start_date'],
        'frequency_days': habit['frequency_days'],
        'completions': habit['completions'],
        'streak_days': streak_days,
        'total_days': total_days,
        'streak_length_days': streak_length_days
    }

# Calculate total statistics
def get_total_stats():
    total_habits = len(st.session_state['habits'])
    total_completions = sum(len(habit['completions']) for habit in st.session_state['habits'])
    total_days = sum((datetime.now().date() - datetime.strptime(habit['start_date'], '%Y-%m-%d').date()).days + 1 
                     for habit in st.session_state['habits'])
    total_years = total_days / 365.25
    return {
        'total_habits': total_habits,
        'total_completions': total_completions,
        'total_days': total_days,
        'total_years': total_years
    }

# Main app
def main():
    # Updated styling with more specific selectors for buttons
    st.markdown("""
        <style>
        div.stButton > button {
            background-color: #e0e0e0;
            color: black;
            border-radius: 5px;
        }
        div.delete-button > button {
            background-color: #ff4444;
            color: white;
            border-radius: 5px;
        }
        .stExpander {
            background-color: #ffffff; 
            border-radius: 5px; 
            padding: 10px; 
            border: 1px solid #dcdcdc;
        }
        h1 {
            color: #2f4f4f; 
            font-family: 'Arial', sans-serif;
        }
        h2 {
            color: #4682b4;
        }
        .stSuccess {
            background-color: #d4edda; 
            padding: 10px; 
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Habit Streak Tracker")
    st.write("Track your habits and maintain streaks with ease.")
    
    init_session_state()

    # Add Habit Form
    st.subheader("Add a New Habit")
    input_method = st.radio("Specify the start by:", ("Start Date", "Number of Days"))
    with st.form(key='habit_form', clear_on_submit=True):
        habit_name = st.text_input("Habit Name", placeholder="e.g., Duolingo Streak")
        if input_method == "Start Date":
            start_input = st.date_input("Start Date", value=datetime.now().date() - timedelta(days=7))
        else:
            start_input = st.number_input("Streak Length (Days)", min_value=0, value=30, step=1)
        frequency_options = {"Daily": 1, "Every 2 Days": 2, "Weekly": 7}
        frequency_label = st.selectbox("Frequency", list(frequency_options.keys()))
        frequency_days = frequency_options[frequency_label]
        submit_button = st.form_submit_button(label="Add Habit")
        if submit_button and habit_name:
            if input_method == "Start Date":
                add_habit_with_date(habit_name, start_input, frequency_days)
            else:
                add_habit_with_days(habit_name, start_input, frequency_days)
            st.success(f"Habit '{habit_name}' added successfully!")

    # Total Statistics
    st.subheader("Total Statistics")
    stats = get_total_stats()
    if stats['total_habits'] == 0:
        st.write("No habits added yet.")
    else:
        st.write(f"- Total Number of Habits: {stats['total_habits']}")
        st.write(f"- Total Completions Across All Habits: {stats['total_completions']}")
        st.write(f"- Total Days Across All Habits: {stats['total_days']}")
        st.write(f"- Total Years (approx.): {stats['total_years']:.2f}")
        if stats['total_habits'] > 1:
            st.write(f"- Average Completions per Habit: {stats['total_completions'] / stats['total_habits']:.1f}")

    # Habit Overview Dashboard
    st.subheader("Habit Overview Dashboard")
    if not st.session_state['habits']:
        st.write("No habits to display.")
    else:
        st.write("Quick view of all your habits:")
        for habit in st.session_state['habits']:
            habit_data = get_habit_data(habit)
            st.write(f"- {habit_data['name']}: {habit_data['streak_days']} completions, started {habit_data['start_date']}")

    # Suggested Habit Section
    st.subheader("Suggested Habit")
    suggested_habits = [
        "Read for 10 minutes every day",
        "Meditate for 5 minutes",
        "Take a 30-minute walk",
        "Write a journal entry",
        "Drink 8 glasses of water",
        "Practice a musical instrument for 15 minutes",
        "Do 10 minutes of stretching",
        "Spend 15 minutes learning a new language"
    ]
    if "suggested_habit" not in st.session_state:
        st.session_state["suggested_habit"] = random.choice(suggested_habits)
    st.write("Struggling for ideas? Try this suggested habit:")
    st.markdown(f"**{st.session_state['suggested_habit']}**")
    if st.button("New Suggestion"):
        new_suggestion = random.choice(suggested_habits)
        while new_suggestion == st.session_state["suggested_habit"]:
            new_suggestion = random.choice(suggested_habits)
        st.session_state["suggested_habit"] = new_suggestion
        st.rerun()

    # Display Habits
    st.subheader("Your Habit Streaks")
    if not st.session_state['habits']:
        st.write("No habits yet—add one to begin tracking.")
    for habit in st.session_state['habits']:
        habit_data = get_habit_data(habit)
        with st.expander(f"{habit_data['name']} (Started: {habit_data['start_date']})"):
            st.write(f"Frequency: Every {habit_data['frequency_days']} day(s)")
            if 'streak_length_days' in habit_data:
                st.write(f"Streak Length: {habit_data['streak_length_days']} days")
            
            # Streak Facts
            st.write("Streak Statistics:")
            st.write(f"- Days Completed: {habit_data['streak_days']}")
            st.write(f"- Total Days Since Start: {habit_data['total_days']}")
            if habit_data['frequency_days'] == 1:
                st.write(f"- Consistency: {habit_data['streak_days'] / habit_data['total_days'] * 100:.1f}%")
            else:
                expected = habit_data['total_days'] // habit_data['frequency_days']
                st.write(f"- Expected Completions: {expected}")
            
            # Complete Today Button
            today = datetime.now().strftime('%Y-%m-%d')
            if today not in habit_data['completions']:
                if st.button("Mark Completed Today", key=f"complete_{habit_data['id']}"):
                    complete_habit_today(habit_data['id'])
                    st.success(f"'{habit_data['name']}' marked as completed for today.")
            else:
                st.write("Completed today.")
            
            # Delete Habit Button
            with st.container():
                st.markdown('<div class="delete-button">', unsafe_allow_html=True)
                if st.button("Delete Habit", key=f"delete_{habit_data['id']}"):
                    delete_habit(habit_data['id'])
                    st.success(f"'{habit_data['name']}' deleted successfully.")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write("Habit Streak Tracker © ¦ Created by Tom Loosley ¦ Published in 2025")
st.markdown("Found a problem? <a href='mailto:loosleytom@gmail.com'>Report an issue</a>", unsafe_allow_html=True)