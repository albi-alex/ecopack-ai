import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

from xgboost import XGBRegressor

# -------------------------------
# 1. Load dataset
# -------------------------------
df = pd.read_csv("D:/ECOPACKAI_ML1/materials_final.csv")

# -------------------------------
# 2. Suitability Model
# -------------------------------
X = df[[
    "strength",
    "biodegradability",
    "recyclability",
    "fragility"
]]

# Add noise
y = df["suitability_score"] + np.random.normal(0, 1.0, len(df))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=30,
    max_depth=3,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n--- Suitability Model ---")
print("MSE:", mse)
print("RMSE:", rmse)
print("MAE:", mae)
print("R2:", r2)

# Save model
pickle.dump(model, open("D:/ECOPACKAI_ML1/model.pkl", "wb"))

# -------------------------------
# 3. CO2 Prediction Model (XGBoost)
# -------------------------------
print("\n--- CO2 Prediction Model (XGBoost) ---")

X_co2 = df[[
    "strength",
    "biodegradability",
    "recyclability",
    "fragility"
]]

y_co2 = df["co2_score"]

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X_co2, y_co2, test_size=0.2, random_state=42
)

co2_model = XGBRegressor(
    n_estimators=50,
    max_depth=3,
    learning_rate=0.1
)

co2_model.fit(X_train_c, y_train_c)

y_pred_c = co2_model.predict(X_test_c)

# Evaluation
mse_c = mean_squared_error(y_test_c, y_pred_c)
rmse_c = np.sqrt(mse_c)
mae_c = mean_absolute_error(y_test_c, y_pred_c)
r2_c = r2_score(y_test_c, y_pred_c)

print("CO2 MSE:", mse_c)
print("CO2 RMSE:", rmse_c)
print("CO2 MAE:", mae_c)
print("CO2 R2:", r2_c)

# -------------------------------
# 4. Cost Prediction Model
# -------------------------------
print("\n--- Cost Prediction Model ---")

df["cost"] = (df["strength"] * 2) + (df["co2_score"] * 5)

X_cost = df[[
    "strength",
    "biodegradability",
    "recyclability",
    "fragility"
]]

y_cost = df["cost"]

X_train_cost, X_test_cost, y_train_cost, y_test_cost = train_test_split(
    X_cost, y_cost, test_size=0.2, random_state=42
)

cost_model = RandomForestRegressor(
    n_estimators=30,
    max_depth=3,
    random_state=42
)

cost_model.fit(X_train_cost, y_train_cost)

y_pred_cost = cost_model.predict(X_test_cost)

# Evaluation
mse_cost = mean_squared_error(y_test_cost, y_pred_cost)
rmse_cost = np.sqrt(mse_cost)
mae_cost = mean_absolute_error(y_test_cost, y_pred_cost)
r2_cost = r2_score(y_test_cost, y_pred_cost)

print("Cost MSE:", mse_cost)
print("Cost RMSE:", rmse_cost)
print("Cost MAE:", mae_cost)
print("Cost R2:", r2_cost)

# -------------------------------
# 5. FIXED MATERIAL RANKING SYSTEM
# -------------------------------
print("\n--- Material Ranking ---")

# Take only unique materials (avoid duplicates)
df_unique = df.groupby("material").mean().reset_index()

# Predict using model
X_unique = df_unique[[
    "strength",
    "biodegradability",
    "recyclability",
    "fragility"
]]

df_unique["predicted_score"] = model.predict(X_unique)

# Improve ranking logic (hybrid scoring)
df_unique["final_score"] = (
    df_unique["predicted_score"]
    + (1 - df_unique["co2_score"]) * 2
    + df_unique["recyclability"] * 1.5
)

# Sort
ranking = df_unique.sort_values(by="final_score", ascending=False)

print(ranking[["material", "final_score"]])