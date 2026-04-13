import streamlit as st
import json
from groq import Groq

# =========================
# 🔐 GROQ API KEY
# =========================
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# =========================
# 🧠 LOAD MEMORY
# =========================
try:
    with open("memory.json", "r") as f:
        memory = json.load(f)
except:
    memory = []

# =========================
# 💾 SAVE MEMORY
# =========================
def save_memory():
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=2)

# =========================
# ➕ ADD MEMORY
# =========================
def add_memory(text):
    memory.append({"text": text})
    save_memory()

# =========================
# 📚 GET MEMORY CONTEXT
# =========================
def get_memory_context():
    return "\n".join([m["text"] for m in memory[-20:]])

# =========================
# 🧠 QUESTION CHECK
# =========================
def is_question(text):
    text = text.lower()
    return (
        "?" in text or
        text.startswith(("who", "what", "when", "where", "how"))
    )

# =========================
# 🤖 GROQ AI FUNCTION
# =========================
def ask_llm(question):
    memory_text = get_memory_context()

    prompt = f"""
You are an AI Meeting Assistant.

Use MEMORY to answer the question.

MEMORY:
{memory_text}

QUESTION:
{question}

Rules:
- If answer exists in memory, use it
- If not found, say "Not found in memory"
- Be short and clear
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

# =========================
# 🎨 STREAMLIT UI
# =========================
st.set_page_config(page_title="AI Meeting Memory Agent", page_icon="🧠")

st.title("🧠 AI Meeting Memory Agent (Groq + Memory)")

user_input = st.text_input("💬 Enter meeting note or question")

col1, col2 = st.columns(2)

# =========================
# 🚀 SUBMIT BUTTON
# =========================
with col1:
    if st.button("🚀 Submit"):
        if user_input:

            if is_question(user_input):
                st.info("🔎 Thinking using Groq AI + Memory...")
                answer = ask_llm(user_input)
                st.success(f"👉 Answer: {answer}")

            else:
                add_memory(user_input)
                st.success("🧠 Stored in memory!")

        else:
            st.warning("Please enter something")

# =========================
# 📌 SHOW MEMORY
# =========================
with col2:
    if st.button("📌 Show Memory"):
        st.subheader("🧠 Stored Memory")

        if memory:
            for item in memory:
                st.write("•", item["text"])
        else:
            st.write("No memory found")

# =========================
# 🧹 CLEAR MEMORY
# =========================
if st.button("🧹 Clear Memory"):
    memory.clear()
    save_memory()
    st.success("Memory cleared!")
