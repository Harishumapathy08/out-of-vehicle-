import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Set page config
st.set_page_config(page_title="Invoice Entry", layout="wide")

# Background color using HTML
st.markdown("""
    <style>
        body {
            background-color: #f0f4f7;
        }
        .stApp {
            background-color: #f0f4f7;
        }
    </style>
""", unsafe_allow_html=True)

# Get current month and year for Excel file name
month_name = datetime.now().strftime("%B_%Y")
file_name = f"{month_name}.xlsx"

# Column names
columns = ["S.No.", "Invoice Date", "Invoice No", "Customer",
           "Destination", "Dispatch Date", "Transporter",
           "Vehicle", "Freight Charges"]

# Load existing data or create a new DataFrame
if os.path.exists(file_name):
    df = pd.read_excel(file_name)
else:
    df = pd.DataFrame(columns=columns)

# Sanitize DataFrame
df["S.No."] = pd.to_numeric(df["S.No."], errors='coerce').fillna(0).astype(int)
df["Freight Charges"] = pd.to_numeric(df["Freight Charges"], errors='coerce').fillna(0.0)
df.fillna("", inplace=True)

st.title("📄 Invoice Entry System")

with st.form("entry_form"):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        invoice_date = st.date_input("Invoice Date")
        invoice_no = st.text_input("Invoice No")
    with col2:
        customer = st.text_input("Customer")
        destination = st.text_input("Destination")
    with col3:
        disp_date = st.date_input("Dispatch Date")
        transporter = st.text_input("Transporter")
    with col4:
        vehicle = st.text_input("Vehicle")
        freight = st.number_input("Freight Charges", min_value=0.0, format="%.2f")
    with col5:
        st.markdown("##")
        submitted = st.form_submit_button("➕ Add Entry")

if submitted:
    new_entry = {
        "S.No.": len(df) + 1,
        "Invoice Date": invoice_date,
        "Invoice No": invoice_no,
        "Customer": customer,
        "Destination": destination,
        "Dispatch Date": disp_date,
        "Transporter": transporter,
        "Vehicle": vehicle,
        "Freight Charges": freight
    }
    df.loc[len(df)] = new_entry
    df.to_excel(file_name, index=False)
    st.success("✅ Entry added and saved!")

# --- Buttons ---
colA, colB, colC = st.columns(3)
with colA:
    if st.button("📂 Load Data"):
        st.dataframe(df)

with colB:
    delete_index = st.number_input("S.No. to Delete", min_value=1, max_value=len(df), step=1)
    if st.button("🗑️ Delete Entry"):
        df = df[df["S.No."] != delete_index]
        df.reset_index(drop=True, inplace=True)
        df["S.No."] = range(1, len(df) + 1)
        df.to_excel(file_name, index=False)
        st.success(f"Deleted entry S.No. {delete_index}")

with colC:
    download_data = df.to_excel(index=False, engine='openpyxl')
    st.download_button("📥 Download Excel", data=download_data, file_name=file_name, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# View below
st.subheader("📊 Current Invoice Data")
st.dataframe(df, use_container_width=True)





