import requests

def api_search(ingredient_list, diet_list, allergic_to):
    api_id = "fd76708a"
    api_key = "d1ba194e6492cb68b2289dff094fe26d"
    url = f"https://api.edamam.com/search?&app_id={api_id}&app_key={api_key}&to=100"

    if len(ingredient_list) > 0:
        for ingredient in ingredient_list:
            url = url + f"&q={ingredient}"

    if len(diet_list) > 0:
        for diet in diet_list:
            if diet == "vegan" or diet == "vegetarian":
                url = url + f"&health={diet}"
            else:
                url = url + f"&diet={diet}"

    if len(allergic_to) > 0:
        for allergy in allergic_to:
            url = url + f"&excluded={allergy}"

    response = requests.get(url)
    data = response.json()
    return data['hits']

def main_user():
    usr_name = input("Hello, you are looking for a recipe and I will help you with that."
                     " Below, you will answer some questions that will show you the ideal"
                     " recipe for your purpose! Let's start, what is your name?\n")

    ingredient = input(f"{usr_name}, what ingredients do you want your recipe to contain?"
                       " Type the ingredients separated by commas\n")
    ingredient_list = ingredient.lower().replace(" ", "").split(",")

    diet = input("Do you want your recipe to fit into any of these diets 'Balanced,"
                 " High-Fiber, High-Protein, Low-Carb, Low-Fat, Low-Sodium', Vegan or Vegetarian?"
                 " Type the diets separated by commas or type NO\n")
    diet_list = []

    if diet.lower() != "no":
        diet_list = diet.lower().replace(" ", "").split(",")

    has_allergies = input("Do you have any allergies? Type 'yes' or 'no': ")
    allergic_to = []

    if has_allergies.lower() == "yes":
        allergies = input("What are your allergies? Type each one separated by commas:\n")
        allergic_to = allergies.lower().replace(" ", "").split(",")

    responses = api_search(ingredient_list, diet_list, allergic_to)

    print(f"\n{usr_name}, here are your recipes:\n")
    for response in responses:
        recipe = response['recipe']
        print(recipe['label'])
        print(recipe['url'])
        print()

    file = input("Would you like to save the recipes to a file? Type 'yes' or 'no':\n")

    if file.lower() == "yes":
        file_name = input("What would you like to name the file?\n")
        with open(f"{file_name}.txt", "w") as f:
            for response in responses:
                recipe = response['recipe']
                f.write(f"{recipe['label']}\n{recipe['url']}\n")

        print(f"Your recipes are saved as {file_name}.")
    else:
        print("Recipes not saved.")

main_user()
