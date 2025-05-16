from flask import Flask, render_template
import requests

app = Flask(__name__)

# Route for the home page
@app.route("/")
def index():
    # We ask the Pokémon API for every Pokemons. Ever. All of them.
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1025")
    pokemondata = response.json()
    pokemon_list = pokemondata['results']