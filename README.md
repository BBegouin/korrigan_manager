# korrigan_manager
une plateforme pour gérer un tournoi de bloodbowl type ronde suisse, avec quelques adaptations. 

#la ronde suisse : 
Les tournois de bloodbowl, à l'instar des tournois d'échecs, utilisent un système dit de "ronde suisse". 
L'appariement du premier tour est tiré au sort. Selon le résultat et les actions des matchs, chaque coach gagne un certain nombre de points. Les autres tour voient s'affronter deux à deux les coachs dont les nombres de points sont les plus proches. 

Le tournoi se déroule en 5 rondes, celui qui gagne est celui qui a accumulé le plus de points.

korrigan manager dispose d'une partie publique pour la consultation du classement en cours et d'une partie privée pour l'administration du tournoi.

La partie administration permet de :
- tirer les rondes
- saisir les résultats des matchs
- calculer automatiquement les points par club et par coach
- télécharger au format excel les appariements de ronde et les classements

#Spécificités du korrigan manager et Contraintes d'appariement : 
1- Spécificités
Chaque joueur appartient à un club
Chaque club peut élire une tête de série et une seule

2- Contraintes d'appariement : 
Sur la ronde 1 :
- les têtes de séries ne peuvent pas se rencontrer
- un club ne peut pas affronter deux têtes de séries

Sur toutes les rondes : 
- deux joueurs d'un même club ne peuvent pas se rencontrer

#Calcul des points
Les points de chaque coach sont calculés comme suit : 
- victoire : 3000 points
- nul : 1000 points
- défaite : 0 points

Pour chaque action, le joueur gagne les points suivants
- TD : 3 points
- Sortie : 2 points
- Interception : 2 points
- passe : 1 point
- aggression réussie : 5 points

Calcul des points de club : 
Les points d'un club sont calculés comme suit : 
- la somme des points des 4 meilleurs joueurs du club
- 100 points bonus par victoire de la tête de série
- 200 par tête de série adverse battue 
