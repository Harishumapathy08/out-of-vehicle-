import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
import os

st.set_page_config(page_title="Invoice Entry", layout="wide")

# Apply custom background
page_bg_color = """
<style>
body {
    background-color: #e8f4f8;
}
</style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)

# Create directory for storing files
if not os.path.exists("data"):
    os.makedirs("data")

# Get file name based on current month
month_name = datetime.now().strftime("%B")
file_name = f"data/{month_name}.xlsx"

# Load data
if os.path.exists(file_name):
    df = pd.read_excel(file_name)
else:
    df = pd.DataFrame(columns=[
        "S.No.", "Invoice Date", "Invoice No", "Customer",
        "Destination", "Dispatch Date", "Transporter",
        "Vehicle", "Freight Charges"
    ])

st.title("🧾 Invoice Entry System")

# Input form
st.header("Add New Invoice")
with st.form("entry_form"):
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
        freight_charges = st.number_input("Freight Charges", min_value=0.0, format="%.2f")

    submitted = st.form_submit_button("➕ Add Entry")
    if submitted:
        new_entry = {
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
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_excel(file_name, index=False)
        st.success("Entry added successfully!")

# View and delete
st.header("📄 Current Entries")

colA, colB = st.columns([3, 1])

with colA:
    st.dataframe(df, use_container_width=True)

with colB:
    if len(df) > 0:
        delete_index = st.number_input("S.No. to Delete", min_value=1, max_value=len(df), step=1)
        if st.button("🗑️ Delete Entry"):
            df = df[df["S.No."] != delete_index]
            df.reset_index(drop=True, inplace=True)
            df["S.No."] = range(1, len(df) + 1)
            df.to_excel(file_name, index=False)
            st.success(f"Deleted entry S.No. {delete_index}")
    else:
        st.info("No entries to delete.")

# Download button
st.markdown("### 📥 Download Data")
output = BytesIO()
df.to_excel(output, index=False)
st.download_button(
    "⬇️ Download Excel",
    data=output.getvalue(),
    file_name=f"{month_name}_invoices.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
