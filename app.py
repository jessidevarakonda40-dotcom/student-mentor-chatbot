import os
import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# ===== API KEY =====
os.environ["GOOGLE_API_KEY"] = "AIzaSyC074kzYKrbjKyoipuF-NX4WfKfZ2PGkzs"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-2.0-flash")

# ===== STREAMLIT UI =====
st.set_page_config(page_title="Student Mentor – Brutal Mode", page_icon="🔥")
st.title("🔥 Student Mentor Chatbot – Brutal Mode")

# ===== SESSION STATE =====
if "messages" not in st.session_state:
    st.session_state.messages = []

if "profile" not in st.session_state:
    st.session_state.profile = {
        "branch": None,
        "year": None,
        "weakness": None
    }

# ===== DISPLAY OLD MESSAGES =====
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ===== USER INPUT =====
user_input = st.chat_input("Type honestly...")

def get_brutal_response(profile, user_text):
    prompt = f"""
You are a brutal but helpful student mentor.

Student profile:
Branch: {profile['branch']}
Year: {profile['year']}
Weakness: {profile['weakness']}

Student says: {user_text}

Reply brutally but helpfully.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except ResourceExhausted:
        return "⚠️ API limit reached. Try again later."

# ===== CHAT LOGIC =====
if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):
        if st.session_state.profile["branch"] is None:
            st.session_state.profile["branch"] = user_input
            reply = "Which year are you in?"

        elif st.session_state.profile["year"] is None:
            st.session_state.profile["year"] = user_input
            reply = "What are you weak at?"

        elif st.session_state.profile["weakness"] is None:
            st.session_state.profile["weakness"] = user_input
            reply = "Profile saved. Now talk."

        else:
            reply = get_brutal_response(
                st.session_state.profile,
                user_input
            )

        st.write(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

   
