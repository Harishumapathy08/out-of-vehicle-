import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

# App title and style
st.set_page_config(page_title="Invoice Entry", layout="wide")
st.markdown(
    """
    <style>
        body {
            background-color: #f0f8ff;
        }
        .stApp {
            background-color: #f0f8ff;
        }
        .big-font {
            font-size: 30px !important;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("<div class='big-font'>📋 Monthly Invoice Entry System</div>", unsafe_allow_html=True)

# File name based on current month
month_name = datetime.now().strftime("%B_%Y")
file_name = f"invoices_{month_name}.xlsx"

# Ensure file exists
if not os.path.exists(file_name):
    df_init = pd.DataFrame(columns=[
        "S.No.", "Invoice Date", "Invoice No", "Customer",
        "Destination", "Dispatch Date", "Transporter",
        "Vehicle", "Freight Charges"
    ])
    df_init.to_excel(file_name, index=False)

# Load data
df = pd.read_excel(file_name)

# Add Entry
with st.form("Add New Invoice"):
    st.subheader("➕ Add Invoice Details")
    col1, col2, col3, col4 = st.columns(4)
    col5, col6, col7, col8 = st.columns(4)

    invoice_date = col1.date_input("Invoice Date", value=datetime.today())
    invoice_no = col2.text_input("Invoice No")
    customer = col3.text_input("Customer")
    destination = col4.text_input("Destination")
    dispatch_date = col5.date_input("Dispatch Date", value=datetime.today())
    transporter = col6.text_input("Transporter")
    vehicle = col7.text_input("Vehicle")
    freight_charges = col8.number_input("Freight Charges", step=0.01)

    submitted = st.form_submit_button("➕ Add Entry")
    if submitted:
        new_entry = {
            "S.No.": len(df) + 1,
            "Invoice Date": invoice_date.strftime("%Y-%m-%d"),
            "Invoice No": invoice_no,
            "Customer": customer,
            "Destination": destination,
            "Dispatch Date": dispatch_date.strftime("%Y-%m-%d"),
            "Transporter": transporter,
            "Vehicle": vehicle,
            "Freight Charges": freight_charges
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df["S.No."] = range(1, len(df) + 1)
        df.to_excel(file_name, index=False)
        st.success("✅ Invoice entry added successfully!")

# View Data
st.subheader("📄 All Invoice Entries")
if not df.empty:
    st.dataframe(df, use_container_width=True)

    # Delete row
    st.subheader("🗑️ Delete Entry by S.No.")
    delete_sno = st.number_input("Enter S.No. to delete", min_value=1, max_value=len(df), step=1)
    if st.button("Delete Entry"):
        df = df[df["S.No."] != delete_sno].reset_index(drop=True)
        df["S.No."] = range(1, len(df) + 1)
        df.to_excel(file_name, index=False)
        st.success(f"✅ Entry with S.No. {delete_sno} deleted.")

    # Download Excel
    st.subheader("⬇️ Download Excel File")
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    st.download_button(
        "📥 Download Excel",
        data=excel_buffer,
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("No entries found yet. Add a new invoice above.")





