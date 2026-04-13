import argparse
import logging

from pipeline import bronze, gold, silver

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def run_pipeline(barcodes: list[str]) -> None:
    successful = []

    for barcode in barcodes:
        log.info("Processing barcode %s...", barcode)
        try:
            raw = bronze.fetch_product(barcode)
            bronze.save_raw(raw, barcode)

            cleaned = silver.clean_product(raw, barcode)
            silver.save_cleaned(cleaned, barcode)
            log.info("  '%s' processed successfully.", cleaned["name"])

            successful.append(barcode)
        except Exception as e:
            log.error("  Failed to process barcode %s: %s", barcode, e)

    if not successful:
        log.error("No products were processed successfully. Aborting Gold layer.")
        return

    log.info("Building Gold layer from %d product(s)...", len(successful))
    try:
        df = gold.load_all_silver()
    except FileNotFoundError as e:
        log.error("Gold layer aborted: %s", e)
        return

    try:
        ranking = gold.build_ranking(df)
        gold.save_ranking(ranking)
        log.info("  products_ranking.csv saved.")
    except Exception as e:
        log.error("  Failed to build ranking: %s", e)

    try:
        summary = gold.build_summary(df)
        gold.save_summary(summary)
        log.info("  nutrition_summary.csv saved.")
    except Exception as e:
        log.error("  Failed to build summary: %s", e)

    log.info("Pipeline complete. Results saved to data/gold/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Open Food Medallion Pipeline — Bronze → Silver → Gold"
    )
    parser.add_argument(
        "barcodes",
        nargs="+",
        metavar="BARCODE",
        help="One or more product barcodes to process (e.g. 3017620429484)",
    )
    args = parser.parse_args()
    run_pipeline(args.barcodes)
