import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
import numpy as np
import ast
import json
import re



# Configuration: Minimum required features
MIN_FEATURES_BEFORE = 5  # Minimum number of features before variance thresholding
MIN_FEATURES_AFTER = 3   # Minimum number of features after variance thresholding

# def extract_risk_score(row):
#     """
#     Extracts the risk_score from the 'Validation_Report' column.
#     Assumes that the report is stored as a string representation of a dictionary.
#     If parsing fails, returns 0.
#     """
#     report = row.get("Validation_Report")
#     if isinstance(report, str) and report.strip():
#         try:
#             # Safely evaluate the string to a dict (in production, consider using json.loads if possible)
#             report_dict = eval(report)
#             return report_dict.get("risk_score", 0)
#         except Exception as e:
#             return 0
#     elif isinstance(report, dict):
#         return report.get("risk_score", 0)
#     return 0

def extract_risk_score(row):
    validation_data = row.get("Validation Results", "")

    if isinstance(validation_data, dict):
        return validation_data.get("risk_score", None)  # If already a dictionary, extract directly

    if not isinstance(validation_data, str) or pd.isna(validation_data):
        return None  # Handle missing values or non-string cases

    try:
        # Remove extra surrounding quotes if necessary
        if validation_data.startswith("\"{") and validation_data.endswith("}\""):
            validation_data = validation_data[1:-1]  # Remove extra quotes
        
        validation_dict = ast.literal_eval(validation_data)  # Convert string to dictionary
        return validation_dict.get("risk_score", None)
    except (SyntaxError, ValueError):  
        return None  # Handle incorrect formats



def select_features(df, min_before=MIN_FEATURES_BEFORE, min_after=MIN_FEATURES_AFTER):
    # Drop non-numeric columns
    df_numeric = df.select_dtypes(include=[np.number])
    # Ensure we have at least `min_before` features
    if df_numeric.shape[1] < min_before:
        return df_numeric  # Return without variance thresholding

    # Remove low-variance features (only if we have enough features)
    selector = VarianceThreshold(threshold=0.01)  # Adjust threshold as needed
    selected_features = selector.fit_transform(df_numeric)

    # Get selected feature names
    selected_columns = df_numeric.columns[selector.get_support()]

    # Ensure we have at least `min_after` features after selection
    if len(selected_columns) < min_after:
        return df_numeric  # Return without variance thresholding

    return pd.DataFrame(selected_features, columns=selected_columns)


# Step 2: Standardize Data


def detect_anomalies(data):
    """
    Detects anomalies using Isolation Forest, considering the risk score extracted from
    the 'Validation_Report' column.
    """
    # Create a new column 'Computed_Risk_Score' by extracting risk score from Validation_Report
    data["Computed_Risk_Score"] = data.apply(extract_risk_score, axis=1)

    # Use Transaction_Amount, Account_Balance, and Computed_Risk_Score as features
    df_selected = select_features(data)
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_selected)
    model = IsolationForest(contamination=0.05, random_state=42)
    data["Anomaly_Score"] = model.fit_predict(df_scaled)
    data["Is_Anomaly"] = data["Anomaly_Score"] == -1
    data.to_csv(r"D:\DataProfiling_TechnologyHackathon\data_profiling-main\data_profiling-main\data\anomalous_transactions.csv", index=True)
    return data

if __name__ == "__main__":
    df = pd.read_csv(r"D:\DataProfiling_TechnologyHackathon\data_profiling-main\data_profiling-main\data\validated_transactions.csv")
    anomalous_df = detect_anomalies(df)
    print("Anomaly detection complete. Sample results:")
    print(anomalous_df[["Transaction_Amount", "Is_Anomaly", "Computed_Risk_Score"]].head())
