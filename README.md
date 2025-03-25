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
├── data/
│   ├── transactions.csv                # Your raw transaction dataset
│   ├── extracted_rules.py              # (Dynamically generated) Python script with validation rules
│   ├── processed_transactions.csv      # Preprocessed data output
│   ├── validated_transactions.csv      # Data after applying validation
│   ├── anomalous_transactions.csv      # Data flagged as anomalous
│   ├── remediated_transactions.csv     # Data with remediation advice added
│
├── src/
│   ├── preprocessing.py                # Data loading and preprocessing
│   ├── rule_extraction.py              # Extracts validation rules using Gemini
│   ├── validation.py                   # Applies dynamic validation rules
│   ├── anomaly_detection.py            # Anomaly detection using Isolation Forest
│   ├── remediation.py                  # Suggest remediation actions using SHAP
│   └── main.py                         # Orchestrates the entire pipeline
│
├── requirements.txt                    # Python dependencies
└── README.md                           # Project documentation
```
## Architecture Diagram
![Editor _ Mermaid Chart-2025-03-25-104733](https://github.com/user-attachments/assets/79aeada7-254f-4e15-96cd-b396113ef520)



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



