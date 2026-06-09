import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Caminho onde se encontra os dados brutos
input_path = Path(__file__).parent.parent/'data'/'raw'/'hospital_patients_real_world.csv'

# Caminho onde os dados processados serão salvos
output_path = Path('data/processed')
output_path.mkdir(parents=True, exist_ok=True)

file_path = output_path / "hospital_records_transformed.csv"

# Listas/Dicionários com as colunas a serem transformadas e tratadas
columns_names_to_datetime = ['AdmissionDate', 'DischargeDate']
columns_names_to_int = ['Age']
columns_names_to_standard = ['Diagnosis']
columns_names_fill_nan = {'Gender': 'Unknown','Diagnosis':'Unknown Diagnosis'}
columns_names_fill_nan_mean = ['Age']

# Cria o DataFrame do pandas
def create_dataframe(path_name: Path):
    logging.info("Criando Data Frame...")

    # Verifica se o arquivo foi encontrado
    if not path_name.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path_name}\n")

    # Ler os dados em csv e converte em DataFrame
    df = pd.read_csv(path_name)

    logging.info(f"Data Frame criado com {len(df)} linha(s)...")

    return df

# Converte as colunas com datas para datetime
def exchange_type_datetime(df: pd.DataFrame, columns_names: list[str])->pd.DataFrame:

    logging.info(f"Convertendo o tipo de dado da(s) coluna(s) {columns_names} para datetime...")

    # Passa por cada coluna especificada e a converte
    for name in columns_names:
        df[name] = pd.to_datetime(df[name], format = "%Y-%m-%d", errors="coerce")

    logging.info("Colunas convertidas para datetime...")

    return df

# Converte as colunas para int
def exchange_type_int(df: pd.DataFrame, columns_names: list[str])->pd.DataFrame:

    logging.info(f"Convertendo tipo de dado da(s) coluna(s) {columns_names} para int...")

    # Passa por cada coluna especificada e a converte
    for name in columns_names:
        df[name] = pd.to_numeric(df[name], errors="coerce").astype("Int64")

    logging.info("Coluna(s) convertida(s) para int...")

    return df
    
# Padroniza os valores das colunas - primeira letra maiúscula e demais minúsculas
def standard_categories(df: pd.DataFrame, columns_names: list[str])->pd.DataFrame:

    logging.info(f"Padronizando categoria(s) da(s) coluna(s) {columns_names}...")

    for name in columns_names:
        df[name] = (df[name]
                    .str.strip() # Remove espaços me branco no inicio e no fim
                    .str.lower() # Todas as letras em minúsculo
                    .str.capitalize() # Primeira letra em maiúsculo
                    )

    logging.info(f"Categoria(s) da(s) coluna(s) {columns_names} padronizada(s)...")

    return df

# Preenche valores nan com base no dicionário
def fill_nan_columns(df: pd.DataFrame, columns_names: dict)->pd.DataFrame:

    logging.info(f"Preenchendo nan das colunas {columns_names.keys()}...")

    # Utiliza o dicionário com coluna:valor para preencher os valores ausentes
    df = df.fillna(columns_names)

    logging.info(f"Valores nan das colunas {list(columns_names.keys())} preenchidos com {list(columns_names.values())} respectivamente...")

    return df

# Preenche valores nan com mediana
def fill_nan_median(df: pd.DataFrame, columns_names: list[str])->pd.DataFrame:

    logging.info(f"Preenchendo valores nan da(s) coluna(s) {columns_names} com a mediana...")

    # Passa por cada coluna, busca a mediana e preenche os valores vazios
    for name in columns_names:
        median = df[name].median()

        logging.info(f"Valores nulos da coluna {name} preenchidos com a mediana de valor {median}")

        df[name] = df[name].fillna(median)

    logging.info(f"Valores nan da(s) coluna(s) {columns_names} preenchidas...")

    return df

# Cria coluna extra especificando se o período de internação (entrada-saída) é válido
def define_valid_stay(df: pd.DataFrame)->pd.DataFrame:

    logging.info("Criando nova coluna booleana para indicar se estadia é válida (DischargeDate >= AdmissionDate)...")

    # Cria a nova coluna booleana que informa período válido ou não
    df['is_valid_stay'] = (df['AdmissionDate'] < df['DischargeDate'])

    logging.info(f"{len(df[~df['is_valid_stay']])} registros com estádia inválida...")

    return df

# Salva os dados tratados 
def save_processed_data(df: pd.DataFrame, output_path)->None:

    logging.info(f"Salvando os dados transformados...")

    df.to_csv(output_path, index=False)

    logging.info(f"Dados salvos em {output_path}...")

# Chama todas as funções de transformação
def transform_data_hospital():

    logging.info("Iniciando as transformações...")

    df = create_dataframe(input_path)
    df = exchange_type_datetime(df, columns_names_to_datetime)
    df = exchange_type_int(df, columns_names_to_int)
    df = standard_categories(df, columns_names_to_standard)
    df = fill_nan_columns(df, columns_names_fill_nan)
    df = fill_nan_median(df, columns_names_fill_nan_mean)
    df = define_valid_stay(df)
    save_processed_data(df, file_path)

    logging.info("Transformações concluídas com sucesso...")

    return df