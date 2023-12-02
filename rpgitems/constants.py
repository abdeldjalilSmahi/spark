import json
import os

# BASE_URL = "https://rpggeek.com/browse/rpgitem/page/38"
BASE_URL = "https://rpggeek.com/browse/rpgitem"
BASE_ITEM_URL = "https://rpggeek.com"
# LOGIN_URL = "https://rpggeek.com/login"
LOGIN_URL = "https://rpggeek.com/browse/rpgitem/page/11"
# Obtenir le chemin absolu du fichier courant
current_path = os.path.dirname(os.path.abspath(__file__))

# Combiner le chemin absolu avec le chemin relatif du fichier JSON
json_file_path = os.path.join(current_path, 'login.json')

with open(json_file_path, 'r') as file:
    data = json.load(file)

USERNAME = data["username"]
PASSWORD = data["password"]

# Autres constantes
AUTRE_CONSTANT = "valeur"