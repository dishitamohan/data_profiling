import pandas as pd
from preprocessing import load_and_preprocess_data
from rule_extraction import extract_rules_gemini
from validation import validate_transactions
from anomaly_detection import detect_anomalies
from remediation import suggest_remediation_gemini,add_remediation_to_data

regulatory_rules=r'C:\Users\krith\hackathon\data_profiling\data\fed_regulations.txt'
data_meta=r'C:\Users\krith\hackathon\data_profiling\data\fed_metadata.txt'
with open(regulatory_rules, 'r') as file:
    regulatory_rules = file.read()
with open(data_meta, 'r') as file:
    data_meta = file.read()
with open(r"C:\Users\krith\hackathon\data_profiling\data\rules_orignal.py", "r") as file:
    python_code = file.read()
def_loan_data_path=r"C:\Users\krith\hackathon\data_profiling\data\data.csv"
def_loan_data=pd.read_csv(def_loan_data_path)

def run_pipeline(loan_data, context):
    flag=False
    if loan_data==None:
        loan_data=def_loan_data
    print("Step 1: Preprocessing Data...")
    df,seen_ids,seen_facility_ids= load_and_preprocess_data(loan_data)

    print("Step 2: Extracting Validation Rules...")
    instruction_text = f"""
     Role: "You are an expert in financial compliance and Python programming. Your task is to extract ALL the corporate loan validation rules from the given regulatory instructions. Use the user context if provided to add or refine existing rules in regulatory instructions.
     Generate a Python script that enforces ALL the rules.

     output: only executable code WITHOUT any kind of errors.
     Instructions:
     Generate a Python function that validates corporate loan details based on the following regulatory instructions. The function should return a structured validation report in dictionary format containing:
     valid (Boolean): Whether the transaction passes all checks.
     flags (List): A list of detected compliance issues.
     remediation (List): Suggested steps to fix or investigate flagged issues.

    Corpporate Loan data fields:
    {data_meta}

    Regulatory Instructions:
    {regulatory_rules}

    User context:
    {context}

    Example python code:
    {python_code}

     Remediation Actions:
     For flagged transactions, suggest appropriate actions, such as:
     Adjustments: Correcting discrepancies in amounts, currencies, and missing remarks.
     Explanations: Requesting additional documentation or validation from the user.
     Compliance Steps: Triggering enhanced due diligence, requesting source of funds, or blocking the transaction if risk is too high.

     Expected Output Format:
     The LLM should return a Python script with NO ERRORS that:

     Defines a validate_transaction(transaction) function.
     Implements all validation rules listed above.
     Uses datetime, pytz, and iso4217 for compliance checks.
     Returns a structured validation report (valid, flags, risk_score, remediation).
     Provides an example transaction and runs validation on it.
     """
    if context!="":
        flag=True
        extract_rules_gemini(instruction_text)
    print("Step 3: Validating Transactions...")
    validated_data=validate_transactions(df,seen_ids,seen_facility_ids,flag)
    if df.shape[0] > 100:
        print("Step 4: Detecting Anomalies...")
        anomaly_data=detect_anomalies(validated_data)
        print("Step 5: Suggesting Remediation Actions...")
        data=add_remediation_to_data(anomaly_data)
    else:
        print("Step 5: Suggesting Remediation Actions...")
        data=add_remediation_to_data(validated_data)
    print("Pipeline execution complete!")
    return data

if __name__ == "__main__":
    run_pipeline()
