# ai-meeting-memory-agent

This project is an AI-powered meeting assistant that remembers past conversations and answers questions using memory.

**Features**
 Stores meeting data
- Remembers tasks and roles
- Answers questions like:
  - Who is handling backend?
  - Who is attending meeting?
- Memory-based retrieval system
  
**How it works**
1. User enters meeting information
2. System stores it in memory
3. User asks a question
4. System searches memory and returns answer

**Tech Stack**
- Python
- Streamlit
- Scikit-learn (TF-IDF)

**Run locally**
pip install -r requirements.txt
streamlit run app.py
