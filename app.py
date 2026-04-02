from flask import Flask, request, render_template, jsonify, send_file
import pickle
import numpy as np
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph

app = Flask(__name__)

# Load ML model
model = pickle.load(open("D:/ECOPACKAI_ML1/model.pkl", "rb"))

# Store latest results
latest_results = []


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict_form', methods=['POST'])
def predict_form():
    global latest_results

    try:
        product = request.form['product']
        fragility = request.form['fragility']
        weight = request.form['weight']
        protection = request.form['protection']

        fragility_map = {"low": 0, "medium": 1, "high": 2}
        weight_map = {"light": 3, "medium": 6, "heavy": 9}
        protection_map = {"low": 4, "medium": 7, "high": 10}

        fragility_val = fragility_map[fragility]
        weight_val = weight_map[weight]
        strength = protection_map[protection]

        materials = {
            "Paper": (9, 1),
            "Cardboard": (8, 1),
            "Glass": (6, 1),
            "Metal": (5, 1),
            "Plastic": (2, 0)
        }

        results = []

        for mat, (bio, rec) in materials.items():
            features = np.array([[strength, bio, rec, fragility_val]])
            score = model.predict(features)[0]
            eco = (bio * 2 + rec * 2) - fragility_val

            results.append({
                "material": mat,
                "score": round(float(score), 2),
                "eco": round(float(eco), 2)
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)
        latest_results = results[:5]

        # Business metrics
        co2_reduction = round(50 + results[0]['eco'], 2)
        cost_savings = round(20 + results[0]['score'], 2)

        return render_template(
            'index.html',
            results=latest_results,
            co2=co2_reduction,
            cost=cost_savings
        )

    except Exception as e:
        return render_template('index.html', error=str(e))


# API (Module 5)
@app.route('/api/predict', methods=['POST'])
def api_predict():
    return jsonify({"status": "success"})


# Export Excel
@app.route('/export_excel')
def export_excel():
    file_path = "report.xlsx"
    df = pd.DataFrame(latest_results)
    df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True)


# Export PDF
@app.route('/export_pdf')
def export_pdf():
    file_path = "report.pdf"

    doc = SimpleDocTemplate(file_path)
    elements = []

    elements.append(Paragraph("EcoPack AI Sustainability Report", None))

    for r in latest_results:
        elements.append(Paragraph(
            f"{r['material']} - Score: {r['score']} - Eco: {r['eco']}",
            None
        ))

    doc.build(elements)

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)