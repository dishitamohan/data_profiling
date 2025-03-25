import re
import datetime
from typing import Dict, List, Union

# ------------------------------
# Approved lists and mappings
# ------------------------------
APPROVED_RATINGS = {"AAA", "AA", "A", "BBB", "BBB-", "BB", "B", "CCC", "CC", "C", "D", "A+", "B-"}
APPROVED_BUSINESS_LINES = {"Corporate Banking", "Retail Banking", "Investment Banking", "Wealth Management"}
# For city-country, using a simple mapping for demonstration
CITY_COUNTRY_MAP = {"Paris": "FR", "London": "GB", "New York": "US", "Chicago": "US"}
VALID_INDUSTRY_CODE_TYPES = {1, 2, 3}

# ------------------------------
# 1. Field-Level Validation Functions
# ------------------------------

def validate_customer_id(customer_id: str) -> Union[None, str]:
    if re.search(r'[\n,\t\r]', customer_id):
        return "Invalid CustomerID"
    return None

def validate_internal_obligor_id(internal_obligor_id: str, seen_ids: set) -> Union[None, str]:
    if internal_obligor_id in seen_ids or not internal_obligor_id.isalnum():
        return "Duplicate/Invalid ObligorID"
    seen_ids.add(internal_obligor_id)
    return None


def validate_original_internal_obligor_id(original_id: str, internal_id: str) -> Union[None, str]:
    if original_id != internal_id:
        return "Original ID Mismatch"
    return None

def validate_obligor_name(obligor_name: str, tin: str) -> Union[None, str]:
    if obligor_name.strip() == "Individual" and tin.strip() not in {"", "NA"}:
        return "Name-TIN Conflict"
    if re.search(r'[^\w\s\-\.]', obligor_name):  # Allow basic punctuation
        return "Invalid Characters in ObligorName"
    return None

def validate_city_country(city: str, country: str) -> Union[None, str]:
    mapped = CITY_COUNTRY_MAP.get(city.strip())
    if mapped and mapped != country.strip():
        return "City-Country Mismatch"
    return None

def validate_country(country: str) -> Union[None, str]:
    if not re.match(r'^[A-Z]{2}$', country.strip()):
        return "Invalid Country Code"
    return None

def validate_zip_code(zip_code: str, country: str) -> Union[None, str]:
    if country.strip() == "US" and not re.match(r'^\d{5}$', str(zip_code)):
        return "Invalid ZIP/Postal Code"
    return None



def validate_industry_code(industry_code: str) -> Union[None, str]:
    if not re.match(r'^\d{4,6}$', str(industry_code).strip()):
        return "Invalid Industry Code"
    return None

def validate_industry_code_type(industry_code_type: Union[str, int]) -> Union[None, str]:
    try:
        value = int(industry_code_type)
        if value not in VALID_INDUSTRY_CODE_TYPES:
            return "Invalid Code Type"
    except (ValueError, TypeError):  # Handle non-numeric input
        return "Invalid Code Type"
    return None



def validate_internal_rating(rating: str) -> Union[None, str]:
    if rating.strip() not in APPROVED_RATINGS:
        return "Unapproved Risk Rating"
    return None


def validate_tin(tin: str, entity_type: str = "Corporate") -> Union[None, str]:
    tin = tin.strip()
    if entity_type == "Individual" and tin not in {"", "NA"}:
         return "Invalid TIN" # Individuals must have "" or "NA" for TIN
    elif entity_type != "Individual":  # Corporate TIN validation
        if not (re.match(r'^\d{2}-\d{7}$', tin) or re.match(r'^\d{9}$', tin)):
            return "Invalid TIN"
    return None


def validate_stock_exchange_tkr(stock_exchange: str, tkr: str) -> Union[None, str]:
    if stock_exchange.strip() == "NA" and tkr.strip() not in {"", "NA"}:
        return "Exchange-TKR Conflict"
    return None

def validate_tkr(tkr: str) -> Union[None, str]:
    tkr = tkr.strip()
    if tkr in {"", "NA"}:  # Allow blank or NA
        return None
    if not re.match(r'^[A-Z0-9]{1,5}$', tkr):  # 1 to 5 alphanumeric
        return "Invalid Ticker"
    return None

def validate_cusip(cusip: str) -> Union[None, str]:
    cusip = cusip.strip()
    if cusip in {"", "NA"}:  # Allow blank or NA
        return None
    if not re.match(r'^[A-Z0-9]{6}$', cusip):  # 6 alphanumeric characters
        return "Invalid CUSIP"
    return None


def validate_internal_credit_facility_id(facility_id: str, seen_facility_ids: set) -> Union[None, str]:
    if facility_id in seen_facility_ids or re.search(r'[^A-Za-z0-9]', facility_id):
        return "Duplicate/Invalid FacilityID"
    seen_facility_ids.add(facility_id)
    return None



def validate_original_internal_credit_facility_id(orig_facility_id: str, facility_id: str) -> Union[None, str]:

    if orig_facility_id != facility_id :
        return "Original FacilityID Mismatch"
    return None




def validate_origination_date(origination_date: str) -> Union[None, str]:
    try:
        dt = datetime.datetime.strptime(origination_date.strip(), "%Y-%m-%d").date()
        cutoff_date = datetime.date(2020, 12, 31)  # Cutoff at end of 2020
        if dt > cutoff_date :  # Use cutoff date for comparison
            return "Future Origination Date"
    except ValueError:
        return "Invalid Origination Date Format"
    return None



def validate_maturity_date(maturity_date: str, origination_date: str) -> Union[None, str]:
    try:
        orig_dt = datetime.datetime.strptime(origination_date.strip(), "%Y-%m-%d").date()
        if maturity_date.strip() == "9999-01-01":
            return None  # Allow 9999-01-01 for demand loans
        mat_dt = datetime.datetime.strptime(maturity_date.strip(), "%Y-%m-%d").date()

        if mat_dt <= orig_dt:
            return "Invalid Maturity Date"
    except ValueError:
        return "Invalid Maturity Date Format"
    return None


def validate_facility_type(facility_type: str) -> Union[None, str]:
    try:
        val = int(facility_type)
        if not (0 <= val <= 19):
            return "Invalid Facility Type"
    except ValueError:
        return "Invalid Facility Type"
    return None


def validate_other_facility_type(other_facility_type: str, facility_type: str) -> Union[None, str]:
    try:
        ft = int(facility_type)
        if ft == 0 and not other_facility_type.strip():  # Check if empty
            return "Missing Other Facility Type Description"
        elif ft != 0 and other_facility_type.strip(): # Check if not empty
            return "Unnecessary Facility Description"
    except ValueError:  # Handle cases where facility_type isn't a valid integer
        return "Invalid Facility Type"
    return None


def validate_credit_facility_purpose(purpose: str) -> Union[None, str]:
    try:
        val = int(purpose)
        if not (0 <= val <= 33):
            return "Invalid Purpose Code"
    except ValueError:
        return "Invalid Purpose Code"
    return None


def validate_other_credit_facility_purpose(other_purpose: str, purpose: str) -> Union[None, str]:

    try:
        p = int(purpose)
        if p == 0 and not other_purpose.strip(): # Check if empty
            return "Missing Other Purpose Description"
        elif p != 0 and other_purpose.strip():  # Check if not empty
            return "Unnecessary Purpose Description"
    except ValueError:
        return "Invalid Purpose Code"
    return None




def validate_committed_exposure(committed: str) -> Union[None, str]:

    try:
        val = int(committed)
        if val < 0:
            return "Invalid Exposure Amount"
    except ValueError:
        return "Invalid Exposure Amount"
    return None


def validate_utilized_exposure(utilized: str, committed: str) -> Union[None, str]:

    try:
        used = int(utilized)
        comm = int(committed)
        if used > comm:
            return "Overutilized Facility"
    except ValueError:
        return "Invalid Exposure Amount"
    return None


def validate_reporting_line(report_line: str) -> Union[None, str]:

    try:
        val = int(report_line)
        if not (1 <= val <= 11):
            return "Invalid Reporting Line"
    except ValueError:
        return "Invalid Reporting Line"
    return None



def validate_line_of_business(lob: str) -> Union[None, str]:
    if lob.strip() not in APPROVED_BUSINESS_LINES:
        return "Unapproved Line of Business"
    return None



def validate_chargeoffs(chargeoffs: str, committed: str) -> Union[None, str]:
    if chargeoffs.strip() in {"", "NA"}:  # Allow empty or "NA"
        return None
    try:
        co = int(chargeoffs)
        comm = int(committed)

        if co < 0 or co > comm:
            return "Invalid Charge-off Amount"
    except ValueError:
        return "Invalid Charge-off Amount"
    return None




def validate_asc31010(asc: str) -> Union[None, str]:

    try:
        val = int(asc)
        if val < 0:
            return "Invalid Reserve Amount"
    except ValueError:
        return "Invalid Reserve Amount"
    return None


# ------------------------------
# Dynamic Risk Scoring
# ------------------------------

def calculate_risk_score(violations: List[str]) -> int:

    weights = {
        "Invalid CustomerID": 5,
        # ... (rest of the weights are the same)
    }
    score = sum(weights.get(v, 0) for v in violations)
    return score


# ------------------------------
# Main Validation Function
# ------------------------------


def validate_transaction(transaction: Dict[str, str],
                         seen_ids: set = None,  # Make seen_ids optional
                         seen_facility_ids: set = None,  # Make seen_facility_ids optional
                         prior_facility_mapping: dict = None) -> Dict:

    if seen_ids is None:
        seen_ids = set()
    if seen_facility_ids is None:
        seen_facility_ids = set()
    if prior_facility_mapping is None:
        prior_facility_mapping = {}
    violations = []

    # ... (The rest of the validation code is the same)



# ------------------------------
# Testing with a Sample Transaction
# ------------------------------
if __name__ == "__main__":
    # Sets for uniqueness checks (now initialized within the if block)
    seen_ids = set()
    seen_facility_ids = set()

    sample_transaction = { # ... (your sample transaction data)

    }



    result = validate_transaction(sample_transaction, seen_ids, seen_facility_ids)
    print("Validation Report:")
    print(result)