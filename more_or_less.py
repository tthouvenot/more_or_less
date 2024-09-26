#################################
###                           ###
###     Jeu Plus ou Moins     ###
###                           ###
### Author: Tristan Thouvenot ###
### Version: 1.0              ###
### Date: 26/09/2024          ###
#################################

# //L'objectif est de créer le jeu du juste prix. 
# //On télécharge les données du fichier JSON
# //L'utilisateur va fournir son nom
#   //Si il est présent dans le fichier data:
#     //  - on récupère ses données
#   //Sinon:
#     //  - on le créera dans le fichier une fois le jeu fini
# //On offre la possibilité à l'utilisateur de choisir entre:
#   //- afficher ses résultats précédents:
#     //  - son total de points (ne peut pas être négatif)
#       //- son record de rapidité
#       //- son nombre de victoire d'affilé (si en cours)
#       //- son nombre de défaite d'affilé (si en cours)
#   //- jouer
#     //  - on lance le jeu
#   //- quitter
#//
# //Game Rules:
#   //- l'utilisateur à 15 essaies
#   //- chaque essaie lui fait perdre 3 points
#   //- une victoire lui donne 100 points
#//
# //Game Loop:
# // - on sélectionne un int random entre 0 et 10000
# //- On demande à l'utilisateur
# //- si sa réponse est:
#   //- plus basse on lui dit c'est plus et on lui redemande
#   //- plus haute on lui dit c'est moins et on lui redemande
#   //- pas un chiffre entre 0 et 10000:
#      // - on le prévient et il perd ni un essaie ni des points
# //- La partie finie s'il a trouvé le bon chiffre ou plus aucun essaie
#// - On lui demande s'il veut rejouer
#//   - oui on relance le jeu
#   //- non :
#       //- on enregistre les datas dans le fichier JSON 
#       //- on fait un résumé de ses stats. 
#       //- On lui demande d'appuyer sur un bouton pour quitter le programme

import random
import time
import json
import re

#################
### functions ###
#################

def json_access(task, datas = None):
    """
    Access the JSON file for reading, writing, or updating user data.

    Args:
        task (str): The action to perform ('read', 'write', or 'update').
        datas (dict, optional): The data to write or update in the JSON file.

    Returns:
        dict: The data read from the JSON file if the task is 'read'.
    """

    file_path = './user_data.json'

    if task == "read":
        with open(file_path, 'r') as file:
            datas_from_files = json.load(file) 
        return datas_from_files
    
    if task == "write":
        with open(file_path, 'w') as file:
            json.dump(datas, file, indent=4)

    if task == "update":
        current_data = json_access("read")
        user_found = False
        
        for user in current_data["users"]:
            if user["user_name"] == datas["user_name"]:
                user.update(datas)
                user_found = True
                break
        
        if not user_found:
            current_data["users"].append(datas)

        json_access("write", datas=current_data)
        # return current_data
    

def validate_pseudo(pseudo):
    """
    Validate the user pseudo against the defined regex pattern.

    Args:
        pseudo (str): The user pseudo to validate.

    Returns:
        bool: True if the pseudo is valid, False otherwise.
    """
     
    return re.match(pseudo_regex, pseudo) is not None

def game_loop(rand):
    """
    Execute the game loop where the user tries to guess a random number.

    Args:
        rand (int): The random number to guess.

    Returns:
        dict: A dictionary containing the number of tries and current points.
    """

    tries = 0
    end_of_game = False
    current_point = 0

    while tries < 15 and not end_of_game:
        try:
            user_answer = int(input("Quel est votre chiffre? "))

            if user_answer < rand and user_answer >= 0:
                print("C'est plus!")
                tries += 1
                current_point -= 3
            elif user_answer > rand and user_answer <= 10000:
                print("C'est moins!")
                tries += 1
                current_point -= 3
            elif user_answer == rand:
                print(f"Bravo! La bonne réponse était bien {rand}!")
                current_point += 100
                end_of_game = True
            else:
                print("Attention, le chiffre à deviner est entre 0 et 10.000")

        except:
            print("Veuillez entrer un chiffre entre 0 et 10000")

    game_score = {
        "tries": tries,
        "current_points": current_point
    }

    return game_score

def exit_program():
    """
    Handle the exit process of the game by prompting the user to quit.
    """

    quit_game = False

    while not quit_game:
        button_press = input("Merci de votre participation. Veuillez appuyer sur la touche \"q\" pour quitter le jeu!: ").lower()

        if button_press != "q":
            print("Erreur: saisie incorrect!")
        else:
            quit_game = True

def display_score(datas):
    """
    Display the user's game statistics.

    Args:
        datas (dict): The user data containing statistics to display.
    """

    streak = datas["win_streak"] - datas["lose_streak"]

    print("#################################")
    print("### Tableau des statistiques: ###")
    print("#################################")
    print()

    print(f"Pseudo: {datas["user_name"]}")
    print(f"Points Total: {datas["total_points"]}")
    print(f"Meilleur score: {datas["best_score"]}")
    print(f"Meilleure tentative: {datas["best_tries"]}")
    print(f"Nombre de victoire: {datas["total_win"]}")
    print(f"Nombre de défaite: {datas["total_lose"]}")
    print(f"Série actuelle: {datas['win_streak']} victoires" if streak > 0 else f"Série actuelle: {datas['lose_streak']} défaites")
    print()

    print("#################################")
    time.sleep(2)


def game_instance(user):
    """
    Manage the game instance and handle user interactions during the game.

    Args:
        user (dict): The user data containing their statistics and game information.
    """

    still_playing = True

    while still_playing:
        print("###############################")
        print("###                         ###")
        print("### Bienvenue au juste prix ###")
        print("###                         ###")
        print("###############################")
        print()

        print("Les règles sont simples. Vous devez deviner un chiffre entre 0 et 10.000")
        print("Si votre réponse est inférieure je dirai c'est plus")
        print("Si votre réponse est supérieure je dirai c'est moins")
        print("Attention:")
        print("Vous avez 15 essaies, chaque mauvaise réponse vous perdez 3 points")
        print("Si vous trouvez la bonne réponse vous gagnerez 100 points plus 2 points par essaies restant.")
        print()

        print("3...", end='', flush=True)
        time.sleep(1)
        print("2...", end='', flush=True)
        time.sleep(1)
        print("1...", end='', flush=True)
        time.sleep(1)
        print("C'est parti!")
        print()

        random_number = random.randint(0, 10000)
        replay_input = False

        result = game_loop(random_number)

        if result["tries"] == 15 and result["current_points"] < 0:
            print(f"Dommage, le bon chiffre à trouver était : {random_number}.")
        
            user["total_lose"] += 1
            user["lose_streak"] += 1
            user["win_streak"] = 0

        elif result["current_points"] >= 0:
            current_points = result["current_points"] + (15 - result["tries"] * 3)
            user["total_points"] += current_points
        
            user["total_win"] += 1
            user["win_streak"] += 1
            user["lose_streak"] = 0
            
            if current_points > user["best_score"]:
                user["best_score"] = current_points

            if result["tries"] < user["best_tries"]:
                user["best_tries"] = result["tries"]

        display_score(user)

        while not replay_input:
            replay = input("Voulez-vous retenter votre chance? (oui ou non): ").lower()
            print()

            if replay == "non" or replay == "n":
                json_access('update', user)
                replay_input = True
                still_playing = False
            elif replay == "oui" or replay == "o":
                replay_input = True
            else:
                print("Erreur de saisie!")

#################
### variables ###
#################

file_data = json_access('read')
enter_program = False
user_data = None
pseudo_regex = r'^(?!.*[-_]{2})[A-Za-z0-9][A-Za-z0-9-_]{1,18}[A-Za-z0-9]$'
user_choice = 0
game_launched = False

######################
### Welcoming User ###
######################

print("Bienvenue dans ce programme!")
print()

while not enter_program:
    user_name = input("Veuillez entrer votre pseudo! ")

    if not validate_pseudo(user_name):
        print("Erreur: Pseudo invalide")
    else:
        enter_program = True

for user in file_data["users"]:
    if user["user_name"] == user_name:
        user_data = user
        break

if user_data is None:
    user_data = {
        "user_name": user_name,
        "total_points": 0,
        "best_score":0,
        "best_tries":15,
        "total_win":0,
        "total_lose": 0,
        "win_streak":0,
        "lose_streak":0
    }

while not game_launched:
    print("Menu: ")
    print("1. Jouer")
    print("2. Score")
    print("3. Quitter")
    user_choice = int(input("Veuillez faire un choix: "))
    print()

    match user_choice:
        case 1:
            game_instance(user_data)
            game_launched = True
        case 2:
            display_score(user_data)
        case 3:
            break
        case _:
            print("Erreur de saisie")

######################
### End of program ###
######################

exit_program()
print("A bientôt!")
time.sleep(2)
