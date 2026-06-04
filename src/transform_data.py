import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_file_raw = Path(__file__).parent.parent/'data'/'hospital_patients_real_world.csv'

columns_names_to_datetime = ['AdmissionDate', 'DischargeDate']
columns_names_to_int = ['Age']
columns_names_to_standard = ['Diagnosis']

def create_dataframe(path_name: str):
    logging.info("Criando copia dos dados para transformação...")

    if not path_name.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path_name}\n")

    df = pd.read_csv(path_name)

    logging.info(f"Data Frame criado com {len(df)} linha(s)...")

    return df

def exchange_type_datetime(df: pd.DataFrame, columns_names: list[str])->pd.DataFrame:

    logging.info(f"Convertendo o tipo de dado da(s) coluna(s) {columns_names} para datetime...")

    for name in columns_names:
        #df[name] = pd.to_datetime(df[name], format = "%m/%d/%y")
        df[name] = pd.to_datetime(df[name], infer_datetime_format=True)

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
        
        




# Trocar o tipo do campo Age de float para int
# Trocar o tipo dos campos AdmissionDate e DischargeDate de str para datetime
# Colocar a coluna Diagnosis em caixa baixa para não haver diferença entre categorias iguais
# Incluir os campos nan da coluna Gender na categoria Unknown
# Criar categoria "Sem diagnóstico" para nan da coluna Diagnosis
# Imputar média das idades na coluna Age pois não há outliers
