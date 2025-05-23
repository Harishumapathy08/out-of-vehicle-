import streamlit as st
import pandas as pd
import os
from io import BytesIO

DATA_FILE = "data.xlsx"

# Ensure file exists
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["S.No.", "Vehicle No", "Material", "Date", "Time", "Weight"])
    df_init.to_excel(DATA_FILE, index=False)

def load_data():
    return pd.read_excel(DATA_FILE)

def save_data(df):
    df.to_excel(DATA_FILE, index=False)

# Title
st.title("Vehicle Entry Logger")

# Load data
df = load_data()

# Search/filter
query = st.text_input("Search")
if query:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(query.lower()).any(), axis=1)]
else:
    filtered_df = df

# Display data
st.dataframe(filtered_df)

# Form to add new data
with st.form("add_form"):
    st.subheader("Add New Entry")
    vehicle = st.text_input("Vehicle No")
    material = st.text_input("Material")
    date = st.date_input("Date")
    time = st.time_input("Time")
    weight = st.number_input("Weight", step=0.01)
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        new_row = {
            "S.No.": len(df) + 1,
            "Vehicle No": vehicle,
            "Material": material,
            "Date": date,
            "Time": time.strftime("%H:%M:%S"),
            "Weight": weight
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("Entry added!")

# Download
buffer = BytesIO()
df.to_excel(buffer, index=False)
buffer.seek(0)
st.download_button("Download Excel", buffer, file_name="data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")



