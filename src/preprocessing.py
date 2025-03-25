import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

def load_and_preprocess_data(data):
    """
    Generic preprocessing function for any financial dataset.

    Args:
        data (pd.DataFrame): Raw financial dataset.

    Returns:
        pd.DataFrame: Cleaned and preprocessed dataset.
    """
    # Standardize column names (lowercase, replace spaces with underscores)
    # data.columns = data.columns.str.lower().str.replace(" ", "_")

    # Remove duplicates
    data = data.drop_duplicates()

    # Identify numeric and categorical columns dynamically
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = data.select_dtypes(include=["object"]).columns.tolist()

    # Handle missing values
    for col in numeric_cols:
        data[col].fillna(data[col].median(), inplace=True)  # Fill numeric columns with median
    for col in categorical_cols:
        data[col].fillna("Unknown", inplace=True)  # Fill categorical columns with "Unknown"

    # Encode categorical variables
    # for col in categorical_cols:
    #     data[col] = LabelEncoder().fit_transform(data[col])

    # Scale numerical features
    # scaler = StandardScaler()
    # data[numeric_cols] = scaler.fit_transform(data[numeric_cols])
    seen_ids = data['InternalObligorID'].unique().tolist()
    seen_facility_ids = data['InternalCreditFacilityID'].unique().tolist()
    data.to_csv(r"C:\Users\krith\hackathon\data_profiling\data\processed_transactions.csv", index=False)
    # return data
    return data,seen_ids,seen_facility_ids