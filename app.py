from flask import Flask, render_template, request # imports flask
import requests # Lets requests work
import random # lets me use random number

app = Flask(__name__) # more flask stuff
response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=151") # getting info from api
data = response.json() # converts info from api to json

everypokemon = {} # creates a dictionary to fill with the specific information of every pokemon ever (in gen 1)
for pokemon in data['results']: # repeat for every pokemon we requestion information on
    name = pokemon['name'] # set variable for name
    url = pokemon['url'] # set variable for url (used to gather more specific information)
    pokeid = url.split("/")[-2] # cuts all the slashes our of the url and picks out the last digit, the pokemon's ID
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokeid}") # gather specific information about each pokemon using the id and each pokemon's specific url
    pokemondata = response.json() # sets specific information about each pokemon to a json file
    types = [t['type']['name'] for t in pokemondata['types']] # gather the pokemon's types
    abilities = [a['ability']['name'] for a in pokemondata['abilities']] # gather the pokemon's abilities
    hp = pokemondata['stats'][0] # pokmeon's hp stats
    attack = pokemondata['stats'][1] # its attack stat
    defence = pokemondata['stats'][2] # you know the drill by now
    sattack = pokemondata['stats'][3]
    sdefence = pokemondata['stats'][4]
    speed = pokemondata['stats'][5]
    key = f"pokemon{pokeid}" # these set all the stuff just gathered into
    everypokemon[key] = { # keys and values in a dictionary; the one we set a the start.
        'name': name,
        'id': pokeid,
        'types': types,
        'abilities': abilities,
        'hp': hp,
        'attack': attack,
        'defence': defence,
        'sattack': sattack,
        'sdefence': sdefence,
        'speed': speed
    }

@app.route("/") # establish link
def index(): # 
    # Randomly choose a Pokemon and a trivia question
    question_type = random.choice(['type', 'ability', 'hp', 'attack','defence','sattack','sdefence','speed'])
    selected_pokemon = random.choice(list(everypokemon.values()))
    
    if question_type == 'type':
        question = f"What is {selected_pokemon['name']}'s primary type?"
        correct_answer = selected_pokemon['types'][0].capitalize()
    elif question_type == "hp":
        question = f"What is {selected_pokemon['name']}'base hp stat?"
        correct_answer = selected_pokemon['hp']
    elif question_type == "attack":
        question = f"What is {selected_pokemon['name']}'s base attack stat?"
        correct_answer = selected_pokemon['attack']
    elif question_type == "defence":
        question = f"What is {selected_pokemon['name']}'s base defence stat?"
        correct_answer = selected_pokemon['defence']
    elif question_type == "sattack":
        question = f"What is {selected_pokemon['name']}'s base special attack stat?"
        correct_answer = selected_pokemon['sattack']
    elif question_type == "sdefence":
        question = f"What is {selected_pokemon['name']}'s base special defence stat?"
        correct_answer = selected_pokemon['sdefence']
    elif question_type == "speed":
        question = f"What is {selected_pokemon['name']}'s base speed stat?"
        correct_answer = selected_pokemon['speed']
    else:
        question = f"What is {selected_pokemon['name']}'s first ability?"
        correct_answer = selected_pokemon['abilities'][0].capitalize().replace('-', ' ')

    return render_template("index.html", question=question, pokemon=selected_pokemon, correct_answer=correct_answer)

@app.route("/answer", methods=["POST"])
def answer():
    user_answer = request.form['answer']
    question = request.form['question']
    correct_answer = request.form['correct_answer']
    pokemon_name = request.form['pokemon']

    is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
    are_you_stupid_or_not = "Correct!" if is_correct else f"Incorrect. The correct answer was: {correct_answer}"

    # Generate new question. This could probably have been done more efficiently, but I don't know how.
    question_type = random.choice(['type', 'ability', 'height', 'weight'])
    selected_pokemon = random.choice(list(everypokemon.values()))

    if question_type == 'type':
        new_question = f"What is {selected_pokemon['name']}'s primary type?"
        new_correct_answer = selected_pokemon['types'][0].capitalize()
    elif question_type == "hp":
        new_question = f"What is {selected_pokemon['name']}'base hp stat?"
        new_correct_answer = selected_pokemon['hp']
    elif question_type == "attack":
        new_question = f"What is {selected_pokemon['name']}'s base attack stat?"
        new_correct_answer = selected_pokemon['attack']
    elif question_type == "defence":
        new_question = f"What is {selected_pokemon['name']}'s base defence stat?"
        new_correct_answer = selected_pokemon['defence']
    elif question_type == "sattack":
        new_question = f"What is {selected_pokemon['name']}'s base special attack stat?"
        new_correct_answer = selected_pokemon['sattack']
    elif question_type == "sdefence":
        new_question = f"What is {selected_pokemon['name']}'s base special defence stat?"
        new_correct_answer = selected_pokemon['sdefence']
    elif question_type == "speed":
        new_question = f"What is {selected_pokemon['name']}'s base speed stat?"
        new_correct_answer = selected_pokemon['speed']
    else:
        new_question = f"What is {selected_pokemon['name']}'s first ability?"
        new_correct_answer = selected_pokemon['abilities'][0].capitalize().replace('-', ' ')

    return render_template(
        "index.html",
        question=new_question,
        correct_answer=new_correct_answer,
        pokemon=selected_pokemon,
        are_you_stupid_or_not=are_you_stupid_or_not,
    )

if __name__ == "__main__":
    app.run(debug=True)