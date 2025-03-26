
import google.generativeai as genai
import os
import time
import pandas as pd
from google.api_core.exceptions import ResourceExhausted
import ast


# Configure Gemini API (replace with your actual Gemini API key)
genai.configure(api_key="AIzaSyDO7BHvUTLChkYFUlCSJK3eDUDN2zQj85E")

def suggest_remediation_gemini(flags, max_retries=3, delay=1.5):

    prompt = (

        "You are a financial compliance expert. A transaction has been flagged for the following issues: "
        + ", ".join(flags)
        + ". Provide brief remediation actions including adjustments, explanations, and compliance steps. If the flag is empty, the transaction doesnt need remediation advice, transaction is safe!"
    )

    model = genai.GenerativeModel('models/gemini-1.5-pro-002')

    for attempt in range(max_retries):
        try:
            if(flags==[]):
                response="Transaction is safe!"
                return response
            else:
                response = model.generate_content(prompt)
                time.sleep(delay)  # Add delay to avoid hitting rate limits
                return response.text
        except ResourceExhausted:
            wait_time = delay * (2 ** attempt)  # Exponential backoff (1.5s, 3s, 6s...)
            print(f"Rate limit exceeded. Retrying in {wait_time:.2f} seconds...")
            time.sleep(wait_time)

    return "Error: Exceeded API rate limits. Try again later."

def add_remediation_to_data(data):

    print("add_remediation_to_data")
     # Limit the data subset (optional)
    data=data.iloc[:6,:]
    def get_flags(validation_data):
        if isinstance(validation_data, dict):
            return validation_data.get("flags", None)  # If already a dictionary, extract directly

        if not isinstance(validation_data, str) or pd.isna(validation_data):
            return None  # Handle missing values or non-string cases

        try:
            # Remove extra surrounding quotes if necessary
            if validation_data.startswith("\"{") and validation_data.endswith("}\""):
                validation_data = validation_data[1:-1]  # Remove extra quotes
            
            validation_dict = ast.literal_eval(validation_data)  # Convert string to dictionary
            return validation_dict.get("flags", None)
        
        except (SyntaxError, ValueError):  
            return None  # Handle incorrect formats
    # Apply the function with rate limiting
    data["Remediation_Advice"] = [
        suggest_remediation_gemini(get_flags(rep)) for rep in data["Validation Results"]
    ]

    # Save the results
    data.to_csv(r"D:\DataProfiling_TechnologyHackathon\data_profiling-main\data_profiling-main\data\remediated_data.csv", index=False, header=True)
    return data

if __name__ == "__main__":
    # Load validated transactions
    df = pd.read_csv(r"D:\DataProfiling_TechnologyHackathon\data_profiling-main\data_profiling-main\data\validated_transactions.csv")

    # Process the data with rate-limited API calls
    df = add_remediation_to_data(df)

    print("Remediation actions assigned. Sample results:")
    print(df[["Transaction_Amount", "Validation_Report", "Remediation_Advice"]].head())
