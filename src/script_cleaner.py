import re

def clean_validation_script(script):
    """
    Cleans the extracted validation script by removing extra text.
    It keeps only the executable code starting from the first 'import' statement,
    and removes any trailing lines that consist solely of triple backticks.
    """
    lines = script.split('\n')
    cleaned_lines = []
    code_started = False
    for line in lines:
        # Start collecting lines once we hit the first 'import' statement
        if re.match(r'^import\s+\w+', line):
            code_started = True
        if code_started:
            cleaned_lines.append(line)
    
    # Remove the last line if it is exactly triple backticks
    if cleaned_lines and cleaned_lines[-1].strip() == "```":
        cleaned_lines = cleaned_lines[:-1]
        
    return "\n".join(cleaned_lines)

if __name__ == "__main__":
    # Example usage
    with open("Team_Repo2\data\extracted_rules.py", "r") as f:
        script = f.read()
    cleaned_script = clean_validation_script(script)
    print("Cleaned Script:\n", cleaned_script)
