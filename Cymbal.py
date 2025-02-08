import streamlit as st
import google.generativeai as genai
import os
import time
import threading
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Ensure API key exists
if not api_key:
    st.error("API Key is missing! Make sure it's set in the .env file.")
    st.stop()

# Configure Google Generative AI
genai.configure(api_key=api_key)

# Function to generate chatbot response
def generate_response(user_input):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_input)
        return response.text if response and hasattr(response, "text") else "I couldn’t find an answer. Try again!"
    except Exception as e:
        return "⚠️ Error: Unable to process response. Check API Key & Internet Connection."

# ---- UI MODE SELECTION ----
st.sidebar.title("🎨 Customize Your Experience")
mode = st.sidebar.radio("🌈 Choose Your View:", ["Low Stimulation Mode", "Dopamine Mode"])

# ---- CHAT HISTORY ----
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.markdown("### ✨ ADHD Study Chatbot")
for message in st.session_state["messages"]:
    role = "You:" if message["role"] == "user" else "ADHD Buddy:"
    st.markdown(f"**{role}** {message['content']}")

# ---- USER INPUT ----
if "last_input" not in st.session_state:
    st.session_state["last_input"] = None

user_input = st.text_input("💬 Type your message here:", key="user_input", value="", label_visibility="collapsed")

# Add a "Send" button to trigger input processing
if st.button("Send") and user_input:
    st.session_state["last_input"] = user_input  
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        time.sleep(1)
        bot_reply = generate_response(user_input)

    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

    # Clear the input box after sending
    st.rerun()


# ---- POMODORO TIMER ----
st.sidebar.subheader("⏳ Pomodoro Timer")

# Timer session duration selection
session_length = st.sidebar.selectbox("Select Focus Session Length:", [10, 20, 30, 40, 50, 60], index=2)  
session_seconds = session_length * 60  # Convert minutes to seconds

# Initialize session state variables
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None
if "timer_seconds" not in st.session_state:
    st.session_state["timer_seconds"] = session_seconds  
if "timer_running" not in st.session_state:
    st.session_state["timer_running"] = False

# Timer display placeholders
timer_display = st.sidebar.empty()
progress_bar = st.sidebar.progress(0)

def start_timer(duration):
    """Starts the countdown timer and stores start time."""
    st.session_state["start_time"] = datetime.now()
    st.session_state["timer_seconds"] = duration
    st.session_state["timer_running"] = True

# Calculate remaining time
if st.session_state["timer_running"] and st.session_state["start_time"]:
    elapsed_time = (datetime.now() - st.session_state["start_time"]).total_seconds()
    remaining_time = max(st.session_state["timer_seconds"] - int(elapsed_time), 0)

    mins, secs = divmod(remaining_time, 60)
    timer_display.markdown(f"**Time Left:** {int(mins)} min {int(secs)} sec")
    progress_bar.progress(remaining_time / st.session_state["timer_seconds"])

    if remaining_time == 0:
        st.sidebar.warning("🚨 Time for a break! 🚨")
        st.session_state["timer_running"] = False  # Stop timer

# Buttons to control the timer
if st.sidebar.button("Start Focus Session"):
    start_timer(session_seconds)

if st.sidebar.button("Take a Break"):
    start_timer(300)  # 5-minute break

if st.sidebar.button("Stop Timer"):
    st.session_state["timer_running"] = False
    st.session_state["start_time"] = None


# ---- SMART TASK MANAGEMENT ----
st.sidebar.subheader("🚀 Smart Task Prioritization")
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []
if "finished_tasks" not in st.session_state:
    st.session_state["finished_tasks"] = []

task_emojis = {
    "urgent": "🔥",
    "creative": "💡",
    "study": "📚",
    "general": "✅"
}

new_task = st.sidebar.text_input("Add New Task:")
task_type = st.sidebar.selectbox("Select Task Type:", ["urgent", "creative", "study", "general"])
deadline = st.sidebar.date_input("Set Deadline:", min_value=datetime.today())

if st.sidebar.button("➕ Add Task"):
    if new_task:
        emoji = task_emojis.get(task_type, "✅")
        task_entry = f"{emoji} {new_task} (Due: {deadline.strftime('%b %d')})"
        st.session_state["tasks"].append(task_entry)

# Display tasks with deadlines & individual remove buttons
st.sidebar.subheader("📌 Current Tasks")
if st.session_state["tasks"]:
    for task in st.session_state["tasks"]:
        col1, col2 = st.sidebar.columns([0.8, 0.2])
        col1.markdown(task)
        if col2.button("❌", key=task):
            st.session_state["tasks"].remove(task)
            st.rerun()

# Mark Task as Finished
task_to_finish = st.sidebar.selectbox("✅ Mark Task as Finished:", ["None"] + st.session_state["tasks"])
if st.sidebar.button("✔️ Complete Task"):
    if task_to_finish != "None":
        st.session_state["tasks"].remove(task_to_finish)
        st.session_state["finished_tasks"].append(task_to_finish)
        st.rerun()

# Display Finished Tasks
st.sidebar.subheader("🎯 Completed Tasks")
if st.session_state["finished_tasks"]:
    for task in st.session_state["finished_tasks"]:
        st.sidebar.markdown(f"✅ {task}")

# ---- STUDY SESSION SUMMARY ----
if st.sidebar.button("📊 Finish Study Session"):
    if st.session_state["study_start_time"]:
        study_time = datetime.now() - st.session_state["study_start_time"]
        minutes_studied = study_time.seconds // 60
        completed_tasks = len(st.session_state["finished_tasks"])

        study_tips = [
            "Try summarizing what you learned today in a few sentences.",
            "Use active recall techniques to reinforce what you studied.",
            "Next time, try breaking complex topics into smaller chunks.",
            "Use visual aids or mind maps for better retention.",
            "Ensure you take enough breaks to avoid burnout!"
        ]

        st.sidebar.markdown("### 📊 Study Session Summary")
        st.sidebar.markdown(f"**Total Study Time:** {minutes_studied} minutes")
        st.sidebar.markdown(f"**Tasks Completed:** {completed_tasks}")
        st.sidebar.markdown("#### 📌 Tips for Next Study Session:")
        for tip in study_tips[:3]:  # Display only 3 tips
            st.sidebar.markdown(f"✅ {tip}")

        # Reset session
        st.session_state["study_start_time"] = None
        st.session_state["finished_tasks"] = []
        st.session_state["messages"] = []
        st.session_state["timer_seconds"] = 1500
        st.rerun()
    else:
        st.sidebar.warning("You need to start a focus session first!")

# ---- STICKY NOTES FEATURE ----
st.sidebar.subheader("📝 Sticky Notes")
if "sticky_notes" not in st.session_state:
    st.session_state["sticky_notes"] = []

note = st.sidebar.text_input("Write a quick thought:")
if st.sidebar.button("📌 Save Note") and note:
    st.session_state["sticky_notes"].append(note)

if st.sidebar.button("🗑️ Clear Notes"):
    st.session_state["sticky_notes"] = []

for saved_note in st.session_state["sticky_notes"]:
    st.sidebar.markdown(f"✅ {saved_note}")

# ---- CLEAR CHAT BUTTON ----
if st.button("Clear Chat"):
    st.session_state["messages"] = []
    st.rerun()
