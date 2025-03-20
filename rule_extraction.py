import openai

class RuleExtraction:
    def __init__(self, api_key):
        openai.api_key = api_key

    def extract_rules(self, regulatory_text):
        prompt = f"Extract clear data profiling rules from the following regulatory text:\n{regulatory_text}"
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=500
            )
            return response['choices'][0]['message']['content'].strip()
        
        except Exception as e:
            print(f"Error extracting rules: {e}")
            return None