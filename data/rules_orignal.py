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
    # Must not contain line breaks, commas, or unprintable characters.
    if re.search(r'[\n,\t\r]', customer_id):
        return "Invalid CustomerID"
    return None

def validate_internal_obligor_id(internal_obligor_id: str, seen_ids: set) -> Union[None, str]:
    if internal_obligor_id in seen_ids or re.search(r'[\n,\t\r]', internal_obligor_id):
        return "Duplicate/Invalid ObligorID"
    seen_ids.add(internal_obligor_id)
    return None

def validate_original_internal_obligor_id(original_id: str, internal_id: str) -> Union[None, str]:
    if original_id != internal_id:
        return "Original ID Mismatch"
    return None

def validate_obligor_name(obligor_name: str, tin: str) -> Union[None, str]:
    # Must be a legal name or "Individual" for natural persons.
    if obligor_name.strip() == "Individual" and tin.strip() not in {"", "NA"}:
        return "Name-TIN Conflict"
    if re.search(r'[^\w\s\-\.]', obligor_name):
        return "Invalid Characters in ObligorName"
    return None

def validate_city_country(city: str, country: str) -> Union[None, str]:
    # If city is known and its mapped country does not match the provided country, flag.
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
    except:
        return "Invalid Code Type"
    return None

def validate_internal_rating(rating: str) -> Union[None, str]:
    if rating.strip() not in APPROVED_RATINGS:
        return "Unapproved Risk Rating"
    return None

def validate_tin(tin: str, entity_type: str = "Corporate") -> Union[None, str]:
    tin = tin.strip()
    if entity_type == "Individual":
        if tin not in {"", "NA"}:
            return "Invalid TIN"
        return None
    # For corporates, require 9 digits (either with a dash or without)
    if re.match(r'^\d{2}-\d{7}$', tin) or re.match(r'^\d{9}$', tin):
        return None
    return "Invalid TIN"

def validate_stock_exchange_tkr(stock_exchange: str, tkr: str) -> Union[None, str]:
    if stock_exchange.strip() == "NA" and tkr.strip() not in {"", "NA"}:
        return "Exchange-TKR Conflict"
    return None

def validate_tkr(tkr: str) -> Union[None, str]:
    tkr = tkr.strip()
    if tkr in {"", "NA"}:
        return None
    if not re.match(r'^[A-Z0-9]{1,5}$', tkr):
        return "Invalid Ticker"
    return None

def validate_cusip(cusip: str) -> Union[None, str]:
    cusip = str(cusip).strip()
    if cusip in {"", "NA"}:
        return None
    if not re.match(r'^[A-Z0-9]{6}$', cusip):
        return "Invalid CUSIP"
    return None

def validate_internal_credit_facility_id(facility_id: str, seen_facility_ids: set) -> Union[None, str]:
    if facility_id in seen_facility_ids or re.search(r'[^A-Za-z0-9]', facility_id):
        return "Duplicate/Invalid FacilityID"
    seen_facility_ids.add(facility_id)
    return None

def validate_original_internal_credit_facility_id(orig_facility_id: str, facility_id: str) -> Union[None, str]:
    if orig_facility_id != facility_id:
        return "Original FacilityID Mismatch"
    return None

def validate_origination_date(origination_date: str) -> Union[None, str]:
    try:
        dt = datetime.datetime.strptime(origination_date.strip(), "%Y-%m-%d")
        if dt > datetime.datetime.today():
            return "Future Origination Date"
    except ValueError:
        return "Invalid Origination Date Format"
    return None

def validate_maturity_date(maturity_date: str, origination_date: str) -> Union[None, str]:
    try:
        orig_dt = datetime.datetime.strptime(origination_date.strip(), "%Y-%m-%d")
        mat_dt = datetime.datetime.strptime(maturity_date.strip(), "%Y-%m-%d")
        if maturity_date.strip() != "9999-01-01" and mat_dt <= orig_dt:
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
        if ft == 0:
            if not other_facility_type.strip():
                return "Missing Other Facility Type Description"
        else:
            if str(other_facility_type).strip():
                return "Unnecessary Facility Description"
    except ValueError:
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
        if p == 0:
            if not str(other_purpose).strip():
                return "Missing Other Purpose Description"
        else:
            if str(other_purpose).strip():
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
    if str(chargeoffs).strip() in {"NA", ""}:
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
    # Define risk weights for each violation.
    weights = {
        "Invalid CustomerID": 5,
        "Duplicate/Invalid ObligorID": 10,
        "Original ID Mismatch": 10,
        "Name-TIN Conflict": 8,
        "City-Country Mismatch": 8,
        "Invalid Country Code": 5,
        "Invalid ZIP/Postal Code": 5,
        "Invalid Industry Code": 5,
        "Invalid Code Type": 5,
        "Unapproved Risk Rating": 5,
        "Invalid TIN": 8,
        "Exchange-TKR Conflict": 8,
        "Invalid Ticker": 5,
        "Invalid CUSIP": 10,
        "Duplicate/Invalid FacilityID": 10,
        "Original FacilityID Mismatch": 10,
        "Future Origination Date": 5,
        "Invalid Origination Date Format": 5,
        "Invalid Maturity Date": 10,
        "Invalid Maturity Date Format": 5,
        "Invalid Facility Type": 8,
        "Missing Other Facility Type Description": 5,
        "Unnecessary Facility Description": 5,
        "Invalid Purpose Code": 8,
        "Missing Other Purpose Description": 5,
        "Unnecessary Purpose Description": 5,
        "Invalid Exposure Amount": 8,
        "Overutilized Facility": 10,
        "Invalid Reporting Line": 5,
        "Unapproved Line of Business": 8,
        "Invalid Charge-off Amount": 5,
        "Invalid Reserve Amount": 5,
    }
    score = sum(weights.get(v, 0) for v in violations)
    return score

# ------------------------------
# Main Validation Function
# ------------------------------
def validate_transaction(transaction: Dict[str, str],
                         seen_ids: set,
                         seen_facility_ids: set,
                         prior_facility_mapping: dict = None) -> Dict:
    """
    Validates a transaction across 28 fields with separate functions.
    Returns a validation report including valid (Boolean), flags (list), risk_score (int), and remediation (list).
    """
    if prior_facility_mapping is None:
        prior_facility_mapping = {}

    violations = []

    # 1. CustomerID
    err = validate_customer_id(transaction.get("CustomerID", ""))
    if err: violations.append(err)

    # 2. InternalObligorID
    err = validate_internal_obligor_id(transaction.get("InternalObligorID", ""), seen_ids)
    if err: violations.append(err)

    # 3. OriginalInternalObligorID
    err = validate_original_internal_obligor_id(transaction.get("OriginalInternalObligorID", ""), transaction.get("InternalObligorID", ""))
    if err: violations.append(err)

    # 4. ObligorName & TIN
    err = validate_obligor_name(transaction.get("ObligorName", ""), transaction.get("TIN", ""))
    if err: violations.append(err)

    # 5. City-Country mismatch
    err = validate_city_country(transaction.get("City", ""), transaction.get("Country", ""))
    if err: violations.append(err)

    # 6. Country
    err = validate_country(transaction.get("Country", ""))
    if err: violations.append(err)

    # 7. Zip Code
    err = validate_zip_code(transaction.get("ZipCodeForeignMailingCode", ""), transaction.get("Country", ""))
    if err: violations.append(err)

    # 8. Industry Code
    err = validate_industry_code(transaction.get("IndustryCode", ""))
    if err: violations.append(err)

    # 9. Industry Code Type
    err = validate_industry_code_type(transaction.get("IndustryCodeType", ""))
    if err: violations.append(err)

    # 10. Internal Rating
    err = validate_internal_rating(transaction.get("InternalRating", ""))
    if err: violations.append(err)

    # 11. TIN
    err = validate_tin(transaction.get("TIN", ""), transaction.get("EntityType", "Corporate"))
    if err: violations.append(err)

    # 12. StockExchange & TKR conflict
    err = validate_stock_exchange_tkr(transaction.get("StockExchange", ""), transaction.get("TKR", ""))
    if err: violations.append(err)

    # 13. TKR
    err = validate_tkr(transaction.get("TKR", ""))
    if err: violations.append(err)

    # 14. CUSIP
    err = validate_cusip(transaction.get("CUSIP", ""))
    if err: violations.append(err)

    # 15. Internal Credit Facility ID
    err = validate_internal_credit_facility_id(transaction.get("InternalCreditFacilityID", ""), seen_facility_ids)
    if err: violations.append(err)

    # 16. Original Internal Credit Facility ID
    err = validate_original_internal_credit_facility_id(transaction.get("OriginalInternalCreditFacilityID", ""), transaction.get("InternalCreditFacilityID", ""))
    if err: violations.append(err)

    # 17. Origination Date
    err = validate_origination_date(transaction.get("OriginationDate", ""))
    if err: violations.append(err)

    # 18. Maturity Date
    err = validate_maturity_date(transaction.get("MaturityDate", ""), transaction.get("OriginationDate", ""))
    if err: violations.append(err)

    # 19. FacilityType
    err = validate_facility_type(transaction.get("FacilityType", ""))
    if err: violations.append(err)

    # 20. OtherFacilityType
    err = validate_other_facility_type(transaction.get("OtherFacilityType", ""), transaction.get("FacilityType", ""))
    if err: violations.append(err)

    # 21. CreditFacilityPurpose
    err = validate_credit_facility_purpose(transaction.get("CreditFacilityPurpose", ""))
    if err: violations.append(err)

    # 22. OtherCreditFacilityPurpose
    err = validate_other_credit_facility_purpose(transaction.get("OtherFacilityPurpose", ""), transaction.get("CreditFacilityPurpose", ""))
    if err: violations.append(err)

    # 23. CommittedExposure
    err = validate_committed_exposure(transaction.get("CommittedExposure", ""))
    if err: violations.append(err)

    # 24. UtilizedExposure
    err = validate_utilized_exposure(transaction.get("UtilizedExposure", ""), transaction.get("CommittedExposure", ""))
    if err: violations.append(err)

    # 25. LineReportedOnFRY9C
    err = validate_reporting_line(transaction.get("LineReportedOnFRY9C", ""))
    if err: violations.append(err)

    # 26. LineOfBusiness
    err = validate_line_of_business(transaction.get("LineOfBusiness", ""))
    if err: violations.append(err)

    # 27. CumulativeChargeoffs
    err = validate_chargeoffs(transaction.get("CumulativeChargeoffs", ""), transaction.get("CommittedExposure", ""))
    if err: violations.append(err)

    # 28. ASC31010
    err = validate_asc31010(transaction.get("ASC31010", ""))
    if err: violations.append(err)

    risk_score = calculate_risk_score(violations)

    # Remediation actions (for demonstration, we use simple logic)
    remediation = []
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

# ------------------------------
# Testing with a Sample Transaction
# ------------------------------
if __name__ == "__main__":
    # Sets for uniqueness checks
    seen_ids = set()
    seen_facility_ids = set()

    # Sample transaction for testing (modify values to trigger different validations)
    sample_transaction = {
        "CustomerID": "CUST002",
        "InternalObligorID": "OBL002",
        "OriginalInternalObligorID": "OBL002",
        "ObligorName": "Individual",          # If Individual, TIN must be NA
        "City": "Paris",                      # "Paris" mapped to FR, but Country is US -> mismatch
        "Country": "US",
        "ZipCodeForeignMailingCode": "33101",  # Valid US ZIP?
        "IndustryCode": "551112",             # Valid 6-digit code
        "IndustryCodeType": "4",              # Invalid, must be 1,2, or 3
        "InternalRating": "ZZZ",              # Unapproved rating
        "TIN": "123456789",                   # Format okay? (without dash) but for Corporate, should be 9 digits -> here it's 9 digits, so valid
        "EntityType": "Corporate",
        "StockExchange": "NA",                # NA, but...
        "TKR": "AAPL",                        # ...Ticker provided => conflict
        "CUSIP": "12345",                     # Invalid, should be 6 characters
        "InternalCreditFacilityID": "FCL002",
        "OriginalInternalCreditFacilityID": "FCL003",  # Mismatch
        "OriginationDate": "2023-05-30",        # Valid, assume today is later than that
        "MaturityDate": "2023-01-01",           # Invalid: before origination
        "FacilityType": "1",
        "OtherFacilityType": "Should not be here",  # Unnecessary since FacilityType != 0
        "CreditFacilityPurpose": "99",         # Invalid, out-of-range (must be 0-33)
        "OtherFacilityPurpose": "Some text",   # Unnecessary if purpose != 0
        "CommittedExposure": "5000000",
        "UtilizedExposure": "6000000",         # Overutilized (utilized > committed)
        "LineReportedOnFRY9C": "12",           # Invalid, must be 1-11
        "LineOfBusiness": "Fake Business",     # Not in approved list
        "CumulativeChargeoffs": "6000000",     # Greater than committed
        "ASC31010": "-1000"                    # Negative reserve, invalid
    }

    result = validate_transaction(sample_transaction, seen_ids, seen_facility_ids)
    print("Validation Report:")
    print(result)
