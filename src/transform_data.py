import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_file_raw = Path(__file__).parent.parent/'data'/'hospital_patients_real_world.csv'

columns_names_to_datetime = ['AdmissionDate', 'DischargeDate']
columns_names_to_int = ['Age']
columns_names_to_standard = ['Diagnosis']
columns_names_fill_nan = {'Gender': 'Unknown','Diagnosis':'No Diagnosis'}
columns_names_fill_nan_mean = ['Age']

def create_dataframe(path_name: Path):
    logging.info("Criando copia dos dados para transformação...")

    if not path_name.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path_name}\n")

    df = pd.read_csv(path_name)

    logging.info(f"Data Frame criado com {len(df)} linha(s)...")

    return df

def exchange_type_datetime(df: pd.DataFrame, columns_names: list[str])->pd.DataFrame:

    logging.info(f"Convertendo o tipo de dado da(s) coluna(s) {columns_names} para datetime...")

    for name in columns_names:
        df[name] = pd.to_datetime(df[name], format = "%Y-%m-%d", errors="coerce")

    logging.info("Colunas convertidas para datetime...")

    return df

def exchange_type_int(df: pd.DataFrame, columns_names: list[str])->pd.DataFrame:

    logging.info(f"Convertendo tipo de dado da(s) coluna(s) {columns_names} para int...")

    for name in columns_names:
        df[name] = df[name].astype(int)

    logging.info("Coluna(s) convertida(s) para int...")

    return df
    
def standard_categories(df: pd.DataFrame, columns_names: list[str])->pd.DataFrame:

    logging.info(f"Padronizando categorias da(s) coluna(s) {columns_names}...")

    for name in columns_names:
        df[name] = df[name].strip().lower() # Remove espaços no inicio e fim e tudo em letra minúscula
        df[name] = df[name].capitalize() # Primeira letra maiúscula

    logging.info(f"Categorias da(s) coluna(s) {columns_names} padronizada(s)...")

    return df

def fill_nan_columns(df: pd.DataFrame, columns_names: dir)->pd.DataFrame:

    logging.info(f"Preenchendo nans das colunas {columns_names.keys()}...")

    # Utiliza o dicionário com coluna:valor para preencher os valores ausentes
    df = df.fillna(columns_names, inplace=True)

    logging.info(f"Valores nans das {columns_names.keys()} preenchidos...")

    return df

def fill_nan_mean(df: pd.DataFrame, columns_names: list[str])->pd.DataFrame:

    logging.info(f"Preenchendo valores nans da(s) coluna(s) {columns_names} com a média...")

    for name in columns_names:
        mean = df[name].mean()
        df[name] = df[name].fillna(mean, inplace=True)

    logging.info(f"Valores nans da(s) coluna(s) {columns_names} preenchidas...")

    return df
