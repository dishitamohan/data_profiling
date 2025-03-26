import re

def clean_validation_script(script):
    """
    Extracts and returns all Python code blocks from the given markdown text.
    If there are multiple code blocks, they will be concatenated with a newline in between.
    """
    # Regex pattern to match code blocks that start with ```python and end with ```
    pattern = r"```python(.*?)```"
    matches = re.findall(pattern, script, re.DOTALL)
    
    # Join all matches, stripping leading/trailing whitespace from each block.
    if matches:
        return "\n\n".join(match.strip() for match in matches)
    else:
        return ""
