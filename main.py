import os
import requests
import pandas as pd

# PATHS
os.makedirs("data/bronze", exist_ok=True)
os.makedirs("data/silver", exist_ok=True)
os.makedirs("data/gold", exist_ok=True)

# ---------------- BRONZE ----------------
def fetch_product(barcode: str) -> dict:
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# ---------------- SILVER ----------------
def clean_product_data(raw_data: dict) -> dict:
    product = raw_data.get("product", {})
    return {
        "name": product.get("product_name", "").strip().title(),
        "brands": product.get("brands", "").lower(),
        "categories": product.get("categories", "").split(","),
        "nutriscore": product.get("nutriscore_grade", "").upper(),
        "ingredients_text": product.get("ingredients_text", "").strip(),
        "energy_kcal": product.get("nutriments", {}).get("energy-kcal_100g", None),
        "fat": product.get("nutriments", {}).get("fat_100g", None),
        "sugars": product.get("nutriments", {}).get("sugars_100g", None),
    }

# ---------------- GOLD ----------------
def summarize_product(data: dict) -> dict:
    return {
        "name": data["name"],
        "nutriscore": data["nutriscore"],
        "energy_kcal": data["energy_kcal"],
        "summary": f"{data['name']} tem {data['energy_kcal']} kcal por 100g e nutri-score {data['nutriscore']}."
    }

# ---------------- SAVE  ----------------
def save_to_csv(data: dict, path: str):
    df = pd.DataFrame([data])  
    df.to_csv(path, index=False)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    barcode = "3017620429484"  # Nutella
    try:
        # Bronze
        raw = fetch_product(barcode)
        save_to_csv(raw, "data/bronze/product_raw.csv")

        # Silver
        cleaned = clean_product_data(raw)
        save_to_csv(cleaned, "data/silver/product_clean.csv")

        # Gold
        summary = summarize_product(cleaned)
        save_to_csv(summary, "data/gold/product_summary.csv")

        print("Pipeline executado com sucesso!")
    except Exception as e:
        print("Erro:", e)


