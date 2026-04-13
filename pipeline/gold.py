from pathlib import Path

import pandas as pd

SILVER_DIR = Path("data/silver")
GOLD_DIR = Path("data/gold")

NUTRISCORE_ORDER = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}


def load_all_silver() -> pd.DataFrame:
    files = list(SILVER_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError("No silver data found. Run the pipeline first.")
    return pd.concat([pd.read_csv(f) for f in files], ignore_index=True)


def build_ranking(df: pd.DataFrame) -> pd.DataFrame:
    ranked = df.copy()
    ranked["nutriscore_rank"] = ranked["nutriscore"].map(NUTRISCORE_ORDER)
    ranked = ranked.sort_values(
        ["nutriscore_rank", "energy_kcal"],
        na_position="last",
    )
    ranked.insert(0, "rank", range(1, len(ranked) + 1))
    return ranked.drop(columns=["nutriscore_rank"]).reset_index(drop=True)


def build_summary(df: pd.DataFrame) -> pd.DataFrame:
    scored = df[df["nutriscore"].isin(NUTRISCORE_ORDER)].copy()
    scored["nutriscore_rank"] = scored["nutriscore"].map(NUTRISCORE_ORDER)

    best_product = (
        scored.loc[scored["nutriscore_rank"].idxmin(), "name"]
        if not scored.empty
        else "N/A"
    )
    worst_product = (
        scored.loc[scored["nutriscore_rank"].idxmax(), "name"]
        if not scored.empty
        else "N/A"
    )

    return pd.DataFrame([{
        "total_products": len(df),
        "avg_energy_kcal": round(df["energy_kcal"].mean(), 2),
        "avg_fat_g": round(df["fat"].mean(), 2),
        "avg_sugars_g": round(df["sugars"].mean(), 2),
        "avg_proteins_g": round(df["proteins"].mean(), 2),
        "best_nutriscore_product": best_product,
        "worst_nutriscore_product": worst_product,
    }])


def save_gold(ranking: pd.DataFrame, summary: pd.DataFrame) -> tuple[Path, Path]:
    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    ranking_path = GOLD_DIR / "products_ranking.csv"
    summary_path = GOLD_DIR / "nutrition_summary.csv"
    ranking.to_csv(ranking_path, index=False)
    summary.to_csv(summary_path, index=False)
    return ranking_path, summary_path
