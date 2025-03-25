import streamlit as st
import pandas as pd
import openpyxl
import google.generativeai as genai
from main import run_pipeline
from remediation_pipeline import apply_remediation

# Configure API Key (Consider storing securely)
genai.configure(api_key="AIzaSyA_iDA7f1mC7dCexRKD8zirBDb3uG0FVyE")

# Read Regulatory Rules File
with open(r"C:\Users\krith\hackathon\data_profiling\data\fed_regulations.txt", 'r') as file:
    lines = file.read().strip().split("\n\n")
st.markdown("""
    <style>
    .bubble {
        display: block;
        background-color: #262730;
        color: white;
        padding: 15px;
        margin: 10px 0;
        border-radius: 15px;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit Page Configuration

st.title("📊 Regulatory Data Validation & Profiling")

# Initialize session state variables
if "enable_chat" not in st.session_state:
    st.session_state.enable_chat = False
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "context" not in st.session_state:
    st.session_state.context = ""
if "resp_type" not in st.session_state:
    st.session_state.resp_type = "validation"
if "result_data" not in st.session_state:
    st.session_state.result_data = pd.DataFrame()

# File Upload Section
uploaded_file = st.file_uploader("Upload a CSV or Excel file for CORPORATE LOAN", type=["csv", "xlsx"])
loan_data=pd.DataFrame()
# Process the uploaded file if present
if uploaded_file:
    st.session_state.file_uploaded = True
    if uploaded_file.name.endswith(".csv"):
        loan_data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        loan_data = pd.read_excel(uploaded_file)

# Show validation rules preview
st.write("### Validation Rules Preview:")
for rule in lines:
    st.markdown(f'<div class="bubble">{rule}</div>', unsafe_allow_html=True)

# Display Action Buttons
if st.button("➕ Add/Refine Rule"):
    st.session_state.enable_chat = True  # Enable chat
    st.session_state.resp_type = 'validation'
# Chat Interface (Only Enabled When "Add/Refine Rule" is Clicked)
if st.session_state.enable_chat:
    col_chat, col_report = st.columns([4, 1])
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if st.session_state.resp_type == 'validation':
        st.write("### 💬 Chat with AI to Add/Refine Rules")
        user_input = st.chat_input("Chat...")
        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            model = genai.GenerativeModel('models/gemini-1.5-pro')
            chat_prompt = f'''
            You are an expert in Corporate Loans Regulations as per the Federal Reserve. Take the user prompt to add or refine rules to the given regulatory rules:{regulatory_rules}
            User prompt:{user_input}.
            Output: If user wants to add a rule respond "Adding" followed by the rule. If the user wants to refine a rule, respond "Refining" followed by the updated rule ONLY.
            If the user prompt is not relevant to the given regulatory rules for corporate loans, respond with: "Please add or refine rules relevant to corporate loans."
            '''
            chat_response = model.generate_content(chat_prompt).text

            if "Adding" in chat_response or "Refining" in chat_response:
                st.session_state.context += " " + chat_response
            st.session_state.chat_history.append({"role": "assistant", "content": chat_response})
            with st.chat_message("assistant"):
                st.markdown(chat_response)

    else:  # Handling remediation report request
        user_input = st.chat_input("Enter the CustomerID")
        org_data = pd.read_csv(r"C:\Users\krith\hackathon\data_profiling\data\data.csv")
        cust_ids = org_data['CustomerID'].unique().tolist()
        all=False
        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            if user_input.strip().lower()=='all':
                all=True
            if user_input.strip().upper() not in cust_ids and user_input.strip().lower()!='all' :
                chat_response = "Provide the correct customer ID or type 'all' for complete report"
            else:
                id=user_input.strip()
                apply_remediation(st.session_state.result_data,id,all)
                pdf_path = '../data/remediation_Report.pdf'

                # Provide download button for PDF
                with open(pdf_path, "rb") as pdf_file:
                    pdf_data = pdf_file.read()

                st.download_button(
                    label="Download Remediation Report",
                    data=pdf_data,
                    file_name="remediation_Report.pdf",
                    mime="application/pdf"
                )
                chat_response="Your report is ready!"

            st.session_state.chat_history.append({"role": "assistant", "content": chat_response})
            with st.chat_message("assistant"):
                st.markdown(chat_response)

# Perform Validation button logic
if st.button("Perform Validation"):
    st.session_state.enable_chat = False  # Disable chat while validating
    st.session_state.result_data = run_pipeline(loan_data, st.session_state.context)
if not st.session_state.result_data.empty:
    if st.button("Generate Remediation Report"):
        st.session_state.enable_chat = True  # Now this properly enables chat
        st.session_state.resp_type = "remediation"  # Switch chat to remediation mode

# **Fix:** Enable chat when "Generate Remediation Report" is clicked
