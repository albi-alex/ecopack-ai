from flask import Flask, render_template, request, send_file
import pandas as pd
import io
import os
import psycopg2

app = Flask(__name__)

# =========================
# DATABASE CONNECTION
# =========================
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(
        DATABASE_URL,
        sslmode='require'
    )

# 🔥 Smart Recommendation Logic
def get_recommendations(product, fragility, weight, protection):

    materials = [
        {"material": "Paper", "score": 9},
        {"material": "Cardboard", "score": 8},
        {"material": "Bioplastic", "score": 7},
        {"material": "Bubble Wrap", "score": 4},
        {"material": "Foam", "score": 3}
    ]

    for m in materials:
        if m["score"] >= 8:
            m["eco"] = "High"
        elif m["score"] >= 5:
            m["eco"] = "Medium"
        else:
            m["eco"] = "Low"

    return materials

# 🏠 Home Page
@app.route('/')
def home():
    return render_template('index.html')

# 🔮 Prediction Route
@app.route('/predict_form', methods=['POST'])
def predict_form():

    product = request.form['product']
    fragility = request.form['fragility']
    weight = request.form['weight']
    protection = request.form['protection']

    # ✅ SAFE DB INSERT (won’t crash app)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO user_logs (product, fragility, weight, protection) VALUES (%s, %s, %s, %s)",
            (product, fragility, weight, protection)
        )

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print("DB Error:", e)

    results = get_recommendations(product, fragility, weight, protection)

    co2 = 30
    cost = 20

    return render_template(
        'index.html',
        results=results,
        co2=co2,
        cost=cost
    )

# 📊 Export Excel
@app.route('/export_excel')
def export_excel():

    data = [
        ["Paper", 9, "High"],
        ["Cardboard", 8, "High"],
        ["Bioplastic", 7, "Medium"],
        ["Bubble Wrap", 4, "Medium"],
        ["Foam", 3, "Low"]
    ]

    df = pd.DataFrame(data, columns=["Material", "Score", "Eco"])

    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(
        output,
        download_name="ecopack_report.xlsx",
        as_attachment=True
    )

# 🚧 PDF (disabled)
@app.route('/export_pdf')
def export_pdf():
    return "PDF feature coming soon 🚧"

# 🚀 REQUIRED FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)