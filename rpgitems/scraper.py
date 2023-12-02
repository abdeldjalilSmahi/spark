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


class RpgItems(webdriver.Chrome):
    def __init__(self,
                 teardown=False):
        self.persistor = Persistor()
        self.teardown = teardown
        super(RpgItems, self).__init__()
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def check_and_click_element(self, element_id):
        try:
            # Essayer de trouver l'élément avec l'ID spécifié
            element = self.find_element(By.ID, element_id)

            # Si l'élément est trouvé, cliquer dessus
            element.click()
            return True  # Indiquer que le clic a réussi
        except:
            # Si l'élément n'est pas trouvé, ne rien faire
            return False

    def login(self):
        print(self.current_url)
        self.wait_for_redirection()
        username = const.USERNAME
        password = const.PASSWORD
        self.get_authenticated(username, password)

    def refresh_page(self):
        self.refresh()

    def get_first_page(self):
        self.get(const.BASE_URL)
        self.check_and_click_element("c-p-bn")
        self.wait_for_redirection()
        # Imprimer la nouvelle URL
        print("Redirected URL:", self.current_url)
        if "login" in self.current_url:
            self.login()
            print("retour de login")
        self.implicitly_wait(5)
        self.wait_for_redirection()

    def get_rpg_items_in_the_page(self):
        # Ajouter un essai pour recharger la page en cas d'erreur StaleElementReferenceException
        try:
            elements = self.find_elements(By.CSS_SELECTOR, 'a.primary')
            liens = [element.get_attribute('href') for element in elements]
            return liens
        except StaleElementReferenceException:
            # Si l'erreur se produit, recharger la page et réessayer
            print("StaleElementReferenceException détectée. Rechargement de la page.")
            self.refresh_page()
            elements = self.find_elements(By.CSS_SELECTOR, 'a.primary')
            liens = [element.get_attribute('href') for element in elements]
            return liens

    def get_rpg_item_data(self, links):
        current = self.current_url
        next_page_url = self.get_next_page_url()
        for link in links:
            self.get(link)
            item = self.scrap_data(link)
            self.persistor.add_rpg_item(item)
            # self.back()
            self.implicitly_wait(5)
            self.wait_for_redirection()
        # self.wait_for_redirection()
        # self.get(current)
        self.wait_for_redirection()
        # next_page_url = self.get_next_page_url()
        if next_page_url is not None:
            self.go_to_next_page(next_page_url)
        else:
            print("nous sommes dans la dernière page")

    def get_next_page_url(self):
        try:
            # Recherche de l'élément <a> avec l'attribut title="next page"
            next_page_element = self.find_element(By.CSS_SELECTOR, 'a[title="next page"]')

            # Récupération de l'URL de la page suivante
            next_page_url = next_page_element.get_attribute('href')
            print("Next page URL:", next_page_url)
            return next_page_url
        except NoSuchElementException:
            # L'élément n'est pas trouvé, cela signifie que nous sommes sur la dernière page
            print("Reached the last page.")
            return None

    def go_to_next_page(self, link):
        self.wait_for_redirection()
        self.redirection_and_wait(link)
        # Imprimer la nouvelle URL
        print("Redirected URL:", self.current_url)
        if "login" in self.current_url:
            self.login()
            print("retour de login")
        self.wait_for_redirection()
        print(self.current_url)
        self.rebolote()

    def wait_for_redirection(self, max_attempts=4):
        attempts = 0
        while "login" in self.current_url and attempts < max_attempts:
            self.implicitly_wait(1)
            attempts += 1

    def get_authenticated(self, username, password):

        # self.wait_for_redirection()
        # # Imprimer la nouvelle URL
        # print("Redirected URL:", self.current_url)

        username_field = self.find_element(By.ID, "inputUsername")
        password_field = self.find_element(By.ID, "inputPassword")
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button = self.find_element(By.CLASS_NAME, 'btn.btn-lg.btn-primary')
        login_button.click()

        self.wait_for_redirection()
        # Imprimer la nouvelle URL
        print("Redirected URL:", self.current_url)

    def redirection_and_wait(self, link):
        self.implicitly_wait(5)
        self.get(link)
        self.wait_for_redirection()

    def rebolote(self):
        self.wait_for_redirection()
        self.implicitly_wait(5)
        links = self.get_rpg_items_in_the_page()
        self.get_rpg_item_data(links)

    def scrap_data(self, link):
        url = link
        titre = self.scrap_title()
        year = self.scrap_year()
        rank = self.scrap_rank()
        rating = self.scrap_rating()
        description = self.scrap_description()
        genres = self.scrap_genres()
        categories = self.scrap_categories()
        item = RpgItem(url, titre, rank, rating, year, description, genres, categories)
        return item

    from selenium.common.exceptions import NoSuchElementException

    def scrap_title(self) -> str:
        try:
            # Sélectionner l'élément <h1> parent
            h1_element = self.find_element(By.XPATH, '//h1[a[@ui-sref="geekitem.overview"]]')

            # Sélectionner l'élément <a> à l'intérieur de <h1>
            a_element = h1_element.find_element(By.CSS_SELECTOR, 'a[ui-sref="geekitem.overview"]')

            # Obtenir le texte de l'élément <a>
            return a_element.text
        except NoSuchElementException:
            # Retourner une chaîne vide si l'élément n'est pas trouvé
            return ""

    def scrap_year(self):
        year = ""
        try:
            # Trouver l'élément <h1> avec la classe spécifiée
            h1_element = self.find_element(By.XPATH, '//h1[a[@ui-sref="geekitem.overview"]]')

            # Obtenir le code HTML de l'élément <h1>
            html_content = h1_element.get_attribute("outerHTML")

            # Utiliser BeautifulSoup pour traiter le code HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # Trouver la balise <span> avec la classe spécifiée à l'intérieur de <h1>
            year_span = soup.find('span', {'class': 'game-year'})

            # Extraire le texte de la balise <span>
            year = year_span.text.strip() if year_span else ""
            year = year.split('(')[1].replace(')', '')

        except NoSuchElementException:
            print("L'élément n'a pas été trouvé.")
        except Exception as e:
            print("Une erreur s'est produite :", str(e))
            year = ""
        return year

    def scrap_rank(self):
        try:
            li_element = self.find_element(By.CLASS_NAME, 'rank')

            # Sélectionner l'élément <a> à l'intérieur de <li>
            a_element = li_element.find_element(By.CLASS_NAME, 'rank-value.ng-binding.ng-scope')

            # Obtenir le texte de l'élément <a>
            rank_text = a_element.text
            return rank_text
        except NoSuchElementException:
            # Si l'élément n'est pas trouvé, afficher "--"
            return "--"

    def scrap_rating(self):
        try:
            # Essayer de trouver l'élément avec ng-show="showRating"
            element = self.find_element(By.CSS_SELECTOR, 'span[ng-show="showRating"].ng-binding')
            element = element.text
            if element == "":
                element = 0.0

        except NoSuchElementException:
            # Si l'élément n'est pas trouvé, essayer de trouver l'élément avec ng-show="!showRating"
            element = self.find_element(By.CSS_SELECTOR, 'span[ng-show="!showRating"]').text

        return element

    def scrap_description(self):

        description = ""
        try:
            # Trouver l'élément <div> avec ng-bind-html="geekitemctrl.wikitext|to_trusted"
            div_element = self.find_element(By.CSS_SELECTOR, 'div[ng-bind-html="geekitemctrl.wikitext|to_trusted"]')

            # Obtenir le code HTML de l'élément
            html_content = div_element.get_attribute("outerHTML")

            # Utiliser BeautifulSoup pour traiter le code HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # Trouver toutes les balises <p>
            paragraphs = soup.find_all('p')

            # Extraire le texte de chaque paragraphe en excluant les balises <em>, <strong> et <a>
            description = ' '.join(
                [''.join(
                    [str(child) if child.name not in ['em', 'strong', 'a', 'br', 'span', 'i', 'u'] else child.text for \
                     child in p.contents]) for
                    p in paragraphs])
        except NoSuchElementException:
            print("L'élément n'a pas été trouvé.")
        except Exception as e:
            print("Une erreur s'est produite :", str(e))
            description = ""

        return description

    def scrap_genres(self):
        # Attendre que la page se charge (vous pouvez ajuster le temps d'attente si nécessaire)
        self.implicitly_wait(10)

        # Initialisez une liste pour stocker les genres
        genres = []

        # Trouver tous les éléments <li> avec la classe spécifiée
        li_elements = self.find_elements(By.CSS_SELECTOR, 'li.feature.ng-scope')

        # Parcourir tous les éléments <li> pour trouver le genre
        for li_element in li_elements:
            # Trouver la balise <div> avec la classe "feature-title ng-binding"
            title_element = li_element.find_element(By.CSS_SELECTOR, 'div.feature-title.ng-binding')

            # Vérifier si le texte de la balise <div> est "Genre"
            if title_element.text.strip() == 'Genre':
                # Trouver toutes les balises <a> à l'intérieur de cette balise <li>
                a_elements = li_element.find_elements(By.CSS_SELECTOR, 'a.ng-binding')

                # Parcourir chaque balise <a> pour extraire le texte et l'ajouter à la liste des genres
                for a_element in a_elements:
                    genre_text = a_element.text.strip()
                    if genre_text != '':
                        genres.append(genre_text)

        return genres

    def scrap_categories(self):
        # Attendre que la page se charge (vous pouvez ajuster le temps d'attente si nécessaire)
        self.implicitly_wait(10)

        # Initialisez une liste pour stocker les catégories
        categories = []

        # Trouver tous les éléments <li> avec la classe spécifiée
        li_elements = self.find_elements(By.CSS_SELECTOR, 'li.feature.ng-scope')

        # Parcourir tous les éléments <li> pour trouver la catégorie
        for li_element in li_elements:
            # Trouver la balise <div> avec la classe "feature-title ng-binding"
            title_element = li_element.find_element(By.CSS_SELECTOR, 'div.feature-title.ng-binding')

            # Vérifier si le texte de la balise <div> est "Category"
            if title_element.text.strip() == 'Category':
                # Trouver toutes les balises <a> à l'intérieur de cette balise <li>
                a_elements = li_element.find_elements(By.CSS_SELECTOR, 'a.ng-binding')

                # Parcourir chaque balise <a> pour extraire le texte et l'ajouter à la liste des catégories
                for a_element in a_elements:
                    category_text = a_element.text.strip()
                    if category_text != '':
                        categories.append(category_text)

        return categories
