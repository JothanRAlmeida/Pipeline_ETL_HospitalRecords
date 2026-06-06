import pandas as pd
import os # Para iteragir diretament com o sistema operacional
from pathlib import Path
from sqlalchemy import create_engine
import logging
from dotenv import load_dotenv # Para carregar as variáveis de ambiente do arquivo .env
from urllib import quote_plus # Codifica strings para que possam ser enviadas com seguranã em uma URL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cria objeto de caminho para o arquivo .env onde estão as variáveis de ambiente
# resolve() converte um caminho relativo em um caminho absoluto e elimina ambiguidade
env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

data_base = os.getenv('database')
user = os.getenv('user')
password = os.getenv('password')
host = 'localhost'

