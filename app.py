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

    # We create a list to store details for each Pokémon.
    pokemons = []
    
    for pokemon in pokemon_list:
        # Each Pokémon has a URL like "https://pokeapi.co/api/v2/pokemon/1/"
        pokeurl = pokemon['url']
        parts = pokeurl.strip("/").split("/")
        pid = parts[-1]  # The last part of the URL is the Pokémon's ID

        
        # We use the ID to build an image URL.
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"
        
        pokemons.append({
            'name': pokemon['name'].title(),
            'id': id,
            'image': image_url
        })
    
    # We tell Flask to show the 'index.html' page and pass the list of Pokémon.
    return render_template("index.html", pokemons=pokemons)

# Route for the Pokémon details page
@app.route("/pokemon/<int:id>")
def pokemon_detail(id):
    # We get detailed info for a specific Pokémon using its id.
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
    pokemondata = response.json()
    
    # We extract extra details like types, height, weight, and stats.
    types = [t['type']['name'] for t in pokemondata['types']]
    types = [type.capitalize() for type in types]
    height = pokemondata.get('height')
    height = height/10
    weight = pokemondata.get('weight')
    weight = weight/10
    abilities = [a['ability']['name'] for a in pokemondata['abilities']]
    abilities = [ability.capitalize() for ability in abilities]
    moveset = [m['move']['name'] for m in pokemondata['moves']]
    moveset = [move.replace("-"," ") for move in moveset]
    moveset = [move.title() for move in moveset]
    moveurls = [u['move']['url'] for u in moveset]
    name = pokemondata.get('name').capitalize()
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"
    
    # Get the Pokémon’s base stats (like hp, attack, defense, etc.)
    stat_names = [stat['stat']['name'] for stat in pokemondata['stats']]
    stat_values = [stat['base_stat'] for stat in pokemondata['stats']]
    
    # We tell Flask to show the 'pokemon.html' page with all these details.
    return render_template("pokemon.html", pokemon={
        'abilities': abilities,
        'name': name,
        'id': id,
        'image': image_url,
        'types': types,
        'height': height,
        'weight': weight,
        'ability': abilities,
        'moves': moveset,
        'stat_names': stat_names,
        'stat_values': stat_values
        'moveurls': moveurls })

if __name__ == '__main__':
    app.run(debug=True)