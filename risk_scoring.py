import pandas as pd

class RiskScoring:
    def __init__(self):
        self.high_risk_countries = ['US', 'UK']
        self.high_value_threshold = 5000

    def assign_risk_score(self, data):
        def calculate_score(row):
            score = 0
            if row['Transaction_Amount'] > self.high_value_threshold:
                score += 3
            if row['Country'] in self.high_risk_countries:
                score += 2
            if row['Anomaly'] == 1:
                score += 5
            return score

        data['Risk_Score'] = data.apply(calculate_score, axis=1)
        return data