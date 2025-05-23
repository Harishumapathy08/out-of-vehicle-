import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Invoice Tracker", layout="wide")

# Background and header styling
st.markdown("""
    <style>
        body {
            background-color: #f0f4f8;
        }
        .main {
            background-color: #f0f4f8;
            padding: 2rem;
        }
        .stApp {
            background-color: #f0f4f8;
        }
    </style>
""", unsafe_allow_html=True)

# File and column setup
DATA_FILE = "data.xlsx"
COLUMNS = ["S.No.", "Invoice Date", "Invoice No", "Customer",
           "Destination", "Dispatch Date", "Transporter",
           "Vehicle", "Freight Charges"]

if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=COLUMNS).to_excel(DATA_FILE, index=False)

def load_data():
    return pd.read_excel(DATA_FILE)

def save_data(df):
    df.to_excel(DATA_FILE, index=False)

st.title("📦 Invoice Entry Tracker")

df = load_data()

# Search bar
query = st.text_input("🔍 Search")
if query:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(query.lower()).any(), axis=1)]
else:
    filtered_df = df

st.subheader("🧾 Current Records")
st.dataframe(filtered_df, use_container_width=True)

# Add Entry Form
with st.form("entry_form"):
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
        st.success("New invoice added!")

# Download Excel
buffer = BytesIO()
df.to_excel(buffer, index=False)
buffer.seek(0)
st.download_button("📥 Download Excel", buffer, file_name="data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")



