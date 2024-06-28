########################################
Auteur.e : BIHET Lucie Term01
Réalisé sous Python 2.7
Bibliothèques utilisées : mcpi, random, et time
########################################

----------------------------------------
Présentation du projet :
- réalisation d'un labyrinthe aléatoire avec deux modes de jeu:
	- une résolution auto avec le chemin s'affichant au fur et à mesure à l'aide d'un algorithme de résolution
	- un mode libre et interactif où le joueur doit résoudre le labyrinthe de lui-même et où certains évènements interviennent lorsqu'il marche sur certains blocks
- résolution auto :
	- le chemin emprunté par l'algorithme appaît tout au long du labyrinthe sous la forme de blocks de laine violette
	- il y a une pose d'une demi seconde entre chaque déplacement pour laisser le temps au joeur de suivre les blocks
- mode libre :
	- après le lancement de la partie, le joueur entre dans le labyrinthe et a tout le temps qu'il le souhaite pour le compléter
	- une boucle lancée au début de la partie vérifie à chaque instant si le joueur marche sur un block d'évènement, si c'est le cas, l'évènement est activé
----------------------------------------

****************************************
Informations avant de lancer le programme/jeu :
- Il est préférable d'être en mode créatif
- Les chargements peuvent s'avérer long, lors des aplanissements de terrains notamment
- Avant de faire un click droit sur le block de démarrage du jeu, il faut se munir d'un épee sinon cela ne marchera pas
- Il faut relancer le programmes à chaque fois qu'il se termine pour relancer le jeu et choix du mode
- Vous pouvez changer si vous le souhaitez la taille du labyrinthe en modifiant la constante "TAILLE_LABY" ligne 9 du programme
- Infos spécifiques au mode libre :
	- Bien évidemment, le labyrinthe peut être contourné mais il est quand même plus interressant de le faire pour le bien du projet :)
	- Quand le labyrinthe est fini, veillez à rester sur les blocks de bedrock jusqu'à ce que le final s'active
	- Pour l'évènempent des blocks d'or, regardez en l'air
****************************************

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Problèmes rencontrés :
- le input() en 2.7 ne transforme pas le texte entré en str directement j'ai donc préféré éviter d'utiliser cette fonctionnalité pour le choix du mode pour la taille du labyrinthe
- le programme ne fonctionne pas tout le temps sur les ordinateurs du lycée (même si il marche la plupart du temps) cependant il marche à chaque fois sur mon pc
- il y a parfois de très grandes latences, ce qui est ennuyeux pour le bon fonctionnement
- quand le feu d'artifice est en cours, la boucle de vérification des évènements est en pause, empêchant leur déclenchement pendant environ 3 à 4 secondes après le lancement du feu d'artifice
- créer un algorithme de génération aléatoire de labyrinthe est bien plus compliqué que ce que je pensais, j'ai donc cherché beaucoup d'exemple avant de réussir à faire quelque chose de satisfaisant
(ma plus grosse inspiration vient d'ici : https://rosettacode.org/wiki/Maze_generation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~