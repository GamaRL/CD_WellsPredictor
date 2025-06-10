import pandas as pd
import os

# Carga modelo desde la carpeta interna ml/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SEISMIC_PATH = os.path.join(BASE_DIR, 'data', 'seismic_activity.parquet')
SPRINGS_PATH = os.path.join(BASE_DIR, 'data', 'springs_with_temp.parquet')

df_seismic = pd.read_parquet(SEISMIC_PATH)
df_springs = pd.read_parquet(SPRINGS_PATH)
