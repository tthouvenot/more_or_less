#################################
###                           ###
###     Jeu Plus ou Moins     ###
###                           ###
### Author: Tristan Thouvenot ###
### Version: 0.1              ###
### Date: 26/09/2024          ###
#################################

# L'objectif est de créer le jeu du juste prix. 
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
# Game Rules:
#   - l'utilisateur à 15 essaies
#   - chaque essaie lui fait perdre 3 points
#   - une victoire lui donne 100 points
#
# Game Loop:
# - on sélectionne un int random entre 0 et 10000
# - On demande à l'utilisateur
# - si sa réponse est:
#   - plus basse on lui dit c'est plus et on lui redemande
#   - plus haute on lui dit c'est moins et on lui redemande
#   - pas un chiffre entre 0 et 10000:
#       - on le prévient et il perd ni un essaie ni des points
# - La partie finie s'il a trouvé le bon chiffre ou plus aucun essaie
# - On lui demande s'il veut rejouer
#   - oui on relance le jeu
#   - non on enregistre les datas dans le fichier JSON et on fait un résumé de ses stats. On lui demande d'appuyer sur un bouton pour quitter le programme
