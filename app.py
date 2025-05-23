import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Generate month-based filename
month_name = datetime.now().strftime("%B_%Y")
file_name = f"invoices_{month_name}.xlsx"

# Load or initialize data
def load_data():
    if os.path.exists(file_name):
        return pd.read_excel(file_name)
    else:
        return pd.DataFrame(columns=[
            "S.No.", "Invoice Date", "Invoice No", "Customer",
            "Destination", "Dispatch Date", "Transporter",
            "Vehicle", "Freight Charges"])

def save_data(df):
    df.to_excel(file_name, index=False)

# App Layout and Styling
st.set_page_config(page_title="Invoice Tracker", layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #f0f4f8;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stTextInput > div > input {
            background-color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📋 Invoice Tracker")
df = load_data()

# Input Form
with st.form("entry_form", clear_on_submit=True):
    st.subheader("➕ Add New Invoice")
    col1, col2, col3 = st.columns(3)
    with col1:
        invoice_date = st.date_input("Invoice Date")
        invoice_no = st.text_input("Invoice No")
        customer = st.text_input("Customer")
    with col2:
        destination = st.text_input("Destination")
        dispatch_date = st.date_input("Dispatch Date")
        transporter = st.text_input("Transporter")
    with col3:
        vehicle = st.text_input("Vehicle")
        freight_charges = st.number_input("Freight Charges", min_value=0.0)
    submitted = st.form_submit_button("✅ Add Entry")

    if submitted:
        new_entry = {
            "S.No.": 1 if df.empty else df["S.No."].max() + 1,
            "Invoice Date": invoice_date,
            "Invoice No": invoice_no,
            "Customer": customer,
            "Destination": destination,
            "Dispatch Date": dispatch_date,
            "Transporter": transporter,
            "Vehicle": vehicle,
            "Freight Charges": freight_charges
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        save_data(df)
        st.success(f"✅ Entry added with S.No. {new_entry['S.No.']}")

# Delete Entry
st.subheader("🗑️ Delete an Entry")
delete_id = st.number_input("Enter S.No. to delete", min_value=1, step=1)
if st.button("Delete Entry"):
    if delete_id in df["S.No."].values:
        df = df[df["S.No."] != delete_id]
        df.reset_index(drop=True, inplace=True)
        df["S.No."] = range(1, len(df)+1)
        save_data(df)
        st.success(f"✅ Deleted entry with S.No. {delete_id}")
    else:
        st.warning("⚠️ Entry not found.")

# Search & Display Data
st.subheader("🔍 Search & Manage")
query = st.text_input("Search anything...")
if query:
    filtered_df = df[df.apply(lambda row: query.lower() in row.astype(str).str.lower().to_string(), axis=1)]
else:
    filtered_df = df

if st.button("🔄 Reload Data"):
    df = load_data()
    st.success("✅ Data reloaded")

st.markdown("### 📊 Invoice Data")
st.dataframe(filtered_df, use_container_width=True)

st.download_button("📥 Download Excel", data=df.to_excel(index=False), file_name=file_name, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")





