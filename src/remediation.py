
import google.generativeai as genai
import os
import time
import pandas as pd
from google.api_core.exceptions import ResourceExhausted

# Configure Gemini API (replace with your actual Gemini API key)
genai.configure(api_key="AIzaSyA_iDA7f1mC7dCexRKD8zirBDb3uG0FVyE")

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

     # Limit the data subset (optional)
    data=data.iloc[:6,:]
    def get_flags(report):
        if isinstance(report, str):
            try:
                report_dict = eval(report)  # Convert string to dictionary
                print(report_dict.get("flags", []))
                return report_dict.get("flags", [])
            except Exception:
                return []
        elif isinstance(report, dict):
            return report.get("flags", [])
        return []

    # Apply the function with rate limiting
    data["Remediation_Advice"] = [
        suggest_remediation_gemini(get_flags(rep)) for rep in data["Validation_Report"]
    ]

    # Save the results
    data.to_csv(r"C:\Users\krith\hackathon\data_profiling\data\remediated_data.csv", index=False, header=True)
    return data

if __name__ == "__main__":
    # Load validated transactions
    df = pd.read_csv(r"D:\DataProfiling_TechnologyHackathon\Team_Repo2\data\validated_transactions.csv")

    # Process the data with rate-limited API calls
    df = add_remediation_to_data(df)

    print("Remediation actions assigned. Sample results:")
    print(df[["Transaction_Amount", "Validation_Report", "Remediation_Advice"]].head())