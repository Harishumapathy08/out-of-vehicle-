from flask import Flask, request, redirect, send_file
from flask import render_template_string
import pandas as pd
import os

app = Flask(__name__)
DATA_FILE = "data.xlsx"

# Create Excel file if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        "S.No.", "Invoice Date", "Invoice No", "Customer",
        "Destination", "Dispatch Date", "Transporter",
        "Vehicle", "Freight Charges"
    ])
    df.to_excel(DATA_FILE, index=False)

def load_data():
    return pd.read_excel(DATA_FILE)

def save_data(df):
    df.to_excel(DATA_FILE, index=False)

# Load HTML from file
def load_html():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route("/", methods=["GET"])
def index():
    df = load_data()
    query = request.args.get("query", "").lower()
    if query:
        df = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)]
    data = df.fillna("").to_dict(orient="records")
    html = load_html()
    return render_template_string(html, data=data, query=query)

@app.route("/submit", methods=["POST"])
def submit():
    df = load_data()
    new_entry = {
        "S.No.": len(df) + 1,
        "Invoice Date": request.form.get("invoice_date"),
        "Invoice No": request.form.get("invoice_no"),
        "Customer": request.form.get("customer"),
        "Destination": request.form.get("destination"),
        "Dispatch Date": request.form.get("disp_date"),
        "Transporter": request.form.get("transporter"),
        "Vehicle": request.form.get("vehicle"),
        "Freight Charges": request.form.get("freight_charges")
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    save_data(df)
    return redirect("/")

@app.route("/delete/<int:sno>", methods=["POST"])
def delete(sno):
    df = load_data()
    df = df[df["S.No."] != sno].reset_index(drop=True)
    df["S.No."] = range(1, len(df) + 1)
    save_data(df)
    return redirect("/")

@app.route("/download")
def download():
    return send_file(DATA_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)


