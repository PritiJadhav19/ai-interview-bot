import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Interview Prep Chatbot", page_icon="💬")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("💬 AI Chatbot for Interview Prep")
st.write("Get ready for your next interview with AI-powered practice questions!")

# Select job role
job_role = st.selectbox("🎯 Select Job Role", ["Frontend Developer", "Data Analyst", "Software Engineer", "Product Manager"])

# Initialize conversation state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Start interview automatically once role is selected and no previous conversation
if job_role and not st.session_state.conversation:
    st.write(f"🧠 Starting interview for: **{job_role}** ...")
    
    start_prompt = f"You are an interviewer for a {job_role}. Start the interview by asking your first question."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional interviewer who evaluates answers and asks insightful follow-up questions."},
            {"role": "user", "content": start_prompt},
        ]
    )
    
    first_question = response.choices[0].message.content
    st.session_state.conversation.append(("Bot", first_question))

# Text input for user's answer
user_input = st.text_input("💬 Your Answer (press Enter to submit)")

if user_input:
    st.session_state.conversation.append(("You", user_input))
    prompt = f"You are an interviewer for a {job_role}. Ask the next question or give feedback on: {user_input}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional interviewer that evaluates answers and asks follow-up questions."},
            {"role": "user", "content": prompt},
        ]
    )
    
    bot_reply = response.choices[0].message.content
    st.session_state.conversation.append(("Bot", bot_reply))

# Display conversation
st.markdown("---")
for speaker, text in st.session_state.conversation:
    st.markdown(f"**{speaker}:** {text}")
