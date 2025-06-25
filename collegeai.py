import streamlit as st
import google.generativeai as genai
import re

# --- API Key ---
genai.configure(api_key="AIzaSyAdAHovI03L4vAPmTCVU5nLC7MCFth-vWk")  # Replace with your Gemini API key

# --- Load College Info from File ---
with open("college_info.txt", "r", encoding="utf-8") as file:
    college_info = file.read()

# --- Keyword List for Valid Questions ---
college_keywords = [
    "college", "sjc", "trichy", "hostel", "campus", "faculty", "lab","hi","hello","thank you",
    "library", "admission", "fees", "class", "sports", "placement",
    "infrastructure", "canteen", "wifi", "transport", "timing", "student",
    "department", "research", "seminar", "building", "autonomous", "ug", "pg"
]

# --- Helpers ---
def is_code_like(text):
    code_keywords = ['import', 'def', 'class', 'return', '=', '{', '}', '(', ')', ':']
    code_patterns = [
        r"^\s*def\s+\w+\(.*\):",
        r"^\s*class\s+\w+",
        r"\bimport\s+\w+",
        r"print\s*\(",
        r"[\{\};=]",
    ]
    return any(kw in text for kw in code_keywords) or any(re.search(p, text) for p in code_patterns)

def is_college_related(text):
    text = text.lower()
    return any(kw in text for kw in college_keywords)

# --- Streamlit UI ---
st.set_page_config(page_title="🎓 EduBot - SJC Chatbot", page_icon="🤖", layout="centered")

st.title("🎓 EduBot")
st.markdown("Ask any question about **St. Joseph's College, Trichy**")

user_input = st.text_input("Your Question", placeholder="e.g. What are the library hours?")

if user_input:
    if is_code_like(user_input):
        st.warning("⚠️ I can't process code. Please ask a question about the college.")
    elif not is_college_related(user_input):
        st.warning("❌ I can only answer questions about St. Joseph's College, Trichy.")
    else:
        with st.spinner("Thinking..."):
            try:
                model = genai.GenerativeModel("gemini-pro")
                prompt = f"""
You are 🎓 EduBot, a helpful assistant with detailed knowledge of the following college:

{college_info}

Now, answer this user's question in simple terms:
{user_input}
"""
                response = model.generate_content(prompt)
                st.success("🎓 EduBot says:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
