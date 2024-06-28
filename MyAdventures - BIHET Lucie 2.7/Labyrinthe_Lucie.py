## Importations des bibliothèques ##
from random import shuffle, randint
from time import sleep
from math import floor
import mcpi.minecraft as minecraft


## Variable globale ##
TAILLE_LABY = 15  # mettre des valeurs entre 2 et 40 seulement

## Création du monde minecraft ##
mc = minecraft.Minecraft.create()


## Classe Pile ##
class Pile:
    ''' classe Pile
    création d'une instance Pile avec une liste
    '''
    def __init__(self):
        "Initialisation d'une pile vide"
        self.liste = []

    def vide(self):
        "teste si la pile est vide"
        return self.liste == []

    def depiler(self):
        "dépile"
        assert not self.vide(), "Pile vide"
        return self.liste.pop()

    def empiler(self, x):
        "empile"
        self.liste.append(x)

    def sommet(self):
        """doc"""
        return self.liste[-1]

    def taille(self):
        """doc"""
        return len(self.liste)


## Classe Labyrinthe ##
class Labyrinthe:
    """création de la classe Labyrinthe"""
    def __init__(self, taille=10):
        """initialisation de la classe Labyrinthe"""
        self.taille = taille
        self.visite = [[0] * self.taille + [1] for loop in range(self.taille)] + [[1] * (self.taille + 1)]  # grille pour vérifier quelles cases ont été visitées
        self.ligne1 = [["10"] * self.taille + ['1'] for loop in range(self.taille)] + [[]]
        self.ligne2 = [["11"] * self.taille + ['1'] for loop in range(self.taille + 1)]
        self.xdepart, self.ydepart, self.zdepart = mc.player.getPos()
        self.xdepart += 5
        self.zdepart -= 1

    def cree_laby(self):
        """crée un tableau avec des 0 pour le chemin et des 1 pour les murs"""
        self.creuse(randint(0, self.taille-1), randint(0, self.taille-1))
        liste = []
        for i in range(len(self.ligne1)-1):
            liste.append(self.ligne2[i])
            liste.append(self.ligne1[i])
        liste.append(self.ligne2[-1])
        liste[0][0] = '10'
        liste[-1][-2] = '10'

        liste2 = []
        for elt in liste:
            sous_liste2 = []
            for elt2 in elt:
                for elt3 in elt2:
                    sous_liste2.append(elt3)
            liste2.append(sous_liste2)
        return liste2

    def creuse(self, x, y):
        """ 'creuse' le chemin afin de créer un labyrinthe aléatoire"""
        self.visite[y][x] = 1  # met en 'visitée' la case en cours de visite
        voisins = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]  # voisins de la case visitée
        shuffle(voisins)  # mélange des voisins de la case visitée pour ne pas tjrs visiter la même
        for (xvoisin, yvoisin) in voisins:
            if not self.visite[yvoisin][xvoisin]:  # si la case n'a pas été vistée
                if xvoisin == x:
                    self.ligne2[max(y, yvoisin)][x] = "10"
                if yvoisin == y:
                    self.ligne1[y][max(x, xvoisin)] = "00"
                self.creuse(xvoisin, yvoisin)

    def laby(self):
        """crée et lance le labyrinthe pour le mode normal"""
        laby = self.cree_laby()
        for i in range(len(laby)):
            for j in range(len(laby[i])):
                if int(laby[i][j]) == 1:
                    self.laby_mur(i, j)
                elif j == (len(laby) - 2) and i == (len(laby) - 1):
                    mc.setBlock(self.xdepart+i, self.ydepart-1, self.zdepart+j, 7)
                    mc.setBlocks(self.xdepart+i, self.ydepart-1, self.zdepart+j-2, self.xdepart+i+4, self.ydepart-1, self.zdepart+j+2, 7)
                else:
                    self.laby_chemin(i, j)

    def laby_resol(self):
        """crée et lance le labyrinthe pour le mode résolu"""
        laby = self.cree_laby()
        for i in range(len(laby)):
            for j in range(len(laby[i])):
                if int(laby[i][j]) == 1:
                    self.laby_mur(i, j)
                else:
                    mc.setBlock(self.xdepart+i, self.ydepart-1, self.zdepart+j, 2)
        sleep(5)
        resol_laby = ResolutionLabyrinthe(laby)
        resol_laby.resol_lab(self.xdepart, self.ydepart, self.zdepart)

    def jeu_encours(self):
        """fonction vérifiant tout au long du jeu si le joueur active des évènements"""
        encours = True
        event = Evenement()
        while encours:
            x, y, z = mc.player.getPos()
            block = mc.getBlock(x, y-1, z)
            if block == 121:
                event.champignon(x, y, z)
            elif block == 35:
                event.laine_random(x, y, z)
            elif block == 41:
                event.feu_artifice(x, y, z)
            elif block == 7:
                event.final()
                encours = False

    def laby_mur(self, i, j):
        """place les blocks pour les murs en choisissant au hasard entre 3 blocks différents pour plus de diversité"""
        mc.setBlock(self.xdepart+i, self.ydepart, self.zdepart+j, 98, randint(0, 3))
        mc.setBlock(self.xdepart+i, self.ydepart+1, self.zdepart+j, 98, randint(0, 3))
        mc.setBlock(self.xdepart+i, self.ydepart+2, self.zdepart+j, 98, randint(0, 3))

    def laby_chemin(self, i, j):
        """place les blocks du chemins, cela peut être un block déclenchant un évènement ou non"""
        rd = randint(1, 10)
        if rd == 1:
            rd2 = randint(1, 3)
            if rd2 == 1:
                block = 121
            elif rd2 == 2:
                block = 35
            else:
                block = 41
            mc.setBlock(self.xdepart+i, self.ydepart-1, self.zdepart+j, block)


## Classe Résolution de Labyrinthe ##
class ResolutionLabyrinthe:
    """création de la classe ResolutionLabyrinthe"""
    def __init__(self, laby):
        """initialisation de la classe ResolutionLabyrinthe"""
        self.laby = laby

    def resol_lab(self, x, y, z):
        """ce code vient du lab sur les piles et permet la résolution du labyrinthe
        le code a été modifié pour correspondre à ce qui doit apparaître sur minecraft"""
        entree = (0, 1)
        sortie = (len(self.laby)-1, len(self.laby[0])-2)
        HAUTEUR, LARGEUR = len(self.laby), len(self.laby[0])

        def voisins(tab, visite):
            """cherche les voisins de visite"""
            liste_voisin = []
            i, j = visite[0], visite[1]
            for a in (-1, 1):
                if 0 <= i + a < HAUTEUR:
                    if tab[i + a][j] == '0':
                        liste_voisin.append((i + a, j))
                if 0 <= j + a < LARGEUR:
                    if tab[i][j+a] == '0':
                        liste_voisin.append((i, j+a))
            return liste_voisin

        def parcours(laby, entree, sortie):
            """parcours de résolution auto du labyrinthe"""
            tab = laby
            pile1 = Pile()
            visite = entree
            tab[entree[0]][entree[1]] = -1
            recherche = True
            while recherche:
                liste_voisin = voisins(tab, visite)
                if liste_voisin == []:
                    if pile1.liste == []:
                        return False
                    else:
                        visite = pile1.depiler()
                        mc.setBlock(x + visite[0], y-1, z + visite[1], 2)
                else:
                    pile1.empiler(visite)
                    mc.setBlock(x + visite[0], y-1, z + visite[1], 35, 2)
                    visite = liste_voisin[-1]
                    tab[visite[0]][visite[1]] = -1
                    if visite == sortie:
                        pile1.empiler(visite)
                        recherche = False
                sleep(0.5)
            mc.setBlock(x + sortie[0], y-1, z + sortie[1], 35, 2)
        parcours(self.laby, entree, sortie)


## Classe Evènement ##
class Evenement():
    """création de la classe Evenement"""
    def __init__(self):
        """initialisation de la classe Evenement"""
        self.x, self.y, self.z = mc.player.getTilePos()

    def feu_artifice(self, x, y, z):
        """fonction pour le déroulement du feu d'artifice"""
        couleur = randint(0, 15)
        mc.setBlock(x, y, z, 35)
        mc.setBlock(x, y, z, 0)
        for i in range(1, 10):
            mc.setBlock(x, y+i, z, 35, couleur)
            mc.setBlock(x, y+i-1, z, 0)
            sleep(0.2)
        for j in range(5):
            mc.setBlock(x+j, y+i+j, z, 35, couleur)
            mc.setBlock(x-j, y+i+j, z, 35, couleur)
            mc.setBlock(x, y+i+j, z+j, 35, couleur)
            mc.setBlock(x, y+i+j, z-j, 35, couleur)
            sleep(0.1)
            mc.setBlock(x+j, y+i+j, z, 0)
            mc.setBlock(x-j, y+i+j, z, 0)
            mc.setBlock(x, y+i+j, z+j, 0)
            mc.setBlock(x, y+i+j, z-j, 0)

        for k in range(5):
            mc.setBlock(x+j+k, y+i+j, z, 35, couleur)
            mc.setBlock(x-j-k, y+i+j, z, 35, couleur)
            mc.setBlock(x, y+i+j, z+j+k, 35, couleur)
            mc.setBlock(x, y+i+j, z-j-k, 35, couleur)
            sleep(0.1)
            mc.setBlock(x+j+k, y+i+j, z, 0)
            mc.setBlock(x-j-k, y+i+j, z, 0)
            mc.setBlock(x, y+i+j, z+j+k, 0)
            mc.setBlock(x, y+i+j, z-j-k, 0)
        for l in range(5):
            mc.setBlock(x+j+k+l, y+i+j-l, z, 35, couleur)
            mc.setBlock(x-j-k-l, y+i+j-l, z, 35, couleur)
            mc.setBlock(x, y+i+j-l, z+j+k+l, 35, couleur)
            mc.setBlock(x, y+i+j-l, z-j-k-l, 35, couleur)
            sleep(0.1)
            mc.setBlock(x+j+k+l, y+i+j-l, z, 0)
            mc.setBlock(x-j-k-l, y+i+j-l, z, 0)
            mc.setBlock(x, y+i+j-l, z+j+k+l, 0)
            mc.setBlock(x, y+i+j-l, z-j-k-l, 0)

    def champignon(self, x, y, z):
        """pose un champignon"""
        mc.setBlock(x, y, z, 40)

    def laine_random(self, x, y, z):
        """change la couleur du block de laine"""
        mc.setBlock(x, y-1, z, 35, randint(0, 15))

    def gomme(self):
        """crée une surface plane et vide"""
        mc.setBlocks(self.x-25, self.y-1, self.z-25, self.x+100, self.y-5, self.z+100, 2)
        mc.setBlocks(self.x-25, self.y, self.z-25, self.x+100, self.y+100, self.z+100, 0)

    def final(self):
        """crée les évènements qui se lancent lors de la sortie du labyrinthe"""
        valeur = 4
        x, y, z = mc.player.getPos()
        for i in range(-valeur, valeur):
            for j in range(-valeur, valeur//20):
                for k in range(-valeur, valeur):
                    if i**2 + j**2 + k**2 < valeur**2:
                        mc.setBlock(x+i, y+j+valeur+10, z-k, 20)
        mc.player.setPos(x, y+j+valeur+11, z)
        for loop in range(20):
            self.feu_artifice(x + randint(-30, 30), y + randint(5, 15), z + randint(-30, 30))


## Classe lancement ##
class Lancement():
    """création de la classe Lancement"""
    def __init__(self):
        """initialisation de la classe Lancement"""
        self.event = Evenement()

    def explications(self):
        """fonction permettant d'afficher dans la console et dans le jeu les explications"""
        print("Bonjour, bonjour et bienvenue !")
        print("Lisez les indications depuis le jeu maintenant")
        mc.postToChat("Il est preferable de jouer en creatif et si vous n'etes pas sur d'y etre tapez '/gamemode 1' dans le chat")
        mc.postToChat("")
        sleep(2)
        mc.postToChat("Il y a deux modes disponibles")
        mc.postToChat("")
        sleep(2)
        mc.postToChat("Un est un labyrinthe genere aleatoirement avec des petites surprises tout au long du parcours")
        mc.postToChat("")
        sleep(2)
        mc.postToChat("L'autre est un algorithme de resolution du labyrinthe avec le parcours qui s'affiche en temps reel")
        mc.postToChat("")
        sleep(2)
        mc.postToChat("Equipez vous d'une epee et faites un click droit sur le bloc bleu pour le labyrinthe non resolu et le rouge pour celui avec la resolution")
        mc.postToChat("")

    def mode_libre(self):
        """permet le démrrage du mode libre"""
        mc.postToChat("Vous avez lancer le mode sans resolution auto. Bonne chance !")
        laby1 = Labyrinthe(TAILLE_LABY)
        self.event.gomme()
        laby1.laby()
        laby1.jeu_encours()

    def mode_auto(self):
        """permet le démrrage du mode auto"""
        mc.postToChat("Vous avez lancer le mode avec resolution auto. Suivez le circuit ! Cela commence dans 5 secondes")
        laby2 = Labyrinthe(TAILLE_LABY)
        self.event.gomme()
        laby2.laby_resol()


## Main ##
def main():
    """fonction principale permettant de lancer les explications et le choix du labyrinthe"""
    event1 = Evenement()
    lancement = Lancement()
    event1.gomme()
    lancement.explications()
    x, y, z = mc.player.getPos()
    mc.player.setPos(x, y, z)
    mc.setBlock(x+2, y, z, 35, 11)  # laine bleue
    mc.setBlock(x+2, y, z+1, 35, 14)  # laine rouge
    attente = True
    while attente:
        coups = mc.events.pollBlockHits()
        for coup in coups:
            if coup.pos.x == floor(x+2) and coup.pos.y == floor(y) and coup.pos.z == floor(z):
                attente = False
                lancement.mode_libre()
            elif coup.pos.x == floor(x+2) and coup.pos.y == floor(y) and coup.pos.z == floor(z+1):
                attente = False
                lancement.mode_auto()
main()
