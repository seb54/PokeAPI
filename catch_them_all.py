import requests
import random

BASE_URL_API = "https://pokeapi.co/api/v2/"

# URL de l'API Pokémon pour récupérer les données de base des pokémons et des types
URL_POKEMON_API_BASE = "%spokemon" % BASE_URL_API
URL_TYPE_API = "%stype" % BASE_URL_API
NB_PARTICIPANTS = 32


def get_type_advantages():
    """
    Récupère les avantages de type pour les Pokémon à partir de l'API Pokémon.

    :return: Un dictionnaire représentant les avantages des types.
    """
    type_advantages = {}
    try:
        # Récupérer les informations sur les types de l'API
        response = requests.get(URL_TYPE_API)
        response.raise_for_status()
        types_data = response.json()["results"]

        # Itérer sur chaque type et récupérer ses relations de dégâts
        for type_info in types_data:
            type_name = type_info["name"]
            type_url = type_info["url"]

            # Récupérer les détails spécifiques du type
            type_response = requests.get(type_url)
            type_response.raise_for_status()
            type_details = type_response.json()

            # Extraire la liste des types contre lesquels ce type est efficace (double_damage_to)
            strong_against = [relation["name"] for relation in type_details["damage_relations"]["double_damage_to"]]
            type_advantages[type_name] = strong_against

    except requests.RequestException as e:
        print("Erreur lors de la requête pour récupérer les avantages de type :", e)

    return type_advantages


def get_pokemons_count():
    """
    Récupère le nombre total de Pokémon à partir de l'API Pokémon.

    :return: Le nombre total de Pokémon, ou 0 si la requête échoue.
    """
    try:
        response = requests.get(URL_POKEMON_API_BASE)
        response.raise_for_status()
        data = response.json()
        return data["count"]
    except requests.RequestException:
        print("Erreur lors de la requête pour récupération du nombre total de pokémons")
        return 0


def get_random_pokemon_id(pokemons_count):
    """
    Génère un ID de Pokémon aléatoire dans la plage du nombre total de Pokémon disponibles.

    :param pokemons_count: Nombre total de pokémons disponibles
    :return: Un ID de Pokémon sélectionné aléatoirement entre 1 et pokemons_count
    """
    return random.randint(1, pokemons_count)


def fetch_pokemon_data(pokemon_id):
    """
    Récupère les données d'un Pokémon spécifique à partir de son ID.

    :param pokemon_id: L'identifiant unique du Pokémon à récupérer
    :return: Un dictionnaire contenant les données du Pokémon si la requête réussit, None sinon
    """
    try:
        url_pokemon = f"{URL_POKEMON_API_BASE}/{pokemon_id}"
        response = requests.get(url_pokemon)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print(f"Pas de pokémon avec l'ID : {pokemon_id}")
        return None


def get_random_pokemons():
    """
    Récupère une liste de données de Pokémon aléatoires jusqu'à ce que la liste contienne NB_PARTICIPANTS entrées uniques.

    :return: Une liste de dictionnaires contenant les données des Pokémon aléatoires.
    """
    pokemons = []
    pokemons_count = get_pokemons_count()
    while len(pokemons) < NB_PARTICIPANTS:
        pokemon_id = get_random_pokemon_id(pokemons_count)
        pokemon_data = fetch_pokemon_data(pokemon_id)
        if pokemon_data and pokemon_data not in pokemons:
            pokemons.append(pokemon_data)
    return pokemons


def calculate_pokemon_strength(pokemon):
    """
    Calcule la force totale d'un Pokémon comme la somme de ses statistiques de base.

    :param pokemon: Dictionnaire contenant les données du Pokémon, y compris les statistiques de base.
    :return: Un entier représentant la force totale du Pokémon.
    """
    stats = pokemon['stats']
    total_strength = sum(stat['base_stat'] for stat in stats)
    return total_strength


def get_type_advantage_multiplier(pokemon1, pokemon2, type_advantages):
    """
    Calcule le multiplicateur d'avantage de type entre deux Pokémon.

    :param pokemon1: Dictionnaire représentant le premier Pokémon avec une liste de ses types
    :param pokemon2: Dictionnaire représentant le second Pokémon avec une liste de ses types
    :param type_advantages: Dictionnaire contenant les avantages de type
    :return: Un float représentant le multiplicateur d'avantage de type
    """
    # Récupérer les types des deux Pokémon
    types1 = [t['type']['name'] for t in pokemon1['types']]
    types2 = [t['type']['name'] for t in pokemon2['types']]
    multiplier = 1.0

    # Vérifier les avantages de type de pokemon1 contre pokemon2
    for t1 in types1:
        if t1 in type_advantages:
            for t2 in types2:
                if t2 in type_advantages[t1]:
                    multiplier *= 1.5  # Avantage de type
    return multiplier


def simulate_battle(pokemon1, pokemon2, type_advantages):
    """
    Simule un combat entre deux Pokémon et détermine le vainqueur.

    :param pokemon1: Dictionnaire contenant les attributs du premier Pokémon.
    :param pokemon2: Dictionnaire contenant les attributs du second Pokémon.
    :param type_advantages: Dictionnaire contenant les avantages de type.
    :return: Le dictionnaire du Pokémon gagnant.
    """
    # Calculer la force de chaque Pokémon
    strength1 = calculate_pokemon_strength(pokemon1)
    strength2 = calculate_pokemon_strength(pokemon2)

    # Appliquer les avantages de type
    multiplier1 = get_type_advantage_multiplier(pokemon1, pokemon2, type_advantages)
    multiplier2 = get_type_advantage_multiplier(pokemon2, pokemon1, type_advantages)

    adjusted_strength1 = strength1 * multiplier1
    adjusted_strength2 = strength2 * multiplier2

    # Afficher les détails du combat
    print(f"Combat entre {pokemon1['name']} et {pokemon2['name']} :")
    print(f" - {pokemon1['name']} : Force totale = {strength1} (après avantage de type : {adjusted_strength1})")
    print(f" - {pokemon2['name']} : Force totale = {strength2} (après avantage de type : {adjusted_strength2})")

    # Déterminer le vainqueur
    if adjusted_strength1 > adjusted_strength2:
        print(f" --> Vainqueur : {pokemon1['name']}\n")
        return pokemon1
    elif adjusted_strength2 > adjusted_strength1:
        print(f" --> Vainqueur : {pokemon2['name']}\n")
        return pokemon2
    else:
        # En cas d'égalité parfaite, choisir un vainqueur aléatoire
        winner = random.choice([pokemon1, pokemon2])
        print(f" --> Égalité parfaite, vainqueur aléatoire : {winner['name']}\n")
        return winner


def simulate_round(pokemons, type_advantages):
    """
    Simule un tour de combats entre les Pokémon participants.

    :param pokemons: Liste des Pokémon participants au tour de combats.
    :param type_advantages: Dictionnaire contenant les avantages de type.
    :return: Liste des Pokémon gagnants des combats simulés.
    """
    winners = []
    for i in range(0, len(pokemons), 2):
        winner = simulate_battle(pokemons[i], pokemons[i + 1], type_advantages)
        winners.append(winner)
    return winners


def main():
    """
    Fonction principale pour simuler un tournoi Pokémon.

    Cette fonction effectue les étapes suivantes :
    1. Valide le nombre de participants.
    2. Récupère une liste de Pokémon aléatoires et les affiche.
    3. Simule plusieurs tours du tournoi jusqu'à ce qu'il ne reste plus qu'un Pokémon.
    4. Affiche le champion Pokémon.

    :return: None
    """
    # Vérifier que le nombre de participants est une puissance de 2 et au moins égal à 2
    if NB_PARTICIPANTS < 2 or (NB_PARTICIPANTS & (NB_PARTICIPANTS - 1)) != 0:
        print("Le nombre de participants doit être une puissance de 2 et supérieur ou égal à 2.")
        return

    # Récupérer les avantages de type
    type_advantages = get_type_advantages()

    # Récupérer les Pokémon aléatoires
    random_pokemons = get_random_pokemons()
    print("Les 32 Pokémon choisis aléatoirement sont :")
    for i, pokemon in enumerate(random_pokemons, start=1):
        print(f"{i}. {pokemon['name']}")

    # Simuler les tours de combats
    round_number = 1
    current_pokemons = random_pokemons
    while len(current_pokemons) > 1:
        print(f"\n--- Tour {round_number} ---\n")
        current_pokemons = simulate_round(current_pokemons, type_advantages)
        round_number += 1

    # Afficher le champion
    print("\nLe champion est :")
    print(f"{current_pokemons[0]['name']}")


if __name__ == "__main__":
    main()