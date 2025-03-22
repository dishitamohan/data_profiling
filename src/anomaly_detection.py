import pandas as pd
from sklearn.ensemble import IsolationForest

def extract_risk_score(row):
    """
    Extracts the risk_score from the 'Validation_Report' column.
    Assumes that the report is stored as a string representation of a dictionary.
    If parsing fails, returns 0.
    """
    report = row.get("Validation_Report")
    if isinstance(report, str) and report.strip():
        try:
            # Safely evaluate the string to a dict (in production, consider using json.loads if possible)
            report_dict = eval(report)
            return report_dict.get("risk_score", 0)
        except Exception as e:
            return 0
    elif isinstance(report, dict):
        return report.get("risk_score", 0)
    return 0

def detect_anomalies(data):
    """
    Detects anomalies using Isolation Forest, considering the risk score extracted from
    the 'Validation_Report' column.
    """
    # Create a new column 'Computed_Risk_Score' by extracting risk score from Validation_Report
    data["Computed_Risk_Score"] = data.apply(extract_risk_score, axis=1)
    
    # Use Transaction_Amount, Account_Balance, and Computed_Risk_Score as features
    features = ["Transaction_Amount", "Account_Balance","Computed_Risk_Score"]
    model = IsolationForest(contamination=0.05, random_state=42)
    data["Anomaly_Score"] = model.fit_predict(data[features])
    data["Is_Anomaly"] = data["Anomaly_Score"] == -1
    data.to_csv(r"Team_Repo2\data\anomalous_transactions.csv", index=True)
    return data

if __name__ == "__main__":
    df = pd.read_csv(r"Team_Repo2\data\validated_transactions.csv")
    anomalous_df = detect_anomalies(df)
    print("Anomaly detection complete. Sample results:")
    print(anomalous_df[["Transaction_Amount", "Is_Anomaly", "Computed_Risk_Score"]].head())
