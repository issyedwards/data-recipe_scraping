"Code to scrape recipes from a website and store their information in a csv"

import sys
import csv
import requests
from bs4 import BeautifulSoup

def parse(html):
    ''' return a list of dict {name, difficulty, prep_time} '''
    soup = BeautifulSoup(html, "html.parser")
    recipe_list = []
    for recipe in soup.find_all(
        "div", class_= "col-12 col-sm-6 col-md-4 col-lg-3"
        ):
        recipe_list.append(parse_recipe(recipe))
    return recipe_list

def parse_recipe(article):
    ''' return a dict {name, difficulty, prep_time} modelising a recipe'''
    name = article.find("p", class_="recipe-name").string
    difficulty = article.find("span", class_="recipe-difficulty").string
    prep_time = article.find(
        "span", class_="recipe-cooktime"
        ).string
    return {"name": name, "difficulty": difficulty, "prep_time": prep_time}

def write_csv(ingredient, recipes, method):
    ''' dump recipes to a CSV file `recipes/INGREDIENT.csv` '''
    with open(f"recipes/{ingredient}.csv", method, encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=recipes[0].keys())
        writer.writeheader()
        for recipe in recipes:
            writer.writerow(recipe)

def scrape_from_internet(ingredient, page=1):
    ''' Use `requests` to get the HTML page of search results for given ingredients. '''
    response = requests.get(
            url = 'https://recipes.lewagon.com/',
            params = {'search[query]': ingredient, 'page': page}
            )
    return response.content

def main():
    """ main function to scrape recipes and output in csv"""
    if len(sys.argv) > 1:
        ingredient = sys.argv[1]
        page = 0
        while page <= 3:
            page += 1
            recipes = parse(scrape_from_internet(ingredient, page))
            if page == 1:
                write_csv(ingredient, "w", recipes)
            else:
                write_csv(ingredient, "a", recipes)
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)


if __name__ == '__main__':
    main()
