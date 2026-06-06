from src.extract_data import extract_hospital_data
from src.transform_data import transform_data_hospital
from src.load_data import load_hospital_data
from pathlib import Path
import pandas as pd

table_name = 'hospital_records'

extract_hospital_data()

df = transform_data_hospital()

load_hospital_data(table_name, df)

print("Pipeline executado com sucesso!\n\n")