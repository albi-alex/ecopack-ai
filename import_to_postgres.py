import pandas as pd
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="ecopack",
    user="postgres",
    password="postgres123",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Load materials CSV
materials_df = pd.read_csv("D:/ECOPACKAI_ML1/materials_cleaned.csv")

# Insert materials data
for _, row in materials_df.iterrows():
    cur.execute("""
        INSERT INTO materials(material, strength, weight_capacity, biodegradability, co2_score, recyclability, fragility)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row['material'],
        row['strength'],
        row['weight_capacity'],
        row['biodegradability'],
        row['co2_score'],
        row['recyclability'],
        row['fragility']
    ))

# Load products CSV
products_df = pd.read_csv("D:/ECOPACKAI_ML1/products.csv")

# Insert products data
for _, row in products_df.iterrows():
    cur.execute("""
        INSERT INTO products(product_type, fragility, weight, category)
        VALUES (%s, %s, %s, %s)
    """, (
        row['product_type'],
        row['fragility'],
        row['weight'],
        row['category']
    ))

# Commit changes
conn.commit()

# Close connection
cur.close()
conn.close()

print("✅ Data imported successfully!")