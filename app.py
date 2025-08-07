# chatbot_ui.py
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample training data
df = pd.read_excel("Training_Data.xlsx", sheet_name="Sheet1")
qa_list = df.to_dict(orient="records")

# Prepare data
questions = [item["question"] for item in qa_list]
answers = [item["answer"] for item in qa_list]

# Vectorize questions
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)


# Function to get best answer
def get_answer(user_query):
    query_vector = vectorizer.transform([user_query])
    similarity = cosine_similarity(query_vector, question_vectors)
    best_match_index = similarity.argmax()
    best_score = similarity[0][best_match_index]

    if best_score > 0.3:
        return answers[best_match_index]
    else:
        return "I'm not sure how to answer that. Can you rephrase?"


# Streamlit UI
st.title("🤖 Interactive ChatBot")
st.write("Please type your query in the below query box!!!!")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:")
    submitted = st.form_submit_button("Send")

    if submitted and user_input:
        response = get_answer(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response))

# Display chat history
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")
