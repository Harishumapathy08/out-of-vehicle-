import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Define Excel file path with current month and year
month_name = datetime.now().strftime("%B")
year = datetime.now().strftime("%Y")
EXCEL_FILE = f"{month_name}_{year}.xlsx"

# Required columns
COLUMNS = [
    "S.No.", "Invoice Date", "Invoice No", "Customer",
    "Destination", "Dispatch Date", "Transporter",
    "Vehicle", "Freight Charges"
]

# Load or initialize data
def load_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    else:
        return pd.DataFrame(columns=COLUMNS)

def save_data(df):
    df.to_excel(EXCEL_FILE, index=False)

# UI Customizations
st.set_page_config(page_title="Invoice Tracker", layout="wide")
st.markdown("<style>body { background-color: #eef3f9; }</style>", unsafe_allow_html=True)

st.title("📄 Invoice Tracker")

# Load data
df = load_data()

# Entry Form
st.header("➕ Add New Entry")
with st.form("entry_form"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        invoice_date = st.date_input("Invoice Date")
        invoice_no = st.text_input("Invoice No")
    with col2:
        customer = st.text_input("Customer")
        destination = st.text_input("Destination")
    with col3:
        dispatch_date = st.date_input("Dispatch Date")
        transporter = st.text_input("Transporter")
    with col4:
        vehicle = st.text_input("Vehicle")
        freight_charges = st.number_input("Freight Charges", min_value=0.0, step=0.01)

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
        df = df.append(new_entry, ignore_index=True)
        save_data(df)
        st.success(f"✅ Entry added with S.No. {new_entry['S.No.']}")

# Delete Entry
st.header("🗑️ Delete an Entry")
del_no = st.number_input("Enter S.No. to delete", min_value=1, step=1)
if st.button("❌ Delete Entry"):
    if del_no in df["S.No."].values:
        df = df[df["S.No."] != del_no].reset_index(drop=True)
        df["S.No."] = range(1, len(df) + 1)
        save_data(df)
        st.success(f"✅ Deleted entry with S.No. {int(del_no)}")
    else:
        st.warning("⚠️ S.No. not found.")

# Search/Filter
st.header("🔍 Search & Manage")
query = st.text_input("Search anything...")
if query:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
else:
    filtered_df = df

if st.button("🔄 Reload Data"):
    df = load_data()
    filtered_df = df
    st.info("🔄 Data reloaded from Excel.")

# Display Data
st.subheader("📊 Invoice Data")
st.dataframe(filtered_df, use_container_width=True)

# Download Button
st.download_button("⬇️ Download Excel", data=df.to_excel(index=False), file_name=EXCEL_FILE, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")





