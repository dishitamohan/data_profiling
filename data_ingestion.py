import pandas as pd
import numpy as np

class DataIngestion:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        try:
            data = pd.read_csv(self.file_path)
            return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None

    def clean_data(self, data):
        data.fillna({'Reported_Amount': 0, 'Transaction_Amount': 0}, inplace=True)
        data['Transaction_Date'] = pd.to_datetime(data['Transaction_Date'], errors='coerce')
        data['Currency'] = data['Currency'].str.strip().str.upper()
        data.dropna(subset=['Transaction_Date'], inplace=True)
        return data

    def preprocess_data(self):
        data = self.load_data()
        if data is not None:
            return self.clean_data(data)
        else:
            return None