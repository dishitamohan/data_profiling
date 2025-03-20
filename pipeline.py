from data_ingestion import DataIngestion
from rule_extraction import RuleExtraction
from anomaly_detection import AnomalyDetection
from risk_scoring import RiskScoring
from remediation import Remediation

class Pipeline:
    def __init__(self, data_path, api_key):
        self.data_ingestion = DataIngestion(data_path)
        self.rule_extraction = RuleExtraction(api_key)
        self.anomaly_detection = AnomalyDetection()
        self.risk_scoring = RiskScoring()
        self.remediation = Remediation()

    def run_pipeline(self):
        data = self.data_ingestion.preprocess_data()
        rules = self.rule_extraction.extract_rules(
            "Transaction_Amount should match Reported_Amount unless it's a cross-currency conversion."
        )
        print("Extracted Rules:\n", rules)
        self.anomaly_detection.fit_model(data)
        data = self.anomaly_detection.detect_anomalies(data)
        data = self.risk_scoring.assign_risk_score(data)
        data = self.remediation.suggest_remediation(data)
        data.to_csv('artifacts/final_output.csv', index=False)
        print("Pipeline completed successfully. Output saved to 'artifacts/final_output.csv'")

if __name__ == "__main__":
    pipeline = Pipeline("sample_data.csv", "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")
    pipeline.run_pipeline()