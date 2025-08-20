import os
from dotenv import load_dotenv
import google.generativeai as genai

# Charger le fichier .env
load_dotenv()

# Utiliser la clé depuis l’environnement
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Affiche tous les modèles disponibles
models = genai.list_models()

for model in models:
    print(model.name)
