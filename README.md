# 🥫 Open Food Medallion Pipeline

This is a simple Python project built to **practice the Medallion Architecture** using data from the [Open Food Facts API](https://world.openfoodfacts.org/data).

The pipeline follows the Medallion structure with:

- **Bronze Layer**: Raw data ingestion
- **Silver Layer**: Data cleaning and transformation
- **Gold Layer**: Aggregated and summarized output

## 🧪 Purpose

The goal is educational: to get hands-on experience with the **Bronze → Silver → Gold** data pipeline concept using real, somewhat messy, open data.

---

## 🧰 Tech Stack

- Python 3.9+
- [Pandas](https://pandas.pydata.org/)
- [Requests](https://docs.python-requests.org/)
- Open Food Facts REST API

---

## 📦 Project Structure

```
open-food-medallion/
├── data/
│   ├── bronze/   # Raw API JSON
│   ├── silver/   # Cleaned, structured data
│   └── gold/     # Summary/aggregated info
├── main.py       # Pipeline entry point
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the pipeline:
```bash
python main.py
```

3. Output CSVs will be saved under the `data/` folder in each layer's subfolder.

---

## 📡 Example Barcode Used

- `3017620429484` → Nutella (you can replace it with any product barcode from Open Food Facts)

---

## 📚 Learn More

- [Open Food Facts API](https://world.openfoodfacts.org/data)
- [Medallion Architecture (Databricks)](https://www.databricks.com/glossary/medallion-architecture)


