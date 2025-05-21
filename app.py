from flask import Flask, render_template
import requests
import random

app = Flask(__name__)

""" # Route for the home page
@app.route("/")
def index(): """
# We ask the Pokémon API for every Pokemons. Ever. All of them.
response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1&offset=1025")
data = response.json()

everypokemon = {} # We slot them all into a dictionary for later use.
for pokemon in data['results']:
    name = pokemon['name']
    url = (pokemon['url'])
    url = url.split("/")
    pokeid = url[-2]
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokeid}")
    pokemondata = response.json()
    types = [t['type']['name'] for t in pokemondata['types']]
    abilities = [a['ability']['name'] for a in pokemondata['abilities']]
    key = f"pokemon{pokeid}"
    everypokemon[key] = {
        'name': name,
        'id': pokeid,
        'types': types,
        'abilities': abilities
    }
while True:
    question = random.randint(1, 1)
    subject = random.randint(1, 1025)
    if question == 1:
        for pokemon in everypokemon:
            if pokemon['id'] == subject:
                answer = input(f"What is {pokemon['name']}'s primary type? ")
                answer = answer.capitalize()
                if answer == pokemon['types'][0].capitalize():
                    print("Correct!")
                else:
                    print("Incorrect.")
    elif question == 2:
        for pokemon in everypokemon:
            if pokemon['id'] == subject:
                answer = input(f"What is {pokemon['name']}'s first ability? ")
                answer = answer.capitalize()
                if answer == pokemon['abilities'][0].capitalize().replace('-', ' '):
                    print("correct")
                else:
                    print("Incorrect")


"---------  _______________________      vroooooom "
"========  / -------____   ______  \ "
"=======  |   /         | |      \  |        *beep* *beep* "
"------- /   |__________| |_______|  \______"
"====== |  ______  ----  |L         ______  \ "
"------ | /  ----\       | ------- /      \  |"
"====== ||   []   |______|________|   []   |_|"
"-------- \______//               \\______/"