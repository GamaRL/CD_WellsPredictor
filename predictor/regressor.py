import joblib
import os

# Carga modelo desde la carpeta interna ml/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'ml', 'model.joblib')

model = joblib.load(MODEL_PATH)
