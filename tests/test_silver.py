from pipeline.silver import clean_product

RAW_FULL = {
    "product": {
        "product_name": "nutella",
        "brands": "Ferrero",
        "categories": "Spreads, Sweet spreads",
        "nutriscore_grade": "e",
        "nutriments": {
            "energy-kcal_100g": 539,
            "fat_100g": 30.9,
            "sugars_100g": 56.3,
            "proteins_100g": 6.3,
        },
    }
}


def test_clean_product_full_data():
    result = clean_product(RAW_FULL, "3017620429484")

    assert result["barcode"] == "3017620429484"
    assert result["name"] == "Nutella"
    assert result["brands"] == "ferrero"
    assert result["energy_kcal"] == 539
    assert result["fat"] == 30.9
    assert result["sugars"] == 56.3
    assert result["proteins"] == 6.3


def test_clean_product_missing_fields():
    result = clean_product({"product": {}}, "0000000000000")

    assert result["name"] == ""
    assert result["brands"] == ""
    assert result["nutriscore"] == ""
    assert result["energy_kcal"] is None
    assert result["fat"] is None
    assert result["sugars"] is None
    assert result["proteins"] is None


def test_clean_product_nutriscore_uppercase():
    raw = {"product": {"nutriscore_grade": "b"}}
    result = clean_product(raw, "1234567890123")

    assert result["nutriscore"] == "B"


def test_clean_product_name_title_case():
    raw = {"product": {"product_name": "  coca-cola original  "}}
    result = clean_product(raw, "5449000000996")

    assert result["name"] == "Coca-Cola Original"
