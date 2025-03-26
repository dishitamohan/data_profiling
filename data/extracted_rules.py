import re
import datetime
from typing import Dict, List, Union
import pandas as pd
import ast


# ------------------------------
# Approved lists and mappings
# ------------------------------
APPROVED_RATINGS = {"AAA", "AA", "A", "BBB", "BBB-", "BB", "B", "CCC", "CC", "C", "D", "A+", "B-"}
APPROVED_BUSINESS_LINES = {"Corporate Banking", "Retail Banking", "Investment Banking", "Wealth Management"}
# For city-country, using a simple mapping for demonstration
CITY_COUNTRY_MAP = {"Paris": "FR", "London": "GB", "New York": "US", "Chicago": "US"}
VALID_INDUSTRY_CODE_TYPES = {1, 2, 3}

def validate_customer_id(customer_id: str) -> Union[None, str]:
    try:
        if re.search(r'[\n,\t\r]', customer_id):
            return "Invalid CustomerID"
        return None
    except Exception as e:
        return f"Error validating CustomerID: {e}"


def validate_customer_id_filter(customer_id: str) -> Union[None, str]:
    try:
        if customer_id != "CUST003":
            return "CustomerID Filtered"
        return None
    except Exception as e:
        return f"Error validating CustomerID Filter: {e}"
    

def calculate_risk_score(violations: List[str]) -> int:
    weights = {
        "Invalid CustomerID": 5,
        "CustomerID Filtered": 2,  # Example weight, adjust as needed
        # ... (other violation weights)
    }
    score = sum(weights.get(v, 0) for v in violations)
    return score

def extract_violation(row):
    try:
        validation_data = row.get("Validation Results", "")
        if isinstance(validation_data, dict):
            return validation_data.get("flags", [])
        if validation_data and isinstance(validation_data, str):
            if validation_data.startswith("\"{") and validation_data.endswith("}\""):
                validation_data = validation_data[1:-1]
            validation_dict = ast.literal_eval(validation_data)
            return validation_dict.get("flags", [])
        return []
    except (SyntaxError, ValueError, TypeError, AttributeError):
        return []

def extract_remediation(row):
    try:
        validation_data = row.get("Validation Results", "")
        if isinstance(validation_data, dict):
            return validation_data.get("remediation", [])
        if validation_data and isinstance(validation_data, str):
            if validation_data.startswith("\"{") and validation_data.endswith("}\""):
                validation_data = validation_data[1:-1]
            validation_dict = ast.literal_eval(validation_data)
            return validation_dict.get("remediation", [])
        return []
    except (SyntaxError, ValueError, TypeError, AttributeError):
        return []

def extract_risk_score(row):
    try:
        validation_data = row.get("Validation Results", "")
        if isinstance(validation_data, dict):
            return validation_data.get("risk_score", 0)
        if validation_data and isinstance(validation_data, str):
            if validation_data.startswith("\"{") and validation_data.endswith("}\""):
                validation_data = validation_data[1:-1]
            validation_dict = ast.literal_eval(validation_data)
            return validation_dict.get("risk_score", 0)
        return 0
    except (SyntaxError, ValueError, TypeError, AttributeError):
        return 0

def validate_transaction(transaction, seen_ids, seen_facility_ids):
    violations = extract_violation(transaction)
    remediation = extract_remediation(transaction)
    risk_score = extract_risk_score(transaction)
    
    try:
        err = validate_customer_id_filter(transaction.get("CustomerID", ""))
        if err:
            violations.append(err)
            remediation.append("Review and correct CustomerID or remove the record if it shouldn't be processed.")

        if "CustomerID Filtered" not in violations: # Only proceed with further validation if not filtered.
            err = validate_customer_id(transaction.get("CustomerID", ""))
            if err: 
                violations.append(err)
                remediation.append("Review and correct CustomerID format.")

    except Exception as e:
        violations.append(f"An unexpected error occurred: {e}")
        remediation.append("Check the logs for details and contact support.")


    risk_score += calculate_risk_score(violations)

    if risk_score > 30:
        remediation.append("Trigger enhanced compliance review and request additional documentation.")
    elif violations:
        remediation.append("Correct the flagged issues as indicated.")
    else:
        remediation.append("No remediation needed.")

    return {
        "valid": not bool(violations),
        "flags": violations,
        "risk_score": risk_score,
        "remediation": remediation
    }



def validate_transaction_file(df):
    seen_ids = set()
    seen_facility_ids = set()
    df["Validation Results"] = df.apply(lambda row: validate_transaction(row.to_dict(), seen_ids, seen_facility_ids), axis=1)
    return df