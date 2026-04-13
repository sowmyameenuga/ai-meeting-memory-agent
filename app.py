import streamlit as st
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- MEMORY ----------------
try:
    with open("memory.json", "r") as f:
        memory = json.load(f)
except:
    memory = []

def save_memory():
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=2)

def add_memory(text):
    memory.append({"text": text})
    save_memory()

# ---------------- AI SEARCH (SMART) ----------------
def get_answer(query):
    if not memory:
        return None

    docs = [item["text"] for item in memory]

    # Combine query + memory
    all_text = docs + [query]

    vectorizer = TfidfVectorizer().fit_transform(all_text)
    vectors = vectorizer.toarray()

    query_vec = vectors[-1]
    memory_vecs = vectors[:-1]

    similarities = cosine_similarity([query_vec], memory_vecs)[0]

    best_index = similarities.argmax()
    best_score = similarities[best_index]

    if best_score < 0.2:
        return None

    return docs[best_index]

# ---------------- UI ----------------
st.set_page_config(page_title="AI Memory Agent", page_icon="🧠")
st.title("🧠 AI Meeting Memory Agent (Smart Version)")

user_input = st.text_input("💬 Ask or add something")

if st.button("🚀 Submit"):
    if user_input:

        text = user_input.strip()

        # ❌ Don't store questions
        is_question = (
            "?" in text or
            text.lower().startswith(("who", "what", "when", "where", "how"))
        )

        if is_question:
            st.info("🔎 Thinking using AI memory...")

            answer = get_answer(text)

            if answer:
                st.success(f"👉 Answer: {answer}")
            else:
                st.warning("🤔 No relevant memory found")

        else:
            add_memory(text)
            st.success("🧠 Learned and stored!")

    else:
        st.warning("Please enter something")

# ---------------- VIEW MEMORY ----------------
if st.button("📚 Show Memory"):
    st.subheader("🧠 Stored Knowledge")

    for item in memory:
        st.write("•", item["text"])

# ---------------- CLEAR MEMORY ----------------
if st.button("🧹 Clear Memory"):
    memory.clear()
    save_memory()
    st.success("Memory cleared!")