from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_hospital_data(path_name: str, name_file: str):

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

    csv_file = next(output_dir.glob("*.csv"))

    novo_nome = output_dir / name_file

    csv_file.rename(novo_nome)

    logging.info(f"Dados baixados em {output_dir}/{name_file}...")
