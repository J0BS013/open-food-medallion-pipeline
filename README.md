# Open Food Medallion Pipeline

A Python pipeline that fetches product data from the [Open Food Facts API](https://world.openfoodfacts.org/data) and processes it through a **Medallion Architecture** (Bronze → Silver → Gold).

---

## Architecture

```
Open Food Facts API
        │
        ▼
┌───────────────┐
│    BRONZE     │  Raw JSON per product (data/bronze/<barcode>.json)
└───────┬───────┘
        │  fetch + validate
        ▼
┌───────────────┐
│    SILVER     │  Cleaned & structured CSV per product (data/silver/<barcode>.csv)
└───────┬───────┘
        │  normalize fields, extract nutriments
        ▼
┌───────────────┐
│     GOLD      │  Aggregated insights (data/gold/)
└───────────────┘
      ├── products_ranking.csv   → all products ranked by nutriscore + kcal
      └── nutrition_summary.csv  → averages, best/worst product
```

---

## Tech Stack

- Python 3.9+
- [Pandas](https://pandas.pydata.org/)
- [Requests](https://docs.python-requests.org/)
- Open Food Facts REST API

---

## Project Structure

```
open-food-medallion-pipeline/
├── pipeline/
│   ├── bronze.py      # API ingestion → raw JSON
│   ├── silver.py      # Cleaning & normalization → structured CSV
│   └── gold.py        # Aggregation & ranking → insight CSVs
├── data/
│   ├── bronze/        # One .json file per barcode
│   ├── silver/        # One .csv file per barcode
│   └── gold/          # products_ranking.csv + nutrition_summary.csv
├── main.py            # CLI entry point & pipeline orchestrator
└── requirements.txt
```

---

## How to Run

**1. Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. Run the pipeline with one or more barcodes:**
```bash
python main.py 3017620429484 7622210449283 5000159484695
```

**3. Check the output:**
```
data/
├── bronze/
│   ├── 3017620429484.json
│   └── ...
├── silver/
│   ├── 3017620429484.csv
│   └── ...
└── gold/
    ├── products_ranking.csv
    └── nutrition_summary.csv
```

---

## Gold Layer Output Example

**`products_ranking.csv`** — products ranked by nutriscore, then by energy:

| rank | name    | nutriscore | energy_kcal | fat  | sugars |
|------|---------|------------|-------------|------|--------|
| 1    | Twix    | E          | 280.7       | 14.6 | 25.5   |
| 2    | Prince  | E          | 466.0       | 17.0 | 32.0   |
| 3    | Nutella | E          | 539.0       | 30.9 | 56.3   |

**`nutrition_summary.csv`** — aggregate stats across all processed products:

| total_products | avg_energy_kcal | avg_fat_g | avg_sugars_g | best_nutriscore_product | worst_nutriscore_product |
|----------------|-----------------|-----------|--------------|-------------------------|--------------------------|
| 3              | 428.58          | 20.84     | 37.94        | Twix                    | Nutella                  |

---

## Error Handling

If a barcode is invalid or the API is unavailable, the pipeline logs the error and continues processing the remaining products. The Gold layer is built from whatever was successfully ingested.

```
23:01:15 [INFO] Processing barcode 3017620429484...
23:01:17 [INFO]   'Nutella' processed successfully.
23:01:17 [ERROR]  Failed to process barcode 9999999999999: Product not found
23:01:17 [INFO] Processing barcode 5000159484695...
23:01:18 [INFO]   'Twix' processed successfully.
23:01:18 [INFO] Building Gold layer from 2 product(s)...
23:01:18 [INFO] Pipeline complete. Results saved to data/gold/
```

---

## Learn More

- [Open Food Facts API](https://world.openfoodfacts.org/data)
- [Medallion Architecture (Databricks)](https://www.databricks.com/glossary/medallion-architecture)
