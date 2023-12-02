# class datascraper:
#     def scrap_title(self):
#         # Sélectionner l'élément <h1> parent
#         h1_element = driver.find_element(By.XPATH, '//h1[a[@ui-sref="geekitem.overview"]]')
#
#         # Sélectionner l'élément <a> à l'intérieur de <h1>
#         a_element = h1_element.find_element(By.CSS_SELECTOR, 'a[ui-sref="geekitem.overview"]')
#
#         # Obtenir le texte de l'élément <a>
#         texte_element_a = a_element.text