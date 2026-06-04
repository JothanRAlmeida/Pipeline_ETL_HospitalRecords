import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_file = Path(__file__).parent.parent/'data'/'hospital_patients_real_world.csv'

def copy_data():
    logging.info("Criando copia dos dados para transformação...")

    df = pd.read_csv(path_file)

    df.to_csv(
        path_file.parent / "data_hospital_records.csv",
        index = False
    )





# Trocar o tipo do campo Age de float para int
# Trocar o tipo dos campos AdmissionDate e DischargeDate de str para datetime
# Colocar a coluna Diagnosis em caixa baixa para não haver diferença entre categorias iguais
# Incluir os campos nan da coluna Gender na categoria Unknown
# Criar categoria "Sem diagnóstico" para nan da coluna Diagnosis
# Imputar média das idades na coluna Age pois não há outliers
