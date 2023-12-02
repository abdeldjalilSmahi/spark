# import json
#
# with open("rpg_items.json") as f:
#     data = json.load(f)
#
# print(len(data))

#####################
from selenium import webdriver
from selenium.common import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import rpgitems.constants as const
from bs4 import BeautifulSoup
from rpgitems.rpgItem import RpgItem
from rpgitems.persistor import Persistor
from selenium.common.exceptions import TimeoutException


driver = webdriver.Chrome()

driver.get("https://rpggeek.com/rpgitem/48050/eyes-only")
year = ""
try:
    # Trouver l'élément <h1> avec la classe spécifiée
    h1_element = driver.find_element(By.XPATH, '//h1[a[@ui-sref="geekitem.overview"]]')

    # Obtenir le code HTML de l'élément <h1>
    html_content = h1_element.get_attribute("outerHTML")

    # Utiliser BeautifulSoup pour traiter le code HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Trouver la balise <span> avec la classe spécifiée à l'intérieur de <h1>
    year_span = soup.find('span', {'class': 'game-year'})

    # Extraire le texte de la balise <span>
    year = year_span.text.strip() if year_span else ""
    year = year.split('(')[1].replace(')','')

except NoSuchElementException:
    print("L'élément n'a pas été trouvé.")
except Exception as e:
    print("Une erreur s'est produite :", str(e))
    year = ""

print(year)