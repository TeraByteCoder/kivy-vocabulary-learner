import nltk
import os

# Festlege des Zielverzeichnisses für die NLTK-Daten
target_folder = os.path.join(os.path.dirname(__file__), "nltk_data")

# Hinzufügen des Zielverzeichnisses zum nltk.data.path
nltk.data.path.append(target_folder)

# Herunterladen der gewünschten Ressource (z.B. Punkt-Tokenizer)
nltk.download('punkt', download_dir=target_folder)

print(nltk.data.path)
