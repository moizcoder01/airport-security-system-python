import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import smtplib
from email.message import EmailMessage

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Airport Security System",
    layout="wide"
)

plt.style.use("seaborn-v0_8-darkgrid")

# ================= EMAIL CONFIG =================
EMAIL_SENDER = "taha.kashif.1199@gmail.com"
EMAIL_PASSWORD = "wnndibsfttijfirw"
EMAIL_RECEIVER = "muhammadmoizkhan391@gmail.com"

# ================= CONSTANTS =================
LESS_DANGEROUS_WEAPONS = ["lighter", "scissors", "blade"]
DANGEROUS_WEAPONS = ["knife", "pistol"]

LESS_DANGEROUS_CHEMICALS = ["glycerin", "cocaine", "heroine", "marijuana"]
DANGEROUS_CHEMICALS = ["potassium_nitrate", "nitrate based explosives"]

# ================= DATA CLEANING =================
def clean_data(df):
    df.columns = df.columns.str.strip().str.lower()

    text_cols = [
        "behavior_state", "bag_tampering", "no_fly_match",
        "chemical_trace", "baggage_scan_result",
        "travel_anomaly_level", "travel_pattern_risk",
        "duplicate_bag_tag", "unattended_baggage",
        "multiple_boarding_passes"
    ]

    for col in text_cols:
        df[col] = df[col].astype(str).str.lower()

    df["extra_weight_kg"] = pd.to_numeric(df["extra_weight_kg"], errors="coerce")
    df = df.dropna().reset_index(drop=True)

    return df

# ================= RISK ENGINE =================
def calculate_risk(row):
    score = 0
    reasons = []

    if row["no_fly_match"] == "yes":
        score += 5
        reasons.append("No-Fly List Match")

    if row["baggage_scan_result"] in DANGEROUS_WEAPONS:
        score += 35
        reasons.append("Dangerous Weapon Detected")
    elif row["baggage_scan_result"] in LESS_DANGEROUS_WEAPONS:
        score += 25
        reasons.append("Suspicious Weapon Detected")

    if row["chemical_trace"] in DANGEROUS_CHEMICALS:
        score += 35
        reasons.append("Dangerous Chemical Trace")
    elif row["chemical_trace"] in LESS_DANGEROUS_CHEMICALS:
        score += 25
        reasons.append("Suspicious Chemical Trace")

    if row["travel_anomaly_level"] == "high":
        score += 15
        reasons.append("High Travel Anomaly")

    if row["duplicate_bag_tag"] == "yes":
        score += 20
        reasons.append("Duplicate Bag Tag")

    if row["multiple_boarding_passes"] == "yes":
        score += 20
        reasons.append("Multiple Boarding Passes")

    if row["unattended_baggage"] == "yes":
        score += 15
        reasons.append("Unattended Baggage")

    if row["bag_tampering"] == "yes":
        score += 10
        reasons.append("Bag Tampering")

    if row["behavior_state"] in ["nervous", "aggressive"]:
        score += 10
        reasons.append("Suspicious Behavior")

    if row["extra_weight_kg"] >= 7:
        score += 10
        reasons.append("Excess Baggage Weight")

    return score, "\n- ".join(reasons)

def classify_risk(score):
    if score >= 140:
        return "HIGH"
    elif score >= 100:
        return "MEDIUM"
    return "LOW"

# ================= SINGLE EMAIL (ALL HIGH RISK) =================
def send_high_risk_email(high_risk_df):
    if high_risk_df.empty:
        return False

    body = """
AIRPORT SECURITY ALERT
=====================

The following HIGH-RISK passengers were detected:

"""

    for _, p in high_risk_df.iterrows():
        body += f"""
Passenger ID   : {p['passenger_id']}
Name           : {p['passenger_name']}
Flight No      : {p['flight_no']}
Risk Score     : {p['risk_score']}
Reasons:
- {p['reasons']}
----------------------------------------
"""

    body += f"""
Generated On:
{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER.strip()
    msg["Subject"] = "🚨 HIGH RISK PASSENGER ALERT"
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

    return True
def generate_report_text(passenger):
    reasons = passenger["reasons"].split("\n- ")
    reasons_block = "\n".join([f"- {r}" for r in reasons if r.strip()])

    return f"""
AIRPORT SECURITY RISK ASSESSMENT REPORT

Passenger ID   : {passenger['passenger_id']}
Passenger Name : {passenger['passenger_name']}
Flight Number  : {passenger['flight_no']}

----------------------------------------
Risk Score : {passenger['risk_score']}
Risk Level : {passenger['risk_level']}

Risk Factors:
{reasons_block}

Generated On:
{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""".strip()
# ================= REPORT GENERATOR =================
def generate_report_pdf(passenger):
    filename = f"{passenger['passenger_id']}_security_report.pdf"

    fig, ax = plt.subplots(figsize=(8.5, 11))  # A4 size
    ax.axis("off")

    y = 0.95      # starting vertical position
    line_gap = 0.035

    # ===== MAIN TITLE =====
    ax.text(
        0.5, y,
        "AIRPORT SECURITY RISK ASSESSMENT REPORT",
        fontsize=18,
        fontweight="bold",
        ha="center",
        va="top"
    )
    y -= line_gap * 2

    # ===== BASIC INFO =====
    ax.text(0.05, y, f"Passenger ID      : {passenger['passenger_id']}", fontsize=11)
    y -= line_gap
    ax.text(0.05, y, f"Passenger Name    : {passenger['passenger_name']}", fontsize=11)
    y -= line_gap
    ax.text(0.05, y, f"Flight Number     : {passenger['flight_no']}", fontsize=11)
    y -= line_gap * 1.5

    # ===== RISK SECTION =====
    ax.text(0.05, y, "RISK ASSESSMENT", fontsize=13, fontweight="bold")
    y -= line_gap

    ax.text(0.05, y, f"Final Risk Score  : {passenger['risk_score']}", fontsize=11)
    y -= line_gap
    ax.text(0.05, y, f"Risk Level        : {passenger['risk_level']}", fontsize=11)
    y -= line_gap * 1.5

    # ===== REASONS =====
    ax.text(0.05, y, "Risk Factors:", fontsize=13, fontweight="bold")
    y -= line_gap

    reasons_list = passenger["reasons"].split("\n- ")
    for reason in reasons_list:
        ax.text(0.07, y, f"• {reason.strip()}", fontsize=11)
        y -= line_gap

    y -= line_gap * 0.5

    # ===== RECOMMENDATION =====
    ax.text(0.05, y, "Recommendation:", fontsize=13, fontweight="bold")
    y -= line_gap

    if passenger["risk_level"] == "HIGH":
        ax.text(
            0.07, y,
            "Immediate secondary screening is REQUIRED.",
            fontsize=11
        )
    else:
        ax.text(
            0.07, y,
            "Passenger cleared under standard security procedures.",
            fontsize=11
        )

    y -= line_gap * 2

    # ===== FOOTER =====
    ax.text(
        0.5, y,
        f"Report Generated On: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        fontsize=10,
        ha="center"
    )

    plt.savefig(filename, format="pdf", bbox_inches="tight")
    plt.close(fig)

    return filename

# ================= UI =================
st.title("✈️ Airport Security System")
st.caption("Rule-Based Passenger Screening System")

uploaded_file = st.file_uploader("Upload Passenger Dataset (CSV)", type="csv")

if uploaded_file:
    df = clean_data(pd.read_csv(uploaded_file))

    scores, reasons = zip(*df.apply(calculate_risk, axis=1))
    df["risk_score"] = scores
    df["risk_level"] = df["risk_score"].apply(classify_risk)
    df["reasons"] = reasons

    st.subheader("📄 Processed Dataset")
    st.dataframe(df)

    # ================= VISUALS =================
    st.subheader("📊 Core Analytics")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(10, 5))
        df["risk_level"].value_counts().plot(kind="bar", ax=ax)
        ax.set_title("Risk Level Distribution")
        ax.set_xlabel("Risk Level")
        ax.set_ylabel("Passenger Count")
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(df["risk_score"], bins=12, edgecolor="black")
        ax.set_title("Risk Score Histogram")
        ax.set_xlabel("Risk Score")
        ax.set_ylabel("Frequency")
        ax.grid(alpha=0.3)
        st.pyplot(fig)
    # ================= REPORT =================
    st.subheader("📄 Passenger Report")

    pid = st.selectbox("Select Passenger ID", df["passenger_id"])
    passenger = df[df["passenger_id"] == pid].iloc[0]

    report_text = generate_report_text(passenger)

    st.text_area("Report Preview", report_text, height= 400)

    pdf_file = generate_report_pdf(passenger)
    with open(pdf_file, "rb") as f:
        st.download_button(
            "⬇️ Download PDF Report",
            f,
            file_name=pdf_file,
            mime="application/pdf"
        )

    # ================= EMAIL =================
    st.subheader("📧 Security Alert")

    high_risk_df = df[df["risk_level"] == "HIGH"]

    if high_risk_df.empty:
        st.success("No HIGH-Risk passengers detected.")
    else:
        st.error(f"{len(high_risk_df)} HIGH-RISK passengers detected.")

        if st.button("🚨 Send High-Risk Alert Email"):
            send_high_risk_email(high_risk_df)
            st.success("High-risk alert email sent successfully.")
else:
    st.info("Upload a CSV file to begin.")