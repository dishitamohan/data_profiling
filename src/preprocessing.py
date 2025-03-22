import pandas as pd
import datetime
import pytz

def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path)
    data['Transaction_Date'] = pd.to_datetime(data['Transaction_Date'], errors='coerce')
    data["Transaction_Date"] = data["Transaction_Date"].dt.tz_localize('UTC', ambiguous='NaT', nonexistent='NaT')
    data['Risk_Score'].fillna(0, inplace=True)
    data.fillna({"Remarks": "", "Currency_Conversion": False, "OD": False}, inplace=True)
    data['is_round_number'] = data['Transaction_Amount'] % 1000 == 0
    data['is_cross_border'] = data['Country'] != 'US'
    data.to_csv("Team_Repo2\data\processed_transactions.csv", index=False)
    return data
