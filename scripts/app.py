from flask import Flask, render_template, request, redirect, url_for
import random
import requests

app = Flask(__name__)

BASE_URL_API = "https://pokeapi.co/api/v2/"
URL_POKEMON_API_BASE = "%spokemon" % BASE_URL_API
NB_PARTICIPANTS = 64

# Variable globale pour stocker les Pokémon sélectionnés
selected_pokemons = []

# Récupérer un pokémon aléatoire
def get_random_pokemon_id(pokemons_count):
    return random.randint(1, pokemons_count)

# Récupérer les données d'un pokémon
def fetch_pokemon_data(pokemon_id):
    try:
        url_pokemon = f"{URL_POKEMON_API_BASE}/{pokemon_id}"
        response = requests.get(url_pokemon)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print(f"Erreur lors de la récupération du Pokémon avec l'ID : {pokemon_id}")
        return None

# Obtenir une liste de pokémons aléatoires
def get_random_pokemons():
    pokemons = []
    response = requests.get(URL_POKEMON_API_BASE)
    pokemons_count = response.json()["count"]

    while len(pokemons) < NB_PARTICIPANTS:
        pokemon_id = get_random_pokemon_id(pokemons_count)
        pokemon_data = fetch_pokemon_data(pokemon_id)
        if pokemon_data and pokemon_data not in pokemons:
            pokemons.append(pokemon_data)
    return pokemons

# Calculer la force d'un pokémon
def calculate_pokemon_strength(pokemon):
    stats = pokemon['stats']
    total_strength = sum(stat['base_stat'] for stat in stats)
    return total_strength

# Simuler un combat et déterminer le vainqueur
def simulate_battle(pokemon1, pokemon2):
    strength1 = calculate_pokemon_strength(pokemon1)
    strength2 = calculate_pokemon_strength(pokemon2)

    if strength1 > strength2:
        return pokemon1
    elif strength2 > strength1:
        return pokemon2
    else:
        return random.choice([pokemon1, pokemon2])

# Simuler un tournoi et stocker les rounds
def simulate_tournament(pokemons):
    rounds = []
    round_number = 1

    while len(pokemons) > 1:
        round_battles = []
        winners = []

        for i in range(0, len(pokemons), 2):
            pokemon1 = pokemons[i]
            pokemon2 = pokemons[i + 1]
            winner = simulate_battle(pokemon1, pokemon2)
            winners.append(winner)

            # Ajout des détails du combat (Pokémon 1, Pokémon 2, Vainqueur)
            round_battles.append({
                'pokemon1': pokemon1['name'],
                'pokemon1_img': pokemon1['sprites']['front_default'],
                'pokemon2': pokemon2['name'],
                'pokemon2_img': pokemon2['sprites']['front_default'],
                'winner': winner['name']
            })

        rounds.append({
            'round_number': round_number,
            'battles': round_battles
        })

        pokemons = winners
        round_number += 1

    return rounds, pokemons[0]  # Retourne les rounds et le champion

# Route principale : Affichage de la liste des combattants
@app.route('/')
def index():
    global selected_pokemons
    selected_pokemons = get_random_pokemons()  # Obtenir et stocker les Pokémon aléatoires
    return render_template('combatants.html', pokemons=selected_pokemons)

# Route pour afficher un tour spécifique
@app.route('/tournament/<int:round_number>')
def tournament(round_number):
    global selected_pokemons
    rounds, champion = simulate_tournament(selected_pokemons.copy())  # On passe une copie des pokémons

    # Si le numéro du tour est supérieur au nombre de tours, afficher le champion
    if round_number > len(rounds):
        return render_template('champion.html', champion=champion)

    # Navigation : obtenir le tour en cours et les données nécessaires
    current_round = rounds[round_number - 1]  # Les tours commencent à 1
    total_rounds = len(rounds)

    return render_template('tournament.html', round=current_round, round_number=round_number, total_rounds=total_rounds)

if __name__ == '__main__':
    app.run(debug=True)
