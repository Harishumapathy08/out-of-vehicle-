from flask import Flask, render_template, request, redirect, send_file, jsonify
import pandas as pd
import os

app = Flask(__name__)

DATA_FILE = "data.xlsx"

# Ensure the data file exists with appropriate headers
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        "S.No.", "Invoice Date", "Invoice No", "Customer", "Destination",
        "Dispatch Date", "Transporter", "Vehicle", "Freight Charges"
    ])
    df.to_excel(DATA_FILE, index=False)

def load_data():
    return pd.read_excel(DATA_FILE)

def save_data(df):
    df.to_excel(DATA_FILE, index=False)

@app.route("/", methods=["GET"])
def index():
    df = load_data()
    query = request.args.get("query", "").lower()
    if query:
        filtered_df = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)]
    else:
        filtered_df = df

    if not filtered_df.empty:
        data = filtered_df.fillna("").to_dict(orient="records")
    else:
        data = []

    return render_template("index.html", data=data, query=query)

@app.route("/add", methods=["POST"])
def add():
    df = load_data()
    new_entry = {
        "S.No.": len(df) + 1,
        "Invoice Date": request.form["invoice_date"],
        "Invoice No": request.form["invoice_no"],
        "Customer": request.form["customer"],
        "Destination": request.form["destination"],
        "Dispatch Date": request.form["disp_date"],
        "Transporter": request.form["transporter"],
        "Vehicle": request.form["vehicle"],
        "Freight Charges": request.form["freight_charges"]
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
    return send_file(DATA_FILE, as_attachment=True, download_name="invoice_data.xlsx")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file and file.filename.endswith((".xls", ".xlsx")):
        df = pd.read_excel(file)
        save_data(df)
    return redirect("/")

@app.route("/events")
def events():
    df = load_data()
    events = []
    for _, row in df.iterrows():
        events.append({
            "title": f"Invoice #{row['Invoice No']} - {row['Customer']}",
            "start": str(row["Dispatch Date"])
        })
    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True)

