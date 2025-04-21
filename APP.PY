import streamlit as st
import openai
import os

# 🧠 Setup your OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Or use st.secrets

st.set_page_config(page_title="AG Coach", layout="centered")

st.title("🧠 AG Coach — Agile Meeting Summarizer")
st.markdown("Paste a transcript from Teams or upload a file. I’ll summarize the meeting and pull out action items + blockers.")

# 📝 Transcript input
transcript_text = st.text_area("Transcript", height=300, placeholder="Paste your Teams transcript here...")

uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"])
if uploaded_file is not None:
    transcript_text = uploaded_file.read().decode("utf-8")

# 🔘 Summarize button
if st.button("Generate Summary") and transcript_text:
    with st.spinner("Thinking like a Scrum Master..."):
        prompt = f"""
        You are an Agile assistant. Given the transcript below, summarize the meeting:

        1. A brief summary (2–3 sentences)
        2. A list of action items (include assignees if available)
        3. A list of blockers (who is blocked, on what)
        4. Optional: Agile improvement tips

        Transcript:
        \"\"\"{transcript_text}\"\"\"
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message["content"]

        st.success("✅ Summary Ready!")
        st.text_area("📋 Agile Summary", result, height=400)

