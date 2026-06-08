import pandas as pd
import os # Para iteragir diretament com o sistema operacional
from pathlib import Path
from sqlalchemy import create_engine, text
import logging
from dotenv import load_dotenv # Para carregar as variáveis de ambiente do arquivo .env
from urllib.parse import quote_plus # Codifica strings para que possam ser enviadas com seguranã em uma URL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cria objeto de caminho para o arquivo .env onde estão as variáveis de ambiente
# resolve() converte um caminho relativo em um caminho absoluto e elimina ambiguidade
env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

# Vincula dados da pasta .env 
database = os.getenv('database')
user = os.getenv('user')
password = os.getenv('password')
host = 'localhost'

# Conexão com o banco de dados PostgreSQL
def get_engine():

    logging.info(f"Conectando em {host}:5432/{database}...")

    # Define onde está o banco e conecta ao mesmo
    return create_engine(f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}")

# Chama a conexão com o banco
engine = get_engine()

# Carrega os dados tratados no banco de dados no PostgreSQL
def load_hospital_data(table_name: str, df: pd.DataFrame):

    logging.info(f"Carregando dados na tabela {table_name} do banco de dados...")

    # Para salvar o DataFrame do pandas diretamente no banco de dados
    df.to_sql(
        name = table_name, # Define o nome da tabela
        con = engine, # Conecta ao banco
        if_exists='replace', # Se a tabela já existir substitui todos os dados
        index=False # Controla se o índice do DataFrame será salvo no banco ou é ignorado
    )

    logging.info("Dados carregados com sucesso...")

    # Para checar se os dados foram carregados no banco
    df_check = pd.read_sql(f"SELECT * FROM {table_name}", con = engine)

    logging.info(f"Total de registros na tabela {table_name}: {len(df_check)}")