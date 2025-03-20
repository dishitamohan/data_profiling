class Remediation:
    def suggest_remediation(self, data):
        data['Remediation_Action'] = data['Risk_Score'].apply(
            lambda score: "Full audit required" if score > 5 else "Review recommended"
        )
        return data