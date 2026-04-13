import pandas as pd
import pytest

from pipeline.gold import build_ranking, build_summary

SAMPLE_DF = pd.DataFrame([
    {"barcode": "AAA", "name": "Apple Juice", "nutriscore": "A", "energy_kcal": 45.0, "fat": 0.1, "sugars": 10.0, "proteins": 0.5},
    {"barcode": "BBB", "name": "Chocolate Bar", "nutriscore": "C", "energy_kcal": 480.0, "fat": 25.0, "sugars": 50.0, "proteins": 5.0},
    {"barcode": "CCC", "name": "Nutella", "nutriscore": "E", "energy_kcal": 539.0, "fat": 30.9, "sugars": 56.3, "proteins": 6.3},
])


def test_build_ranking_order():
    ranking = build_ranking(SAMPLE_DF)
    assert list(ranking["name"]) == ["Apple Juice", "Chocolate Bar", "Nutella"]


def test_build_ranking_adds_rank_column():
    ranking = build_ranking(SAMPLE_DF)
    assert "rank" in ranking.columns
    assert ranking["rank"].iloc[0] == 1
    assert ranking["rank"].iloc[-1] == len(SAMPLE_DF)


def test_build_ranking_unknown_nutriscore_goes_last():
    df = pd.DataFrame([
        {"barcode": "AAA", "name": "Known", "nutriscore": "B", "energy_kcal": 100.0, "fat": 5.0, "sugars": 10.0, "proteins": 2.0},
        {"barcode": "BBB", "name": "Unknown", "nutriscore": "", "energy_kcal": 50.0, "fat": 1.0, "sugars": 5.0, "proteins": 1.0},
    ])
    ranking = build_ranking(df)
    assert ranking.iloc[-1]["name"] == "Unknown"


def test_build_summary_total_products():
    summary = build_summary(SAMPLE_DF)
    assert summary["total_products"].iloc[0] == 3


def test_build_summary_averages():
    summary = build_summary(SAMPLE_DF)
    expected_avg_kcal = round((45.0 + 480.0 + 539.0) / 3, 2)
    assert summary["avg_energy_kcal"].iloc[0] == expected_avg_kcal


def test_build_summary_best_and_worst():
    summary = build_summary(SAMPLE_DF)
    assert summary["best_nutriscore_product"].iloc[0] == "Apple Juice"
    assert summary["worst_nutriscore_product"].iloc[0] == "Nutella"


def test_build_summary_no_scored_products():
    df = pd.DataFrame([
        {"barcode": "AAA", "name": "Unknown", "nutriscore": "", "energy_kcal": 100.0, "fat": 5.0, "sugars": 10.0, "proteins": 2.0},
    ])
    summary = build_summary(df)
    assert summary["best_nutriscore_product"].iloc[0] == "N/A"
    assert summary["worst_nutriscore_product"].iloc[0] == "N/A"
