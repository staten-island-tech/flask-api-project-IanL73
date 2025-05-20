from flask import Flask, render_template
import requests
import random

app = Flask(__name__)

""" # Route for the home page
@app.route("/")
def index(): """
# We ask the Pokémon API for every Pokemons. Ever. All of them.
response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1025")
data = response.json()

everypokemon = {} # We slot them all into a dictionary for later use.
for pokemon in data['results']:
    name = pokemon['name']
    url = (pokemon['url'])
    url = url.split("/")
    pokeid = url[-2]
    key = f"pokemon{pokeid}"
    everypokemon[key] = {
        'name': name,
        'id': pokeid
    }
print(everypokemon)


"---------  _______________________      vroooooom "
"========  / -------____   ______  \ "
"=======  |   /         | |      \  |        *beep* *beep* "
"------- /   |__________| |_______|  \______"
"====== |  ______  ----  |L         ______  \ "
"------ | /  ----\       | ------- /      \  |"
"====== ||   []   |______|________|   []   |_|"
"-------- \______//               \\______/"