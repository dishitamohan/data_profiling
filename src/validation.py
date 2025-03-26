import importlib.util

from script_cleaner import clean_validation_script
from rules_orignal import validate_transaction_file

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

def validate_transactions(data,flag):
    """
    Validates all transactions using the dynamically extracted (and cleaned) validation rules.
    Returns the DataFrame with a new column 'Validation_Report'.
    """
        
    try:
        if (flag==True):
            script_path_gemini =r"D:\DataProfiling_TechnologyHackathon\data_profiling-main\data_profiling-main\data\extracted_rules.py"
            validation_module_gemini = load_validation_script(script_path_gemini)
            # output_csv_final = validation_module_gemini.validate_transaction(output_csv,seen_ids = set(),seen_facility_ids = set())
            data["Validation Results"] = data.apply(lambda row: validation_module_gemini.validate_transaction(row.to_dict(),seen_ids = set(),seen_facility_ids = set()), axis=1)
    except Exception as e:
        print(f"Unexpected error occured:",e)
        pass
    # validation_module = load_validation_script(script_path)
    output_csv = validate_transaction_file(data)
    # output_csv.to_csv(r"D:\DataProfiling_TechnologyHackathon\data_profiling-main\data_profiling-main\data\validated_transactions.csv", index=False)
    

    
    output_csv_final =output_csv
    output_csv_final.to_csv(r"D:\DataProfiling_TechnologyHackathon\data_profiling-main\data_profiling-main\data\validated_transactions.csv", index=False)

        
    return output_csv_final

if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv(r"D:\DataProfiling_TechnologyHackathon\data_profiling-main\data_profiling-main\data\processed_transactions.csv")
    validated_df = validate_transactions(df)
    print("Sample Validation Reports:")
    print(validated_df["Validation_Report"].head())
