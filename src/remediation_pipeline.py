from remediation import add_remediation_to_data
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def apply_remediation(df,custid,all):
    if all:
        filtered_data=df
    else:
        filtered_data = df[df["CustomerID"] == custid]
    print("entered remediation pipeline")
    # filtered_data=df
    data = add_remediation_to_data(filtered_data)
    print(data)
    remediations = data.to_dict(orient="records")
    selected_keys = ['CustomerID', 'Validation Results', 'Remediation_Advice']
    if 'Is_Anomaly'in df.columns:
        selected_keys.insert(2,'Is_Anomaly')
    # Only these fields will be shown
    # Create PDF document
    pdf_filename = r"D:\DataProfiling_TechnologyHackathon\data_profiling-main\data_profiling-main\data\remediation_Report.pdf"
    pdf = SimpleDocTemplate(pdf_filename, pagesize=A4)
    elements = []

    # Define text style with increased line spacing (leading)
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=styles["Normal"],
        fontSize=12,       # Adjust font size if needed
        leading=20,        # Line spacing (increase for more space)
        spaceAfter=10      # Extra space after each paragraph
    )

    # Add each dictionary entry to the PDF with proper spacing
    for entry in remediations:
        for key in selected_keys:
            print(key)
            elements.append(Paragraph(f"<b>{key}</b>:  {entry[key]}", custom_style))  # Bold keys, increased spacing
            elements.append(Spacer(1, 15))  # More space between key-value pairs

        elements.append(Spacer(1, 30))  # Larger space between different records

    # Build the PDF
    pdf.build(elements)

    print(f"✅ PDF saved as {pdf_filename}")
