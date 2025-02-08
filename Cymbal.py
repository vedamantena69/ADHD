import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Ensure API key exists
if not api_key:
    st.error("⚠️ API Key is missing! Make sure it's set in the .env file.")
    st.stop()

# Configure Google Generative AI
genai.configure(api_key=api_key)

# Function to generate chatbot response
def generate_response(user_input):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_input)
        return response.text if response and hasattr(response, "text") else "Oops! I couldn’t find an answer. Try again!"
    except Exception as e:
        return "⚠️ Error: Unable to process response. Check API Key & Internet Connection."

# ---- UI MODE SELECTION ----
st.sidebar.title("🎨 Customize Your Experience")
mode = st.sidebar.radio("🌈 Choose Your View:", ["🧘 Low Stimulation Mode", "🎉 Dopamine Mode"])

# ---- AESTHETIC STYLING ----
if mode == "🧘 Low Stimulation Mode":
    st.markdown("""
        <style>
            body { background-color: #FAFAFA; font-family: 'Inter', sans-serif; }
            .stApp { background: #FAFAFA; }
            .chat-container { background: white; padding: 20px; border-radius: 15px; box-shadow: 2px 2px 15px rgba(0,0,0,0.1); }
            .chat-message { font-size: 18px; font-weight: 500; margin-bottom: 10px; padding: 12px; border-radius: 12px; }
            .user { background: #E3F2FD; color: #0D47A1; }
            .bot { background: #E8F5E9; color: #2E7D32; }
            .stTextInput>div>div>input { font-size: 18px; padding: 12px; border-radius: 12px; border: 2px solid #D0D0D0; }
            .stButton>button { background: linear-gradient(90deg, #6A11CB, #2575FC); color: white; font-size: 16px; border-radius: 12px; padding: 10px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

elif mode == "🎉 Dopamine Mode":
    st.markdown("""
        <style>
            body { background: linear-gradient(to right, #FFD3A5, #FD6585); font-family: 'Poppins', sans-serif; }
            .stApp { background: linear-gradient(to right, #FFD3A5, #FD6585); }
            .title { font-size: 42px; font-weight: bold; color: #FFF; text-align: center; margin-bottom: 10px; }
            .subtitle { font-size: 18px; text-align: center; color: #FFF; opacity: 0.8; }
            .chat-container { background: rgba(255, 255, 255, 0.3); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px); }
            .chat-message { font-size: 20px; font-weight: bold; padding: 12px; border-radius: 12px; }
            .user { background: #FFEB3B; color: #333; }
            .bot { background: #B3E5FC; color: #01579B; }
            .stTextInput>div>div>input { font-size: 18px; padding: 12px; border-radius: 12px; border: 2px solid #FF80AB; }
            .stButton>button { background: linear-gradient(90deg, #FF80AB, #FF4081); color: white; font-size: 18px; border-radius: 12px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="title">✨ ADHD Chatbot 💖</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ask me anything! 🌈</p>', unsafe_allow_html=True)

# ---- CHAT HISTORY ----
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state["messages"]:
    role_class = "user" if message["role"] == "user" else "bot"
    role = "👤 You:" if message["role"] == "user" else "🤖 ADHD Buddy:"
    st.markdown(f"<p class='chat-message {role_class}'><b>{role}</b> {message['content']}</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---- USER INPUT ----
if "last_input" not in st.session_state:
    st.session_state["last_input"] = None

user_input = st.text_input("💬 Type your message here:")

if user_input and st.session_state["last_input"] != user_input:
    st.session_state["last_input"] = user_input  
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.spinner("🤖 ADHD Buddy is thinking..."):
        time.sleep(1)
        bot_reply = generate_response(user_input)

    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
    st.rerun()

# ---- STICKY NOTES FEATURE ----
st.sidebar.subheader("📝 Sticky Notes")
if "sticky_notes" not in st.session_state:
    st.session_state["sticky_notes"] = []

note = st.sidebar.text_input("Write a quick thought:")
if st.sidebar.button("📌 Save Note") and note:
    st.session_state["sticky_notes"].append(note)

for saved_note in st.session_state["sticky_notes"]:
    st.sidebar.markdown(f"✅ {saved_note}")

if st.sidebar.button("🗑️ Clear Notes"):
    st.session_state["sticky_notes"] = []

# ---- BREAK REMINDER PROGRESS BAR ----
st.sidebar.subheader("⏳ Stay on Task")
task_progress = st.sidebar.slider("How long have you been working? (minutes)", 0, 60, 25)
if task_progress >= 25:
    st.sidebar.warning("🔔 Time for a 5-minute break!")

# ---- TASK MANAGEMENT (SMART PRIORITIZATION) ----
st.sidebar.subheader("🚀 Smart Task Prioritization")
tasks = {
    "Finish Homework": {"deadline": 2, "subtasks": 5},
    "Reply to Emails": {"deadline": 5, "subtasks": 2},
    "Study for Exam": {"deadline": 1, "subtasks": 7},
}

sorted_tasks = sorted(tasks.items(), key=lambda x: (x[1]["deadline"], x[1]["subtasks"]))

for task, details in sorted_tasks:
    st.sidebar.markdown(f"✅ **{task}** (Due in {details['deadline']} days, {details['subtasks']} steps)")

# ---- CLEAR CHAT BUTTON ----
if st.button("🧹 Clear Chat"):
    st.session_state["messages"] = []
    st.rerun()
