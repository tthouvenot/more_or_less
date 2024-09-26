#################################
###                           ###
###     Jeu Plus ou Moins     ###
###                           ###
### Author: Tristan Thouvenot ###
### Version: 0.2              ###
### Date: 26/09/2024          ###
#################################

# L'objectif est de créer le jeu du juste prix. 
# //On télécharge les données du fichier JSON
# L'utilisateur va fournir son nom
#   Si il est présent dans le fichier data:
#       - on récupère ses données
#   Sinon:
#       - on le créera dans le fichier une fois le jeu fini
# On offre la possibilité à l'utilisateur de choisir entre:
#   - afficher ses résultats précédents:
#       - son total de points (ne peut pas être négatif)
#       - son record de rapidité
#       - son nombre de victoire d'affilé (si en cours)
#       - son nombre de défaite d'affilé (si en cours)
#   - jouer
#       - on lance le jeu
#   - quitter
#
# //Game Rules:
#   //- l'utilisateur à 15 essaies
#   //- chaque essaie lui fait perdre 3 points
#   //- une victoire lui donne 100 points
#
# Game Loop:
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
#   - non :
#       //- on enregistre les datas dans le fichier JSON 
#       - on fait un résumé de ses stats. 
#       //- On lui demande d'appuyer sur un bouton pour quitter le programme

import random
import time
import json

#################
### variables ###
#################

still_playing = True
total_points = 0
user_data = None
updated_datas = None

#################
### functions ###
#################

def json_access(task, datas = None, updated_datas = None):

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

        if 'users' in current_data:
            current_data['users'].append(updated_datas)
        else:
            current_data['users'] = [updated_datas]
        return current_data


def game_loop(rand):
    
    tries = 0
    end_of_game = False
    current_point = 0

# TODO: Change tries when program is finished
    while tries < 1 and not end_of_game:
        try:
            user_answer = int(input("Quel est votre chiffre? "))

            if user_answer < rand and user_answer <= 10000:
                print("C'est plus!")
                tries += 1
                current_point -= 3
            elif user_answer > rand and user_answer >= 0:
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
    
    return current_point

def exit_program():

    quit_game = False

    while not quit_game:
        button_press = input("Merci de votre participation. Veuillez appuyer sur la touche \"q\" pour quitter le jeu!: ").lower()

        if button_press != "q":
            print("Erreur: saisie incorrect!")
        else:
            quit_game = True

def game_instance(user):
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
        print("Si vous trouvez la bonne réponse vous gagnerez 100 points.")
        print()

        print("3...", end='', flush=True)
        time.sleep(1)
        print("2...", end='', flush=True)
        time.sleep(1)
        print("1...", end='', flush=True)
        time.sleep(1)
        print("C'est parti!")
        print()

        win = 0
        lose = 0
        random_number = random.randint(0, 10000)

        result = game_loop(random_number)

        if result == 0:
            print(f"Dommage, le bon chiffre à trouver était : {random_number}.")
            lose +=1
            win = 0
        elif result >= 0:
            total_points += result
            win += 1
            lose = 0

        replay = input("Voulez-vous retenter votre chance? (oui ou non): ").lower()
        print()

        if replay == "non" or replay == "n":
            json_access('write', file_data)
            still_playing = False

######################
### Welcoming User ###
######################

file_data = json_access('read')

#################
### Game Loop ###
#################

game_instance(user_data)

######################
### End of program ###
######################

exit_program()
print("A bientôt!")
time.sleep(2)
