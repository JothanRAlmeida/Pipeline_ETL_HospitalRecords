from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Utiliza a API do Kaggle para extrair arquivo com os dados
def extract_hospital_data():

    logging.info("Extraindo os dados do dataset...")

    output_dir = Path('data/raw') # Diretório onde irá salvar o dataset (.csv)
    output_dir.mkdir(parents=True, exist_ok=True) # Se o caminho não existir, cria as pastas

    api = KaggleApi() # Instância da classe KaggleApi
    api.authenticate() # Carrega as credenciais e autentica o usuário

    # Baixa o(s) arquivo(s) do local especificado e salva no diretório informado
    api.dataset_download_files(
        "nudratabbas/hospital-records-for-data-cleaning-medium",
        output_dir,
        unzip=True # Se estiver zipado descompacta automaticamente
    )

    logging.info(f"Dados baixados em {output_dir}...")
