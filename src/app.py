import streamlit as st
import pandas as pd
import openpyxl
import google.generativeai as genai
from main import run_pipeline
loan_data=None
# Read Regulatory Rules File
genai.configure(api_key="AIzaSyA_iDA7f1mC7dCexRKD8zirBDb3uG0FVyE")
with open(r"C:\Users\krith\hackathon\data_profiling\data\fed_regulations.txt", 'r') as file:
    regulatory_rules = file.read()
loan_data=None
# Streamlit Page Configuration
st.set_page_config(page_title="Regulatory Data Validation", layout="wide")

st.title("📊 Regulatory Data Validation & Profiling")

st.subheader("Upload Corporate Loan Data (Optional)")

# File Upload Section
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

# Initialize session state variables

if "enable_chat" not in st.session_state:
    st.session_state.enable_chat = False
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

# Process the uploaded file if present
if uploaded_file:
    st.session_state.file_uploaded = True
    if uploaded_file.name.endswith(".csv"):
        loan_data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        loan_data = pd.read_excel(uploaded_file)


    # Show validation rules preview
st.write("### Validation Rules Preview:")
st.write(regulatory_rules)

# Display Action Buttons

if st.button("➕ Add/Refine Rule"):
        st.session_state.enable_chat = True  # Enable chat
if "context" not in st.session_state:
        st.session_state.context = ""


# Chat Interface (Only Enabled When "Add/Refine Rule" is Clicked)
if st.session_state.enable_chat:
    st.write("### 💬 Chat with AI to Add/Refine Rules")
    col_chat, col_report = st.columns([4, 1])
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Chat...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        model = genai.GenerativeModel('models/gemini-1.5-pro')
        chat_prompt = f'''You are an expert in Corporate Loans Regulations as per the Federal Reserve. Take the the user prompt to add or refine rules to the given regulatory rules:{regulatory_rules} user prompt:{user_input}.
        Output: If user wants to add rule respond "Adding" followed by the rule. If the user want to refine, change or modify the rule respond "Refining" followed by the updated rule ONLY.
        If the user prompt is not relevant to the given regulatory rules for corporate loans : ""Please Add or refine rules relevant to corporate loan.'''
        chat_response = model.generate_content(chat_prompt).text

        if "Adding" in chat_response:
            st.session_state.context=st.session_state.context+"add "+chat_response
        elif "Refining" in chat_response:
            st.session_state.context=st.session_state.context+"refine "+chat_response
        st.session_state.chat_history.append({"role": "assistant", "content": chat_response})
        with st.chat_message("assistant"):
            st.markdown(chat_response)

if st.button("Generate Report"):
            result_data = run_pipeline(loan_data,st.session_state.context)
            csv_data = result_data.to_csv(index=False)
            st.download_button(
                label="Download Results as CSV",
                data=csv_data,
                file_name="profiling_results.csv",
                mime="text/csv"
            )
        # AI Chat Model (Commented for now, uncomment if needed)
        # model = genai.GenerativeModel('models/g
