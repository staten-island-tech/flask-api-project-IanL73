from flask import Flask, render_template
import requests

app = Flask(__name__)

""" # Route for the home page
@app.route("/")
def index(): """
# We ask the Pokémon API for every Pokemons. Ever. All of them.
response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=151&offset=251")
data = response.json
for result in data['results']:
    print(result['name'])

"---------  _______________________      vroom vroom "
"========  / -------____   ______  \ "
"=======  |   /         | |      \  |        *beep* "
"------- /   |__________| |_______|  \______"
"====== |  ______  ----  |          ______  \ "
"------ | /  ----\       | ------- /      \  |"
"====== ||   []   |______|________|   []   |_|"
"-------- \______//               \\______/"
