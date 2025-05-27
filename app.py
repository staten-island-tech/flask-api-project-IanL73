from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

# Fetch Pokémon data once, when the app starts
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
    question_type = random.choice(['type', 'ability'])
    selected_pokemon = random.choice(list(everypokemon.values()))
    
    if question_type == 'type':
        question = f"What is {selected_pokemon['name']}'s primary type?"
        correct_answer = selected_pokemon['types'][0].capitalize()
    else:
        question = f"What is {selected_pokemon['name']}'s first ability?"
        correct_answer = selected_pokemon['abilities'][0].capitalize().replace('-', ' ')

    return render_template("index.html", question=question, pokemon=selected_pokemon, correct_answer=correct_answer)

score = 0
highscore = 0
@app.route("/answer", methods=["POST"])
def answer():
    user_answer = request.form['answer']
    question = request.form['question']
    correct_answer = request.form['correct_answer']
    pokemon_name = request.form['pokemon']

    is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
    feedback = "Correct!" if is_correct else f"Incorrect. The correct answer was: {correct_answer}"
    score.value
    highscore.value
    if is_correct:
        score.value =+ 1
        if score.value > highscore.value:
            highscore = score.value
        print(f'score: {score.value}')
        print(f'high: {highscore.value}')

    # Generate new question
    question_type = random.choice(['type', 'ability'])
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
        score=score,
        highscore=highscore
    )

if __name__ == "__main__":
    app.run(debug=True)