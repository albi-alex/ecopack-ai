from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template("index.html")


# Prediction route
@app.route("/predict_form", methods=["POST"])
def predict_form():
    try:
        product = request.form.get("product")
        fragility = request.form.get("fragility")
        weight = request.form.get("weight")
        protection = request.form.get("protection")

        # 🔥 Smart rule-based system
        materials = [
            {"material": "Paper", "eco": 9},
            {"material": "Cardboard", "eco": 8},
            {"material": "Bioplastic", "eco": 7},
            {"material": "Bubble Wrap", "eco": 4},
            {"material": "Foam", "eco": 3},
        ]

        results = []

        for m in materials:
            score = m["eco"]

            if fragility == "high":
                score += 2
            if weight == "heavy":
                score -= 1
            if protection == "high":
                score += 2

            results.append({
                "material": m["material"],
                "score": round(score, 2),
                "eco": "High" if m["eco"] > 7 else "Medium"
            })

        # Sort and pick top 5
        results = sorted(results, key=lambda x: x["score"], reverse=True)[:5]

        co2 = 25 + len(results)
        cost = 15 + len(results)

        return render_template(
            "index.html",
            results=results,
            co2=co2,
            cost=cost
        )

    except Exception as e:
        return f"Error: {str(e)}"


# Required for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)