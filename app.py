import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Invoice Tracker", layout="wide")

# CSS for background color
st.markdown("""
    <style>
        .stApp {
            background-color: #f2f6fc;
            padding: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "data.xlsx"
COLUMNS = ["S.No.", "Invoice Date", "Invoice No", "Customer",
           "Destination", "Dispatch Date", "Transporter",
           "Vehicle", "Freight Charges"]

# Initialize file
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=COLUMNS).to_excel(DATA_FILE, index=False)

def load_data():
    return pd.read_excel(DATA_FILE)

def save_data(df):
    df.to_excel(DATA_FILE, index=False)

# Load data
df = load_data()

st.title("📦 Invoice Entry Tracker")

# --- ADD NEW ENTRY ---
with st.form("add_form"):
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
        freight_charges = st.number_input("Freight Charges", step=0.01)

    submit = st.form_submit_button("✅ Add Entry")
    if submit:
        new_row = {
            "S.No.": len(df) + 1,
            "Invoice Date": invoice_date,
            "Invoice No": invoice_no,
            "Customer": customer,
            "Destination": destination,
            "Dispatch Date": dispatch_date,
            "Transporter": transporter,
            "Vehicle": vehicle,
            "Freight Charges": freight_charges
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("✅ Invoice added!")


# --- DELETE ENTRY ---
st.subheader("🗑️ Delete an Entry")
delete_sn = st.number_input("Enter S.No. to delete", min_value=1, step=1)
if st.button("Delete Entry"):
    if delete_sn in df["S.No."].values:
        df = df[df["S.No."] != delete_sn].reset_index(drop=True)
        df["S.No."] = range(1, len(df) + 1)
        save_data(df)
        st.success(f"✅ Deleted entry with S.No. {delete_sn}")
    else:
        st.warning("⚠️ S.No. not found.")

# --- SEARCH + LOAD BUTTON ---
st.subheader("🔍 Search & Manage")
colA, colB = st.columns([3, 1])
with colA:
    query = st.text_input("Search anything...")
with colB:
    if st.button("🔁 Reload Data"):
        df = load_data()
        st.success("🔄 Data reloaded")

# Filter logic
filtered_df = df.copy()
if query:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(query.lower()).any(), axis=1)]

# --- DISPLAY TABLE ---
st.subheader("📊 Invoice Data")
st.dataframe(filtered_df, use_container_width=True)

# --- DOWNLOAD EXCEL ---
buffer = BytesIO()
df.to_excel(buffer, index=False)
buffer.seek(0)
st.download_button("📥 Download Excel", buffer, "data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")




