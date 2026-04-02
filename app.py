from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# 🔥 MATCHES YOUR FORM
@app.route("/predict_form", methods=["POST"])
def predict_form():
    try:
        product = request.form.get("product")
        fragility = request.form.get("fragility")
        weight = request.form.get("weight")
        protection = request.form.get("protection")

        # 🔥 Dummy recommendation logic (replace later with ML)
        results = [
            {"material": "Paper", "score": 8.5, "eco": "High"},
            {"material": "Bioplastic", "score": 7.8, "eco": "Medium"},
            {"material": "Cardboard", "score": 7.2, "eco": "High"},
        ]

        co2 = 30
        cost = 20

        return render_template(
            "index.html",
            results=results,
            co2=co2,
            cost=cost
        )

    except Exception as e:
        return f"Error: {str(e)}"


# 🔥 REQUIRED FOR RENDER (VERY IMPORTANT)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)