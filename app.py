import streamlit as st
from langchain_groq import ChatGroq
from PyPDF2 import PdfReader

# UI Setup
st.set_page_config(page_title="AI Doc Insight", page_icon="🤖")
st.title("📄 AI Document Insight Tool")
st.write("अपने PDF से बात करें - 15 साल के अनुभव की पहली AI झलक!")

# Sidebar for API Key
with st.sidebar:
    groq_api_key = st.text_input("Enter Groq API Key:", type="password")
    st.info("आप अपनी फ्री Key यहाँ से ले सकते हैं: https://console.groq.com/keys")

# File Uploader
uploaded_file = st.file_uploader("अपनी PDF फाइल अपलोड करें", type="pdf")

if uploaded_file and groq_api_key:
    # PDF से टेक्स्ट निकालना
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    # User Question
    user_question = st.text_input("इस फाइल के बारे में कुछ पूछें:")

    if user_question:
        try:
            # AI Model Setup
            llm = ChatGroq(groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")
            
            # Prompt Engineering
            prompt = f"Context: {text[:5000]}\n\nQuestion: {user_question}\n\nAnswer accurately based on the context."
            
            response = llm.invoke(prompt)
            st.success("AI का जवाब:")
            st.write(response.content)
        except Exception as e:
            st.error(f"Error: {e}")

elif not groq_api_key:
    st.warning("कृपया साइडबार में अपनी Groq API Key डालें।")