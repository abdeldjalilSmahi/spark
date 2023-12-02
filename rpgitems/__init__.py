# mon_package/__init__.py

# Importer constants en premier pour assurer son exécution
from . import constants

# Ensuite, importer scraper pour récupérer les données de constants
from . import scraper