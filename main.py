from src.extract_data import extract_hospital_data
from src.transform_data import transform_data_hospital
from src.load_data import load_hospital_data
from pathlib import Path
import pandas as pd

# Nome da tabela que será enviada ao banco de dados
table_name = 'hospital_records'

# Extração
extract_hospital_data()

# Transformação
df = transform_data_hospital()

# Carga
load_hospital_data(table_name, df)

print("Pipeline executado com sucesso!\n\n")