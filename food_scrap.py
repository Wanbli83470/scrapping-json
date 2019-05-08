import requests as r
from bs4 import BeautifulSoup as b
import unicodedata
import json


class Scrapping_json :
    def __init__(self, product):
        self.product = product

    def get_product_url(self, link_product=""):
        self.link_product = link_product
        requête = r.get("https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}&search_simple=1&action=process".format(self.product))
        html = requête.content
        soup = b(html, 'html.parser')
        list_products = soup.select(".products")[0]
        product_one = list_products.li

        # On récupère une url
        nb = 0

        for link in list_products.find_all('a'):
            while nb < 1:
                self.link_product = link.get('href')
                # print(link_product)
                nb += 1

        return self.link_product


    def get_categorie_url(self, link_cat = ""):
        self.link_cat = link_cat

        print("on rentre dans get_categorie_url")

        link_product_complete = "https://fr.openfoodfacts.org{}".format(self.link_product)
        print(link_product_complete)
        cat_requête = r.get(link_product_complete)
        cat_html = cat_requête.content
        cat_soup = b(cat_html, 'html.parser')
        self.link_cat = cat_soup.select(".tag.well_known")[2]
        self.link_cat = self.link_cat.text

        print("lien catégorie : {}".format(self.link_cat))
        return self.link_cat


    def get_json_categorie(self, link_cat = ""):
        self.link_cat = link_cat
        print("\nOn rentre dans get_json_categorie \n")
        # Traitement de link_cat en vue de l'url

        # Suppresion des caracètre accentués
        self.link_cat = self.link_cat.lower()
        # remplacement des espaces par un tiret
        self.link_cat = self.link_cat.replace(" ", "-")

        # Suppresion des accents
        self.link_cat = unicodedata.normalize('NFKD', self.link_cat).encode('ascii', 'ignore')
        self.link_cat = self.link_cat.decode('utf-8')

        url_cat_json = "https://fr-en.openfoodfacts.org/category/{}.json".format(self.link_cat)

        return url_cat_json

def get_category(choice_product) :
    # On choisit un produit
    product = choice_product
    # On paramètre la requête avec le produit pour obtenir le html correspondant
    requête = r.get("https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}&search_simple=1&action=process".format(product))

    # On récupère le contenu du code html
    html = requête.content

    # On récupère proprement le contenu
    soup = b(html, 'html.parser')

    # On récupère la liste des produits
    list_products = soup.select(".products")[0]
    product_one = list_products.li

    # On récupère une url
    nb = 0

    link_product = str
    for link in list_products.find_all('a'):
        while nb < 1:
            link_product = link.get('href')
            # print(link_product)
            nb += 1


    link_product_complete = "https://fr.openfoodfacts.org{}".format(link_product)
    print(link_product_complete)

    """Etape 2 : Récupérer le liens de la catégorie."""

    cat_requête = r.get(link_product_complete)
    cat_html = cat_requête.content
    cat_soup = b(cat_html, 'html.parser')

    link_cat = cat_soup.select(".tag.well_known")[2]
    link_cat = link_cat.text
    # print("lien catégorie : {}".format(link_cat))

    """Etape 3 : parcourir le json de la catégorie"""

    # Traitement de link_cat en vue de l'url

    # Suppresion des caracètre accentués
    link_cat = link_cat.lower()

    # remplacement des espaces par un tiret
    link_cat = link_cat.replace(" ", "-")

    # Suppresion des accents
    link_cat = unicodedata.normalize('NFKD', link_cat).encode('ascii', 'ignore')
    link_cat = link_cat.decode('utf-8')
    # print(link_cat)
    url_cat_json = "https://fr-en.openfoodfacts.org/category/{}.json".format(link_cat)
    # print(url_cat_json)
    return url_cat_json




# # On initialise l'instance de classe
# Nutella = Scrapping_json("Nutella")
#
# Nutella.get_product_url()
#
# MA_CATÉGORIE = Nutella.get_categorie_url()
#
# JSON = Nutella.get_json_categorie(link_cat=MA_CATÉGORIE)
# print(JSON)

categories = r.get('https://fr.openfoodfacts.org/api/v0/produit/3564700007341.json')
print(categories)

convert = categories.json()
print(convert['product']['categories_tags'])