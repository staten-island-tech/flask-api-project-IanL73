from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

# Fetch Pokémon data once, when the app starts
def load_pokemon_by_generation(gen_number):
    global everypokemon
    gen = int(gen_number)
    gen_data = {
        1: (0, 151),
        2: (151, 100),
        3: (251, 135),
        4: (386, 107),
        5: (493, 156),
        6: (649, 72),
        7: (721, 88),
        8: (809, 96),
        9: (905, 120)
    }

    offset, limit = gen_data.get(gen, (0, 151))  # Default to Gen 1
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={limit}")
    data = response.json()

    everypokemon.clear()
    for pokemon in data['results']:
        name = pokemon['name']
        url = pokemon['url']
        pokeid = url.split("/")[-2]
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

@app.route("/")
def index():
    # Randomly choose a Pokémon and a trivia question
    question_type = random.choice(['type'])
    selected_pokemon = random.choice(list(everypokemon.values()))
    
    if question_type == 'type':
        question = f"What is {selected_pokemon['name']}'s primary type?"
        correct_answer = selected_pokemon['types'][0].capitalize()
    else:
        question = f"What is {selected_pokemon['name']}'s first ability?"
        correct_answer = selected_pokemon['abilities'][0].capitalize().replace('-', ' ')

    return render_template("index.html", question=question, pokemon=selected_pokemon, correct_answer=correct_answer)

@app.route("/answer", methods=["POST"])
def answer():
    global score
    global highscore
    user_answer = request.form['answer']
    question = request.form['question']
    correct_answer = request.form['correct_answer']
    pokemon_name = request.form['pokemon']

    is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
    feedback = "Correct!" if is_correct else f"Incorrect. The correct answer was: {correct_answer}"

    # Generate new question
    question_type = random.choice(['type'])
    selected_pokemon = random.choice(list(everypokemon.values()))

    if question_type == 'type':
        new_question = f"What is {selected_pokemon['name']}'s primary type?"
        new_correct_answer = selected_pokemon['types'][0].capitalize()
    else:
        new_question = f"What is {selected_pokemon['name']}'s first ability?"
        new_correct_answer = selected_pokemon['abilities'][0].capitalize().replace('-', ' ')

    return render_template(
        "index.html",
        question=new_question,
        correct_answer=new_correct_answer,
        pokemon=selected_pokemon,
        feedback=feedback,
    )

if __name__ == "__main__":
    app.run(debug=True)