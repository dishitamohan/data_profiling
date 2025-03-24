import streamlit as st
import pandas as pd
import openpyxl
import google.generativeai as genai
from main import run_pipeline
genai.configure(api_key="AIzaSyBWQCOCpMDo4A0cUNQ7rY4v_gQJDVGNRAs")

# Configure Gemini API (Replace with actual API Key)
# genai.configure(api_key="YOUR_GEMINI_API_KEY")

st.set_page_config(page_title="Regulatory Data Validation", layout="wide")

st.title("📊 Regulatory Data Validation & Profiling")
regulatory_text=""
result_data=None
# 1️⃣ Upload Regulatory Instructions
st.subheader("Upload Validation rules Data")
reg_file = st.file_uploader("Upload Regulatory Instructions (TXT, DOCX, PDF)", type=["txt", "docx", "pdf"])

if reg_file:
    st.success(f"Uploaded `{reg_file.name}` successfully!")

    # Convert uploaded file to text (Handle PDF/DOCX parsing here if needed)
    regulatory_text = reg_file.read().decode("utf-8")

    # Store extracted rules in session state for refinement
    st.session_state["regulatory"] = regulatory_text

st.subheader("Upload Transaction Data")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Check file type and read accordingly
    if uploaded_file.name.endswith(".csv"):
        transactions = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        transactions = pd.read_excel(uploaded_file)
    transactions.to_csv(r"C:\Users\krith\hackathon\data_profiling\data\transactions.csv",index=False)
    # Display DataFrame
    st.write("### Transaction Data Preview:")
    st.dataframe(transactions.head())  # Show first few rows

    # Save to session state for further processing
    st.session_state["transactions"] = transactions
# 2️⃣ Interactive Chat for Refining Rules
st.subheader("💬 Chat to Refine Validation Rules")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Chat...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    validation_prompt=""
    if  not regulatory_text=="":
        validation_prompt=f"Validation rules: {regulatory_text}"

    # Get AI-generated response

    model = genai.GenerativeModel('models/gemini-1.5-pro')
    chat_prompt = f"You are an experienced regulatory and compliance agent for banks. Discuss and help the user refine validation rules based on user prompt and validation rules for the user data. DO NOT provide any code in your response. Instead, explain the validation logic, rules, and necessary steps in plain language. User input: {user_input}. User data:{transactions.head()}. {validation_prompt}"
    chat_response = model.generate_content(chat_prompt).text
    st.session_state.chat_history.append({"role": "assistant", "content": chat_response})
    with st.chat_message("assistant"):
        st.markdown(chat_response)

    # Store refined rules
    # st.session_state["refined_rules"] = chat_response

# # 3️⃣ User Confirms Rules

if st.button("Run Data Profiling & Download Report"):
    result_data=run_pipeline(st.session_state.chat_history,regulatory_text)
    csv_data = result_data.to_csv(index=False)
    st.download_button(
        label="Download Results as CSV",
        data=csv_data,
        file_name="profiling_results.csv",
        mime="text/csv"
            )