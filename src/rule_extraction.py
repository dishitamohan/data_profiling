import google.generativeai as genai

genai.configure(api_key="AIzaSyDO7BHvUTLChkYFUlCSJK3eDUDN2zQj85E")

def extract_rules_gemini(instruction_text):
    model = genai.GenerativeModel('models/gemini-1.5-pro-002')
    response = model.generate_content(instruction_text)
    with open("D:\DataProfiling_TechnologyHackathon\data_profiling-main\data_profiling-main\data\extracted_rules.py", "w") as f:
        f.write(response.text)
    print(response.text)
    return response.text
