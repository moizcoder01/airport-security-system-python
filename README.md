# airport-security-system-python
Streamlit-based Airport Security System for passenger risk assessment, analytics, PDF reporting, and automated alerts.

This project demonstrates how Python can be used to transform raw passenger screening data into actionable security intelligence through centralized processing, analytics, and reporting.
🚀 Features
CSV-based passenger data ingestion
Automated data cleaning and normalization
Rule-based risk engine with weighted threat scoring
Risk classification into LOW / MEDIUM / HIGH tiers
Interactive Streamlit dashboard
Real-time graphical analytics using Matplotlib
Automated PDF risk assessment reports
Email alerts for high-risk passengers using SMTP
Transparent justification (“Reasons”) for each risk decision

🧠 System Architecture (Python Backend)
The backend follows a functional pipeline architecture:

Data Ingestion
Passenger data uploaded via CSV

Data Cleaning
Column normalization
Type enforcement
Missing value handling

Risk Evaluation
Weapons detection
Chemical trace analysis
Behavioral anomalies
Travel pattern risk
Procedural irregularities (duplicate tags, unattended baggage)

Risk Classification
Numeric score → categorical risk level

Outputs
Interactive dashboard
Visual analytics
PDF reports
Automated email alerts

🛠️ Technologies Used
Technology	Purpose
Python	Core backend logic
Streamlit	Web-based UI
Pandas	Data processing
NumPy	Numerical operations
Matplotlib	Charts & PDF generation
smtplib	Email alerts
EmailMessage	Structured email formatting
datetime	Timestamping

📊 Risk Scoring Logic
Each passenger is evaluated using a weighted risk model:
Dangerous weapons → high penalty
Explosive chemical traces → high penalty
Behavioral anomalies → moderate penalty
Travel pattern irregularities → moderate penalty
Procedural violations → cumulative penalty

Risk Classification
Score Range	Risk Level
≥ 140	HIGH
100 – 139	MEDIUM
< 100	LOW
Each score is accompanied by a detailed list of reasons for audit transparency.

📈 Visual Analytics
The dashboard includes:
Risk Level Distribution (Bar Chart)
Risk Score Histogram

These visuals allow security analysts to:
Detect anomaly spikes
Identify clustering near critical thresholds
Monitor overall threat distribution

📄 PDF Report Generation
For each passenger, the system generates a professional A4 PDF report containing:
Passenger details
Final risk score & classification
Detailed list of detected risk factors
Automated security recommendation
Timestamp for audit traceability

📧 Automated Email Alerts
If any passenger is classified as HIGH risk, the system can:
Compile passenger details and threat reasons
Send a real-time alert email to security authorities
Confirm delivery inside the dashboard

SMTP is configured using app-based authentication for security.

## How to Run the Project
1. Install required libraries:
pip install streamlit pandas numpy matplotlib smtp 
2. Configure email credentials
Inside the script:
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "security_authority@email.com"
3. Run the Streamlit application:
streamlit run project.py

