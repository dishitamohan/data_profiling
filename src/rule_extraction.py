import google.generativeai as genai

genai.configure(api_key="AIzaSyCiGZUTd4MheB995OM9Yjk7cgeq6AmETNs")

def extract_rules_gemini(instruction_text):
    model = genai.GenerativeModel('models/gemini-1.5-pro-002')
    response = model.generate_content(instruction_text)
    with open("Team_Repo2\data\extracted_rules.py", "w") as f:
        f.write(response.text)
    return response.text
