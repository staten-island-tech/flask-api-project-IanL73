from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)
response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=151")
data = response.json()

everypokemon = {}
for pokemon in data['results']:
    name = pokemon['name']
    url = pokemon['url']
    pokeid = url.split("/")[-2]
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokeid}")
    pokemondata = response.json()
    types = [t['type']['name'] for t in pokemondata['types']]



    abilities = [a['ability']['name'] for a in pokemondata['abilities']]





    hp = pokemondata['stats'][0]['base_stat']
    attack = pokemondata['stats'][1]['base_stat']
    defence = pokemondata['stats'][2]['base_stat']
    sattack = pokemondata['stats'][3]['base_stat']
    sdefence = pokemondata['stats'][4]['base_stat']
    speed = pokemondata['stats'][5]['base_stat']
    key = f"pokemon{pokeid}"
    everypokemon[key] = {
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

@app.route("/")
def index():
    question_type = random.choice(['type', 'ability', 'hp', 'attack', 'defence', 'sattack', 'sdefence', 'speed'])
    selected_pokemon = random.choice(list(everypokemon.values()))

    if question_type == 'type':
        question = f"What is {selected_pokemon['name']}'s primary type?"
        correct_answer = selected_pokemon['types'][0].capitalize()
    elif question_type == "hp":
        question = f"What is {selected_pokemon['name']}'s base hp stat?"
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
    feedback = "Correct!" if is_correct else f"Incorrect. The correct answer was: {correct_answer}"

    question_type = random.choice(['type', 'ability', 'hp', 'attack', 'defence', 'satack', 'sdefence', 'speed'])
    selected_pokemon = random.choice(list(everypokemon.values()))

    if question_type == 'type':
        new_question = f"What is {selected_pokemon['name']}'s primary type?"
        new_correct_answer = selected_pokemon['types'][0].capitalize()
    elif question_type == "hp":
        new_question = f"What is {selected_pokemon['name']}'s base hp stat?"
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
        feedback=feedback
    )

if __name__ == "__main__":
    app.run(debug=True)
