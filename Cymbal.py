import streamlit as st
import google.generativeai as genai
import os
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
    model = genai.GenerativeModel("gemini-pro")  # Using Gemini AI model
    response = model.generate_content(user_input)
    return response.text if response else "Sorry, I couldn't generate a response."

# Streamlit UI
st.title("Cymbal Direct Chatbot 🤖")
st.write("Ask me anything about Cymbal Direct!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Store the last processed user input to prevent infinite loops
if "last_input" not in st.session_state:
    st.session_state["last_input"] = ""

# Display chat history
for message in st.session_state["messages"]:
    role = "User" if message["role"] == "user" else "Cymbal Bot"
    st.markdown(f"**{role}:** {message['content']}")

# User input
user_input = st.text_input("You:", "")

# Process new input only if it's different from the last input
if user_input and user_input != st.session_state["last_input"]:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Generate AI response
    bot_reply = generate_response(user_input)

    # Append bot response to chat history
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

    # Update last processed input
    st.session_state["last_input"] = user_input

    # Refresh Streamlit UI
    st.rerun()
