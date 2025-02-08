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
    print(f"🔍 Sending input to Gemini AI: {user_input}")  # Debugging

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_input)

        if response and hasattr(response, "text"):
            print(f"✅ AI Response: {response.text}")  # Debugging
            return response.text
        else:
            print("⚠️ No valid response from AI.")
            return "Oops! I couldn’t find an answer. Try again!"
    except Exception as e:
        print(f"❌ AI Error: {e}")  # Debugging
        return "⚠️ Error: Unable to process response. Check API Key & Internet Connection."

# ---- UI MODE SELECTION ----
st.sidebar.title("🎨 Customize Your Experience")
mode = st.sidebar.radio("🌈 Choose Your View:", ["🧘 Low Stimulation Mode", "🎉 Dopamine Mode"])

# ---- AESTHETIC STYLING ----
if mode == "🧘 Low Stimulation Mode":
    st.markdown("""
        <style>
            body { background-color: #F5F5F5; font-family: 'Arial', sans-serif; }
            .chat-container { background-color: #FFFFFF; padding: 20px; border-radius: 15px; box-shadow: 5px 5px 15px rgba(0,0,0,0.1); }
            .chat-message { font-size: 20px; font-weight: bold; margin-bottom: 10px; }
            .stTextInput>div>div>input { font-size: 20px; padding: 10px; border-radius: 15px; border: 2px solid #aaa; }
        </style>
    """, unsafe_allow_html=True)

elif mode == "🎉 Dopamine Mode":
    st.markdown("""
        <style>
            body { background: linear-gradient(to right, #FCE7F3, #D9F4FF); font-family: 'Poppins', sans-serif; }
            .stApp { background: linear-gradient(to right, #FCE7F3, #D9F4FF); }
            .title { font-size: 48px; font-weight: bold; color: #FF69B4; text-align: center; margin-bottom: 10px; }
            .subtitle { font-size: 22px; text-align: center; color: #444; }
            .chat-container { background: rgba(255, 255, 255, 0.6); padding: 20px; border-radius: 20px; backdrop-filter: blur(10px); }
            .chat-message { font-size: 22px; font-weight: bold; padding: 12px; border-radius: 10px; }
            .bot { color: #007AFF; font-weight: bold; }
            .user { color: #FF69B4; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="title">✨ ADHD Chatbot 💖</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ask me anything! 🌈</p>', unsafe_allow_html=True)

# ---- CHAT HISTORY ----
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state["messages"]:
    role = "👤 **You:** " if message["role"] == "user" else "🤖 **ADHD Buddy:** "
    st.markdown(f"<p class='chat-message'><b>{role}</b> {message['content']}</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---- USER INPUT ----
if "last_input" not in st.session_state:
    st.session_state["last_input"] = None

user_input = st.text_input("💬 Type your message here:")

if user_input and st.session_state["last_input"] != user_input:
    # Store last processed input to prevent infinite reruns
    st.session_state["last_input"] = user_input  

    # Add user message to session state
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Generate response with delay
    with st.spinner("🤖 ADHD Buddy is thinking..."):
        time.sleep(1)
        bot_reply = generate_response(user_input)

    # Append bot response to session state
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

    # Prevent infinite reruns
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
    "Finish Homework": {"deadline": 2, "subtasks": 5},  # Deadline in days, subtasks count
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
