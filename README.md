# Data Profiling & Regulatory Compliance Pipeline

## Overview
This repository contains a **GenAI-powered data profiling solution** designed for regulatory reporting in the banking sector. It automates data validation, anomaly detection, risk scoring, and remediation actions using **LLMs, unsupervised ML techniques, and Python**.

## Features
- **Data Profiling & Validation:** Extracts profiling rules and validates financial transactions.
- **Anomaly Detection:** Uses Isolation Forest to detect suspicious transactions.
- **Risk Scoring System:** Assigns dynamic risk scores based on validation checks.
- **Remediation Actions:** Utilizes **Gemini AI** and **SHAP explanations** to suggest corrective measures.
- **Modular Pipeline Architecture:** Designed for scalability and maintainability.

## Folder Structure
```
├── data/                # Raw and processed datasets
├── src/
│   ├── main.py         # Main pipeline orchestrator
│   ├── validation.py   # Transaction validation module
│   ├── anomalies.py    # Anomaly detection module
│   ├── remediation.py  # Risk scoring and remediation logic
│   ├── utils.py        # Helper functions
├── notebooks/          # Jupyter notebooks for testing and development
├── README.md           # Project documentation
```

## Setup & Installation
### Prerequisites
- Python 3.8+
- Required dependencies in `requirements.txt`

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-url.git
   cd your-repo
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the pipeline:
   ```bash
   python src/main.py
   ```

## Modules & Workflow
### **1. Data Validation (`validation.py`)**
- Checks **transaction consistency**, currency validation, and fraud indicators.
- Outputs a validation report with **flags and risk scores**.

### **2. Anomaly Detection (`anomalies.py`)**
- Uses **Isolation Forest** to detect anomalies.
- Adds **anomaly scores** to the dataset.

### **3. Risk Scoring & Remediation (`remediation.py`)**
- **SHAP Explainers** highlight key risk drivers.
- **Gemini AI** suggests remediation actions.



