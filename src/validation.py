import importlib.util

from script_cleaner import clean_validation_script

def load_validation_script(script_path):
    """Dynamically loads the cleaned validation script."""
    with open(script_path, "r") as f:
        raw_script = f.read()
    cleaned_script = clean_validation_script(raw_script)
    
    # Save the cleaned version (optional)
    with open(script_path, "w") as f:
        f.write(cleaned_script)
    
    spec = importlib.util.spec_from_file_location("extracted_rules", script_path)
    validation_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validation_module)
    return validation_module

def validate_transactions(data, script_path="Team_Repo2\data\extracted_rules.py"):
    """
    Validates all transactions using the dynamically extracted (and cleaned) validation rules.
    Returns the DataFrame with a new column 'Validation_Report'.
    """
    
    validation_module = load_validation_script(script_path)
    data["Validation_Report"] = data.apply(lambda row: validation_module.validate_transaction(row.to_dict()), axis=1)
    data.to_csv(r"Team_Repo2\data\validated_transactions.csv", index=False)
    return data

if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("Team_Repo2\data\processed_transactions.csv")
    validated_df = validate_transactions(df)
    print("Sample Validation Reports:")
    print(validated_df["Validation_Report"].head())
