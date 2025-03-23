import pandas as pd
from preprocessing import load_and_preprocess_data
from rule_extraction import extract_rules_gemini
from validation import validate_transactions
from anomaly_detection import detect_anomalies
from remediation import suggest_remediation_gemini,add_remediation_to_data

def run_pipeline(chat_history,validation_rules):
    print("Step 1: Preprocessing Data...")
    df = load_and_preprocess_data(r"C:\Users\krith\hackathon\data_profiling\data\transactions.csv")

    print("Step 2: Extracting Validation Rules...")
    instruction_text = f"""
    Role: "You are an expert in financial compliance and Python programming. Your task is to extract transaction validation rules from the chat history of the user and custom rules if provided to generate a Python script that enforces these rules. If no custom rules provided use default rules to generate a Python script that enforces these rules. The script must include a dynamic risk scoring system and remediation actions."
    output: only executable code without any kind of errors.
    Instructions:
    Generate a Python function that validates financial transactions based on the following regulatory rules. The function should return a structured validation report containing:

    valid (Boolean): Whether the transaction passes all checks.
    flags (List): A list of detected compliance issues.
    risk_score (Integer): A dynamically calculated risk score based on transaction patterns and historical violations.
    remediation (List): Suggested steps to fix or investigate flagged issues.

    Transaction data has the following fields:
    Customer_ID:
    Type: Integer
    Unique identifier for customers (e.g., 1000, 1001).

    Account_Balance:
    Type: Integer
    Current balance in the account (may include negative values, e.g., -8).

    Transaction_Amount:
    Type: Integer
    Amount involved in the transaction (e.g., 2720, 4745).

    Reported_Amount:
    Type: Integer
    Amount officially reported (may differ slightly from Transaction_Amount, e.g., 2730 vs. 2720).

    Currency:
    Type: String
    3-letter currency code (e.g., GBP, USD, INR).

    Country:
    Type: String
    2-letter country code (e.g., UK, IN, US).

    Transaction_Date:
    Type: DateTime (with timezone)
    Timestamp of the transaction (e.g., 2024-06-20 00:00:00+00:00).

    Risk_Score:
    Type: Integer
    Numeric risk assessment (range: 1 to 10).

    is_round_number:
    Type: Boolean
    Indicates if the transaction amount is a round number (values: TRUE/FALSE).

    is_cross_border:
    Type: Boolean
    Indicates if the transaction is international (values: TRUE/FALSE).

    Chat History:
    {chat_history}

    Custom  Rules:
    {validation_rules}

    Default Rules:

    Transaction Amount vs. Reported Amount:
    If transaction Amount differs from reported amount by more than 1% and Currency_Conversion is False, flag it as "Amount mismatch" and suggest an investigation.

    Negative Account Balance:
    If account balance field is negative and OD (Overdraft) is not allowed, flag as "Negative balance" and recommend verifying overdraft permissions.

    Currency Code Validation:
    Transactions should use a valid ISO 4217 currency code.
    If Currency is not valid, flag it as "Invalid currency code" and recommend correcting it.
    If the currency is not in the allowed list, flag as "Unsupported currency" and suggest rejecting the transaction.

    Cross-Border Transactions:
    If Cross_Border is True and transaction amount > $10,000, mandatory Remarks are required.
    If missing, flag as "Missing mandatory remarks" and suggest adding an explanation.

    Transaction Date Checks:
    Future transactions should be flagged with "Future transaction date" and require correction.
    Old transactions (>365 days) should be flagged for data integrity review.

    High-Risk Country Transactions:
    If transaction amount > $5,000 and Country is in high-risk countries (RU, IR, KP), flag as "High-risk transaction" and suggest enhanced due diligence.
    Round-Number Transactions (Money Laundering Risk):
    If transaction amount is $1,000, $5,000, $10,000, $25,000, flag as "Potential money laundering risk" and require source of funds verification.

    Dynamic Risk Scoring System:
    A dynamic risk scoring system should be implemented, adjusting scores based on transaction patterns and historical violations.
    If risk score exceeds a threshold, transaction is high risk and must undergo compliance review.

    Remediation Actions:
    For flagged transactions, suggest appropriate actions, such as:
    Adjustments: Correcting discrepancies in amounts, currencies, and missing remarks.
    Explanations: Requesting additional documentation or validation from the user.
    Compliance Steps: Triggering enhanced due diligence, requesting source of funds, or blocking the transaction if risk is too high.
    Expected Output Format:
    The LLM should return a Python script that:

    Defines a validate_transaction(transaction) function.
    Implements all validation rules listed above.
    Uses datetime, pytz, and iso4217 for compliance checks.
    Implements a dynamic risk scoring system that adjusts scores based on transaction patterns and history.
    Returns a structured validation report (valid, flags, risk_score, remediation).
    Provides an example transaction and runs validation on it.
    """
    extract_rules_gemini(instruction_text)

    print("Step 3: Validating Transactions...")
    validate_transactions(df)

    print("Step 4: Detecting Anomalies...")
    detect_anomalies(pd.read_csv(r"C:\Users\krith\hackathon\data_profiling\data\validated_transactions.csv"))

    print("Step 5: Suggesting Remediation Actions...")
    data=add_remediation_to_data(pd.read_csv(r"C:\Users\krith\hackathon\data_profiling\data\anomalous_transactions.csv"))
    print("Pipeline execution complete!")
    return data

if __name__ == "__main__":
    run_pipeline()
