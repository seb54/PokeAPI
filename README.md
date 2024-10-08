# Pokémon Tournament Simulator

Ce projet est une application web Flask qui simule un tournoi entre Pokémon, en récupérant les données via la [PokeAPI](https://pokeapi.co/). Le tournoi sélectionne aléatoirement 16 Pokémon, les fait s'affronter en duels, et détermine un champion.

## Fonctionnalités

- **Combattants aléatoires** : L'application sélectionne aléatoirement 16 Pokémon depuis la PokeAPI.
- **Simulations de combats** : Chaque combat simule la puissance des Pokémon en fonction de leurs statistiques.
- **Tournoi** : Les combats se déroulent par tours successifs jusqu'à ce qu'un champion soit désigné.
- **Affichage par rounds** : L'interface permet de naviguer de round en round pour voir les détails des combats.
  
## Prérequis

- Python 3.x
- `Flask` et `requests` (voir la section **Installation** pour plus de détails)
- Accès à internet pour récupérer les données depuis la PokeAPI

## Installation

1. Clonez le projet depuis ce dépôt :
   ```bash
   git clone https://github.com/votre-repo/pokemon-tournament.git
