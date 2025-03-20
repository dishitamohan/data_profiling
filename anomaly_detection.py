from sklearn.ensemble import IsolationForest
import pandas as pd

class AnomalyDetection:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)

    def fit_model(self, data):
        features = ['Account_Balance', 'Transaction_Amount']
        self.model.fit(data[features])

    def detect_anomalies(self, data):
        data['Anomaly'] = self.model.predict(data[['Account_Balance', 'Transaction_Amount']])
        data['Anomaly'] = data['Anomaly'].apply(lambda x: 1 if x == -1 else 0)
        return data