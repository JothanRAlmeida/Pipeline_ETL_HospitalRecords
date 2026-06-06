from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_hospital_data(path_name: str):

    logging.info("Extraindo os dados do dataset...")

    output_dir = Path(path_name)
    output_dir.mkdir(parents=True, exist_ok=True)

    api = KaggleApi()
    api.authenticate()

    api.dataset_download_files(
        "nudratabbas/hospital-records-for-data-cleaning-medium",
        output_dir,
        unzip=True
    )

    logging.info(f"Dados baixados em {output_dir}...")
