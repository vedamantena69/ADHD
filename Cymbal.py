import streamlit as st
import google.generativeai as genai
import os
import time
import threading
from datetime import datetime, timedelta
from dotenv import load_dotenv
from PIL import Image  # Import the Pillow library
import streamlit.components.v1 as components

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Ensure API key exists
if not api_key:
    st.error("🔑 API Key Missing! Check .env file. 🔑")
    st.stop()

# Configure Google Generative AI
genai.configure(api_key=api_key)

# Chatbot Response Function
def generate_response(user_input):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_input)
        return response.text if response and hasattr(response, "text") else "🤔 Not sure. Can you rephrase?"
    except Exception as e:
        return "⚠️ Error! Check API key & internet. 🌐"

# ---- UI MODE SELECTION ----
st.set_page_config(page_title="Orbit", page_icon="🧠", layout="wide")

# Color Schemes
color_schemes = {
    "Low Stimulation 🧘": {
        "background": "#FDD7E4",  # Baby Pink
        "text": "#495057",  # Dark Gray
        "header": "#FDD7E4",  # Light pink for header - Same as background
        "sidebar": "#FDD7E4",  # Light Pink sidebar
        "frame": "#E91E63",  # Dark Pink Frame
        "highlight": "#FFFFFF"  # White Highlight
    },
    "Dopamine Boost ✨": {
        "background": "linear-gradient(to right, #FF69B4, #7DF9FF, #FFEB80, #32CD32)",  # Candy-like Gradient
        "text": "#000000",  # Black - for high contrast
        "header": "linear-gradient(to right, #FF69B4, #7DF9FF, #FFEB80, #32CD32)",  # Candy-like Gradient
        "sidebar": "#FFF2CC",  # Light Yellow sidebar
        "frame": "#8B4513",  # Saddle Brown Frame (can be adjusted)
        "highlight": "#FFFFE0"  # LightYellow Highlight
    }
}

# --- Sidebar ---
try:
    logo = Image.open("logo.png")  # Replace "orbit_logo.png" with your logo file
    st.sidebar.image(logo, width=150)  # Adjust width as needed
except FileNotFoundError:
    st.sidebar.error("Logo not found. Please make sure 'logo.png' is in the same directory.")

st.sidebar.title("🧠 Study Buddy")

# Get selected mode
mode = st.sidebar.radio("🌈 Choose Your Vibe:", ["Low Stimulation 🧘", "Dopamine Boost ✨"])
selected_colors = color_schemes[mode]

# Apply custom CSS
st.markdown(
    f"""
    <style>
        body {{
            background: {selected_colors["background"]};
            color: {selected_colors["text"]};
            font-family: 'Poppins', sans-serif; /* Example font */
            line-height: 1.6;
        }}
        .stApp {{
            background: {selected_colors["background"]};
        }}
        .stSidebar {{
            background: {selected_colors["sidebar"]};
            color: {selected_colors["text"]};
            border-radius: 10px; /* Rounded corners for sidebar */
            padding: 1em;
            box-shadow: 0 0 10px rgba(0,0,0,0.2); /* Subtle shadow */
        }}
        /* Top of the app */
        [data-testid="stHeader"] {{
            background: {selected_colors["header"]};
        }}
        [data-testid="stVerticalBlock"] {{
            background-color: transparent;
            padding: 0;
            border-radius: 0;
            max-width: 600px; /* Set max width for chat */
            margin: 0 auto; /* Center the chat */
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {selected_colors["text"]};
        }}
        h3 {{
            font-size: 2.5em; /* Increase size of H3 headers */
            text-align: center; /* Center the h3 text */
        }}
        .stMarkdown {{
            background-color: transparent;
            padding: 0;
        }}

        /* Frame around text input boxes */
        .stTextInput>label:first-child {{
            border: 2px solid {selected_colors["frame"]};
            border-radius: 5px;
            padding: 0.5em; /* Add some space around the label */
            display: block; /* Make the label a block element */
            margin-bottom: 0.5em; /* Add some space below the label */
            background-color: {selected_colors["highlight"]}; /*Highlight text boxes*/
        }}
        .stTextInput>div>div>input {{
            border: 1px solid {selected_colors["frame"]};
            border-radius: 5px;
            padding: 0.5em;
        }}

        /* Frame around select boxes */
        .stSelectbox>label:first-child {{
            border: 2px solid {selected_colors["frame"]};
            border-radius: 5px;
            padding: 0.5em;
            display: block;
            margin-bottom: 0.5em;
            background-color: {selected_colors["highlight"]}; /*Highlight select boxes*/
        }}
        .stSelectbox>div>div>div {{
            border: 1px solid {selected_colors["frame"]};
            border-radius: 5px;
            padding: 0.5em;
        }}

        /* Button Styling */
        .stButton>button {{
            color: {selected_colors["text"]};
            background-color: #FFFFFF; /* White background */
            padding: 0.75em 1.25em; /* Slightly larger padding */
            border-radius: 25px; /* More rounded buttons */
            box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* Stronger shadow */
            transition: transform 0.2s, box-shadow 0.2s; /* Smooth transition on hover */
            border: none; /* Remove border */
            font-weight: 600; /* Bolder font */
        }}

        .stButton>button:hover {{
            transform: translateY(-2px); /* Move up slightly on hover */
            box-shadow: 0 6px 12px rgba(0,0,0,0.3); /* Stronger shadow on hover */
        }}

        /* Subtle background animation */
        body {{
            background: {selected_colors["background"]};
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }}

        @keyframes gradient {{
            0% {{
                background-position: 0% 50%;
            }}
            50% {{
                background-position: 100% 50%;
            }}
            100% {{
                background-position: 0% 50%;
            }}
        }}

    </style>
    """,
    unsafe_allow_html=True
)


# --- Chat Interface ---
st.markdown(f"<h3 style='text-align: center; color:{selected_colors['text']};'>💡 Study Chatbot 🤖</h3>", unsafe_allow_html=True)

# Initialize messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages
for message in st.session_state["messages"]:
    role = "You 👤:" if message["role"] == "user" else "Buddy 📚:"
    st.markdown(f"**{role}** {message['content']}")

# ---- USER INPUT ----
if "last_input" not in st.session_state:
    st.session_state["last_input"] = None

user_input = st.text_input("💬 Type your message here:", key="user_input", value="", label_visibility="collapsed")


# Add a "Send" button to trigger input processing
if st.button("Send") and user_input:
    st.session_state["last_input"] = user_input 
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.spinner("🤖 ADHD Buddy is thinking..."):
        time.sleep(1)
        bot_reply = generate_response(user_input)

    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
    st.rerun()


# --- Sidebar Organization ---
with st.sidebar:
    
    st.markdown("---")
    
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
    
    col1, col2, col3 = st.sidebar.columns(3)
    
    def update_timer_display():
        """Updates the timer display and progress bar."""
        if st.session_state["timer_running"] and st.session_state["start_time"]:
            elapsed_time = (datetime.now() - st.session_state["start_time"]).total_seconds()
            remaining_time = max(st.session_state["timer_seconds"] - int(elapsed_time), 0)

            mins, secs = divmod(remaining_time, 60)
            timer_display.markdown(f"**Time Left:** {int(mins)} min {int(secs)} sec")
            progress_bar.progress(max(0, remaining_time / st.session_state["timer_seconds"]))

            if remaining_time <= 0:
                st.sidebar.warning("🚨 Time for a break! 🚨")
                st.session_state["timer_running"] = False  # Stop timer
                st.session_state["start_time"] = None  # Reset start time

        else:
            mins, secs = divmod(st.session_state['timer_seconds'], 60)
            timer_display.markdown(f"**Time Left:** {int(mins)} min {int(secs)} sec")
            progress_bar.progress(0)

    def start_timer(duration):
        """Starts the countdown timer and stores start time."""
        st.session_state["timer_seconds"] = duration
        st.session_state["start_time"] = datetime.now()
        st.session_state["timer_running"] = True

    # Buttons to control the timer
    with col1:
        if st.button("Start"):
            start_timer(session_seconds)

    with col2:
        if st.button("Break"):
            start_timer(300)  # 5-minute break

    with col3:
        if st.button("Stop"):
            st.session_state["timer_running"] = False
            st.session_state["start_time"] = None
    
    st.markdown("---")
    st.subheader("✅ Task Manager")

    # Task state variables
    if "tasks" not in st.session_state:
        st.session_state["tasks"] = []
    if "finished_tasks" not in st.session_state:
        st.session_state["finished_tasks"] = []

    # Task emojis
    task_emojis = {
        "urgent": "❗",
        "creative": "✏️",
        "study": "📖",
        "general": "✔️"
    }

    # Add new task
    new_task = st.text_input("Add a task:", key="new_task")
    task_type = st.selectbox("Category:", ["urgent", "creative", "study", "general"], key="task_type")
    deadline = st.date_input("Deadline:", min_value=datetime.today(), key="deadline")

    if st.button("Add to List", key="add_task"):
        if new_task:
            emoji = task_emojis.get(task_type, "✔️")
            task_entry = f"{emoji} {new_task} (Due: {deadline.strftime('%b %d')})"
            st.session_state["tasks"].append(task_entry)

    # Categorize tasks
    sorted_tasks = {"urgent": [], "creative": [], "study": [], "general": []}

    for task in st.session_state["tasks"]:
        for category in task_emojis.keys():
            if task.startswith(task_emojis[category]):
                sorted_tasks[category].append(task)

    # Sort tasks within each category by deadline
    def extract_deadline(task):
        try:
            # Extract date from the task string (format: "Due: MMM DD")
            deadline_part = task.split("(Due: ")[-1].strip(")")
            return datetime.strptime(deadline_part, "%b %d")
        except ValueError:
            return datetime.max  # If no valid date, push to the end

    for category in sorted_tasks:
        sorted_tasks[category].sort(key=extract_deadline)

    # Display current tasks
    st.subheader("Current Tasks")
    for category in ["urgent", "study", "general", "creative"]:
        if sorted_tasks[category]:
            st.markdown(f"**{category.capitalize()} Tasks:**")
            for i, task in enumerate(sorted_tasks[category]):
                col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
                # Use st.write or st.markdown for left alignment
                col1.markdown(task)
                if col2.button("✅", key=f"complete_{category}_{i}"):
                    st.session_state["tasks"].remove(task)
                    st.session_state["finished_tasks"].append(task)
                    st.rerun()  # Refresh to update the display
                if col3.button("❌", key=f"remove_{category}_{i}"):  # Ensure unique key
                    st.session_state["tasks"].remove(task)

    # Display finished tasks
    st.subheader("Completed Tasks")
    if st.session_state["finished_tasks"]:
        for task in st.session_state["finished_tasks"]:
            st.markdown(f"✔️ {task}")
            
    if st.button("Clear Completed Tasks", key="clear_finished"):
        st.session_state["finished_tasks"] = []
        st.rerun()

    st.markdown("---")

    st.subheader("Notes 📝")
    if "sticky_notes" not in st.session_state:
        st.session_state["sticky_notes"] = []

    note = st.text_input("Jot a thought:", key="new_note")
    if st.button("Add Note", key="add_note") and note:
        st.session_state["sticky_notes"].append(note)

    if st.button("Clear Notes", key="clear_notes"):
        st.session_state["sticky_notes"] = []

    st.subheader("My Notes")
    for saved_note in st.session_state["sticky_notes"]:
        st.markdown(f"⏺️ {saved_note}")
    
    st.markdown("---")


    # ---- POMODORO TIMER DISPLAY ----

    # 🔹 Non-blocking real-time update using Streamlit's built-in rerun mechanism
    if st.session_state["timer_running"]:
        update_timer_display()
        time.sleep(1)  # Wait 1 second before updating again
        st.rerun()  
    # Forces script to rerun, but keeps UI elements

        st.markdown("---")

# --- Session Summary ---
    st.subheader("📊 Session Summary")
    if st.button("End Session & Get Summary", key="end_session"):
        if st.session_state["study_start_time"]:
            study_time = datetime.now() - st.session_state["study_start_time"]
            minutes_studied = study_time.seconds // 60
            completed_tasks = len(st.session_state["finished_tasks"])

            study_tips = [
                "Summarize what you learned. 📝",
                "Use active recall. 🤔",
                "Break into chunks. 🧩",
                "Use visuals. 🗺️",
                "Take breaks! 😴"
            ]

            st.sidebar.markdown(f"<h4 style='color:{selected_colors['text']};'>Session Review</h4>", unsafe_allow_html=True)
            st.sidebar.markdown(f"**Focus Time:** {minutes_studied} mins")
            st.sidebar.markdown(f"**Tasks Done:** {completed_tasks}")
            st.sidebar.markdown(f"<h5 style='color:{selected_colors['text']};'>Tips:</h5>", unsafe_allow_html=True)
            for tip in study_tips[:3]:
                st.sidebar.markdown(f"✔️ {tip}")

            # Reset session
            st.session_state["study_start_time"] = None
            st.session_state["finished_tasks"] = []
            st.session_state["messages"] = []
            st.session_state["timer_seconds"] = 1500
            st.rerun()
        else:
            st.sidebar.warning("Start focus session first!")
        

# --- Clear Chat Button ---
if st.button("Clear Chat"):
    st.session_state["messages"] = []
    st.rerun()