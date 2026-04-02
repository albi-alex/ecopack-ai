import pandas as pd

# Load data
df = pd.read_csv("D:/ECOPACKAI_ML1/materials_featured.csv")

# -------------------------------
# 1. Handle missing values
# -------------------------------
df = df.fillna(0)

# -------------------------------
# 2. Normalize numerical features
# -------------------------------
df["weight_capacity"] = df["weight_capacity"] / df["weight_capacity"].max()
df["co2_score"] = df["co2_score"] / df["co2_score"].max()
df["strength"] = df["strength"] / df["strength"].max()

# -------------------------------
# 3. Encode categorical data
# -------------------------------
df["fragility"] = df["fragility"].map({
    "low": 0,
    "medium": 1,
    "high": 2
})

# -------------------------------
# 4. Additional Feature Engineering
# -------------------------------

# Cost Efficiency Index (simple assumption)
df["cost_efficiency"] = df["strength"] / (df["co2_score"] + 0.1)

# Material Suitability Score
df["suitability_score"] = (
    df["strength"] +
    df["biodegradability"] +
    df["recyclability"] -
    df["co2_score"]
)

# -------------------------------
# 5. Validate data (summary)
# -------------------------------
print(df.describe())

# Save final dataset
df.to_csv("D:/ECOPACKAI_ML1/materials_final.csv", index=False)

print("✅ Module 2 Step completed!")