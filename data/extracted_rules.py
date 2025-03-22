import datetime
import pytz
import iso4217

def validate_transaction(transaction):
    """
    Validates a financial transaction against regulatory rules.

    Args:
        transaction (dict): A dictionary containing transaction details.

    Returns:
        dict: A validation report with flags, risk score, and remediation suggestions.
    """

    flags = []
    remediation = []
    risk_score = 0
    valid = True
    allowed_currencies = ["GBP", "USD", "INR", "EUR", "JPY"]  # Example allowed currencies
    high_risk_countries = ["RU", "IR", "KP"]
    round_numbers = [1000, 5000, 10000, 25000]

    # Transaction Amount vs. Reported Amount
    if abs(transaction["Transaction_Amount"] - transaction["Reported_Amount"]) > 0.01 * transaction["Transaction_Amount"]:
        flags.append("Amount mismatch")
        remediation.append("Investigate amount discrepancy.")
        risk_score += 8

    # Negative Account Balance (Assuming OD is not allowed by default)
    if transaction["Account_Balance"] < 0:
        flags.append("Negative balance")
        remediation.append("Verify overdraft permissions.")
        risk_score += 6

    # Currency Code Validation
    try:
        iso4217.Currency(transaction["Currency"])
    except ValueError:
        flags.append("Invalid currency code")
        remediation.append("Correct currency code.")
        risk_score += 5
    
    if transaction["Currency"] not in allowed_currencies:
        flags.append("Unsupported currency")
        remediation.append("Reject transaction due to unsupported currency.")
        risk_score +=5


    # Cross-Border Transactions (Assuming remarks are required for > $10,000)
    if transaction["is_cross_border"] and transaction["Transaction_Amount"] > 10000:
        if "Remarks" not in transaction or not transaction["Remarks"]:  # Check for missing or empty remarks
            flags.append("Missing mandatory remarks")
            remediation.append("Add explanation for cross-border transaction.")
            risk_score += 10

    # Transaction Date Checks
    now = datetime.datetime.now(pytz.utc)  # Use UTC for consistency
    transaction_date = transaction["Transaction_Date"]
    if transaction_date > now:
        flags.append("Future transaction date")
        remediation.append("Correct transaction date.")
        risk_score += 5

    if (now - transaction_date).days > 365:
        flags.append("Old transaction")  # Greater than 365 days old
        remediation.append("Review transaction for data integrity.")
        risk_score += 4



    # High-Risk Country Transactions
    if transaction["Transaction_Amount"] > 5000 and transaction["Country"] in high_risk_countries:
        flags.append("High-risk transaction")
        remediation.append("Perform enhanced due diligence.")
        risk_score += 15

    # Round-Number Transactions (Money Laundering Risk)
    if transaction["Transaction_Amount"] in round_numbers:
        flags.append("Potential money laundering risk")
        remediation.append("Verify source of funds.")
        risk_score += 7


    if risk_score > 15:
       remediation.append("Transaction requires compliance review.")
       valid = False

    return {"valid": valid, "flags": flags, "risk_score": risk_score, "remediation": remediation}


# Example transaction (replace with your actual data)
example_transaction = {
    "Customer_ID": 1001,
    "Account_Balance": 15000,
    "Transaction_Amount": 10000,
    "Reported_Amount": 10100, 
    "Currency": "USD",
    "Country": "US",
    "Transaction_Date": datetime.datetime(2024, 6, 20, tzinfo=pytz.utc),
    "Risk_Score": 0,  # Initial risk score
    "is_round_number": True,
    "is_cross_border": False
    # ... other transaction fields
}



validation_report = validate_transaction(example_transaction)
print(validation_report)


