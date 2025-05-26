import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="Out of Vehicle Entry", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #eef5ff;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚚 Out of Vehicle Entry Form")

# Get current month as sheet name
month_sheet = datetime.now().strftime("%B")

excel_file = "data.xlsx"

# Initialize or load Excel
if not os.path.exists(excel_file):
    df = pd.DataFrame(columns=[
        "S.No.", "Invoice Date", "Invoice No", "Customer",
        "Destination", "Dispatch Date", "Transporter",
        "Vehicle", "Freight Charges", "Vehicle Capacity",
        "Product", "Qty"
    ])
    df.to_excel(excel_file, sheet_name=month_sheet, index=False)
else:
    try:
        df = pd.read_excel(excel_file, sheet_name=month_sheet)
    except:
        df = pd.DataFrame(columns=[
            "S.No.", "Invoice Date", "Invoice No", "Customer",
            "Destination", "Dispatch Date", "Transporter",
            "Vehicle", "Freight Charges", "Vehicle Capacity",
            "Product", "Qty"
        ])

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
        freight_charges = st.number_input("Freight Charges", min_value=0.0, step=0.1)
        vehicle_capacity = st.text_input("Vehicle Capacity (e.g. 5 tons)")

    product = st.text_input("Product")
    qty = st.number_input("Quantity", min_value=0, step=1)

    submitted = st.form_submit_button("Submit")

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
            "Freight Charges": freight_charges,
            "Vehicle Capacity": vehicle_capacity,
            "Product": product,
            "Qty": qty
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        with pd.ExcelWriter(excel_file, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=month_sheet, index=False)
        st.success("Data saved successfully.")

st.markdown("## 📄 Saved Entries")

if not df.empty:
    st.dataframe(df, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Load Latest Data"):
            df = pd.read_excel(excel_file, sheet_name=month_sheet)
            st.experimental_rerun()

    with col2:
        delete_index = st.number_input("Enter S.No. to Delete", min_value=1, max_value=len(df), step=1)
        if st.button("❌ Delete Entry"):
            df = df[df["S.No."] != delete_index].reset_index(drop=True)
            df["S.No."] = range(1, len(df) + 1)
            with pd.ExcelWriter(excel_file, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                df.to_excel(writer, sheet_name=month_sheet, index=False)
            st.success(f"Entry {delete_index} deleted.")
            st.experimental_rerun()

    with col3:
        output = BytesIO()
        df.to_excel(output, index=False)
        st.download_button(
            "📥 Download Excel",
            data=output.getvalue(),
            file_name=f"{month_sheet}_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

