from fltk import *

def vitesse(trajectoire):
    """
    Paramètre:
        -trajectoire (liste): liste des points parcourues par la voiture.
        
    Renvoie la vitesse de la voiture par rapport aux positions de trajectoire.
    
    """
    if len(trajectoire) < 2: #verifie s'il y a au moins 2 points dans la liste car sinon on peut pas calculer la vitesse
        return (0,0)  
    x1, y1 = trajectoire[-1] #on prend les 2 points du dernier élement de la liste
    x0, y0 = trajectoire[-2] #on prend les 2 points de l'avant dernier élement de la liste
    vitesse_x = x1 - x0 #on fait le calcul du x pour savoir la vitesse en x 
    vitesse_y = y1 - y0 #pareil avec y
    return (vitesse_x, vitesse_y)

def verif_collision(piste, debut, fin):
    """
    Paramètres:
        -piste (liste): piste de racetrack
        -debut (int): coordonnée
        -fin(int): coordonnée
        
    Fonction qui renvoie True si on touche une collision et False sinon.

    """
    if debut >= len(piste[0]) or fin >= len(piste) or debut < 0 or fin < 0:
        return True
    if piste[fin][debut] == "#": #on vérifie si le point de départ est dans un # si oui
         return True #on renvoie true ce qui signifie que le jeu est fini
    else:
        return False

def options(trajectoire, piste):
    """
    Paramètres:
        -trajectoire (liste): liste des points parcourues par la voiture
        -piste (liste): piste de racetrack
    
    Fonction qui renvoie la liste des points disponibles pour le déplacement de la voiture.
    """
    vitesses = vitesse(trajectoire)
    x = trajectoire[-1][0]+vitesses[0]
    y = trajectoire[-1][1]+vitesses[1]
    positions_voisines = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),  #ce sont toutes les positions qui avoisinent la position principale
                          (x, y - 1), (x, y), (x, y + 1), 
                          (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
    point_dispo=[]
    for coord in positions_voisines:
        if not verif_collision(piste,coord[0],coord[1]):
            point_dispo.append(coord)
    return point_dispo

def verification_victoire(trajectoire, carte):
    """
    Paramètres:
        -trajectoire (liste): liste des points parcourues par la voiture
        -carte (liste): piste de racetrack
        
    Fonction qui renvoie True si la voiture est arrivée à la fin de la piste, False sinon.
    """
    x = trajectoire[-1][0]
    y = trajectoire[-1][1]
    if carte[y][x] == "*":
        return True
    return False

def pixel_vers_case(x,y,taille_case):
    """
    Paramètres:
        -x (int): coordonnée en x
        -y (int): coordonnee en y
        -taille_case (int): taille d'une case
    Fonction qui convertit un nombre pixels vers le numéro de la case correspondant.
    """
    return (x//taille_case, y//taille_case)

def couleurs(vitesse):
    """
    Paramètre:
        -vitesse (int): vitesse de la voiture de la forme (x,y)
    
    Fonction qui renvoie couleur héxadécimale en fonction de la vitesse.
    Couleur bleue: vitesse 'lente'
    Couleur violette: vitesse 'moyenne'
    Couleur rouge: vitesse 'rapide'
    
    """
    vitesse_totale=abs(vitesse[0]+vitesse[1])
    
    if vitesse_totale <=3:
        return '#0000a' + str(vitesse_totale) #dégradé bleu
    elif vitesse_totale>=4 and vitesse_totale<6:
        return '#8'+str(vitesse_totale)+'008'+str(vitesse_totale) #dégradé violet
    elif vitesse_totale>=6 and vitesse_totale <10:
        return '#a'+ str(vitesse_totale) +'0000' #dégradé rouge
    else:
        return '#ff0000' #rouge
    
    
def dessine_trajectoire(vitesse, trajectoire, taille_case_x, taille_case_y,ligne_lst):
    """
    Paramètres:
        -vitesse (int): vitesse de la voiture de la forme (x,y)
        -trajectoire (liste): liste de coordonnées des points où la voiture est passée
        -taille_case_x (int): taille de la case en x
        -taille_case_y (int): taille de la case en y
        -ligne_lst (liste): liste de tuples qui sert à dessiner les lignes
        
    Fonction qui dessine les lignes avec les couleurs qui varient selon la vitesse.

    """
    x = taille_case_x
    y = taille_case_y
    
    if len(trajectoire) >= 2:
        couleur = couleurs(vitesse)
        ligne_lst.append((x * trajectoire[-2][0], y * trajectoire[-2][1], x * trajectoire[-1][0], y * trajectoire[-1][1], couleur))
    for elem in ligne_lst:
        ligne(elem[0], elem[1], elem[2], elem[3], elem[4], epaisseur="2")
        
def dessine_map(choix_map, taille_case_x, taille_case_y):
    """
    Paramètres:
        -choix_map (str) : Carte choisi txt
        -taille_case_x (int): taille de la case en x
        -taille_case_y (int): taille de la case en y

    Fonction qui dessine la carte sur la fenêtre.
    """
    for y in range(len(choix_map)):
        for x in range(len(choix_map[y])):
            couleur = ""
            if choix_map[y][x] == '#':
                couleur = "green"
            elif choix_map[y][x] == '*':
                couleur = "gray"
            elif choix_map[y][x] == '>':
                couleur = "brown"
            elif choix_map[y][x] == '.':
                couleur = "lightgray"
            rectangle(x * taille_case_x, y * taille_case_y,
                    (x + 1) * taille_case_x, (y + 1) * taille_case_y,
                    couleur="black", remplissage=couleur)
def charger(fichier):
    """
    Paramètre :
        -fichier (str):  destination vers la carte

    Fonction qui charge le fichier donné.
    """
    with open(fichier, 'r') as fichier:
        return [ligne.strip() for ligne in fichier]

def solveur(trajectoire, visite, choix_map, taille_case_x, taille_case_y, ligne_lst):
    """
    Paramètres:
        -trajectoire (liste): liste des points parcourues par la voiture.
        -visite (set): ensemble des couples (position, vitesse) parcourues par la voiture.
        -choix_map (liste): piste de racetrack.
        -taille_case_x (int): taille de la case en x
        -taille_case_y (int): taille de la case en y
        -ligne_lst (liste): liste de tuples qui sert à dessiner les lignes.
    
    Fonction qui cherche une trajectoire du départ à l'arrivée et affiche les mouvements en temps réel.
    """
    position = trajectoire[-1]
    vitesses = vitesse(trajectoire)
    c = (position, vitesses)
    if verification_victoire(trajectoire, choix_map):
        return True
    if c in visite:
        return False
    visite.add(c)
    for o in options(trajectoire, choix_map):
        trajectoire.append(o)
        efface_tout()
        dessine_map(choix_map, taille_case_x, taille_case_y)
        dessine_trajectoire(vitesses, trajectoire, taille_case_x, taille_case_y, ligne_lst)   
        mise_a_jour()
        if solveur(trajectoire, visite, choix_map, taille_case_x, taille_case_y, ligne_lst):
            return True
        else:
            trajectoire.pop()
            efface_tout()
            dessine_map(choix_map, taille_case_x, taille_case_y)
            dessine_trajectoire(vitesses, trajectoire, taille_case_x, taille_case_y, ligne_lst)
            mise_a_jour()
    return False


if __name__ == "__main__":
    
    visite = set()
    largeur_fenetre = 1000
    hauteur_fenetre = 1000
    cree_fenetre(largeur_fenetre, hauteur_fenetre)
    boucle = True

    while boucle:
        menu = True
        choix = True
        jouer = True
        solver = False
        choix_map = ""
        
        position_l = []
        position_choix = [(0,0)]
        ligne_lst = []
        
        rectangle(400, 500, 600, 400, couleur="cyan", remplissage="cyan")
        rectangle(400, 600, 600, 700, couleur="cyan", remplissage="cyan")
        texte(455,428,"Jouer",couleur="black")
        texte(455,628,"Solver",couleur="black")
        texte(420,50, "Race", couleur="Red")
        texte(488,50, "Track", couleur="black")
        
        trajectoire = []

        while menu:
            
            ev = donne_ev()
            tev = type_ev(ev)
            if tev == 'ClicGauche':
                position = (abscisse(ev), ordonnee(ev))
                position_l.append(position)
                x = position_l[-1][0]
                y = position_l[-1][1]
                if position_l[-1][0] >= 400 and position_l[-1][0] <= 600 and position_l[-1][1] >= 400 and position_l[-1][1] <= 500: #choix jouer
                    menu = False
                if position_l[-1][0] >= 400 and position_l[-1][0] <= 600 and position_l[-1][1] >= 600 and position_l[-1][1] <= 700: #choix solver
                    solver = True #pour rentrer dans la boucle solver
                    menu = False
                    jouer = False #pour ne pas rentrer dans la boucle jouer
            elif tev == 'Quitte':
                    break
            
            mise_a_jour()
        efface_tout()
        
        #les rectangles et textes du menu du choix des maps
        rectangle(150, 250, 350, 350, couleur="palegoldenrod", remplissage="palegoldenrod")  # (map-mini)
        rectangle(650, 250, 850, 350, couleur="khaki", remplissage="khaki")  # (map test)
        rectangle(400, 550, 600, 450, couleur="moccasin", remplissage="moccasin")  # (map 1)
        rectangle(150, 750, 350, 650, couleur="navajowhite", remplissage="navajowhite")  # (map 2)
        rectangle(650, 750, 850, 650, couleur="bisque", remplissage="bisque")  # (map 3)
        texte(180,280,"Map Mini",couleur="black") 
        texte(183,680,"Map test",couleur="black")
        texte(455,480,"Map 1",couleur="black")
        texte(700,280,"Map 2",couleur="black")
        texte(700,680,"Map 3",couleur="black")
        texte(220,100, "Veuillez choisir la carte de votre choix", couleur="black")
        
        while choix: #boucle du choix entre les maps
            ev = donne_ev()
            tev = type_ev(ev)
            if tev == 'ClicGauche':
                position = (abscisse(ev), ordonnee(ev))
                position_choix.append(position)
            if position_choix[-1][0] >= 150 and position_choix[-1][0] <= 350 and position_choix[-1][1] >= 250 and position_choix[-1][1] <= 350:
                fichier = "pistes/maps-texte/map_mini.txt"
                choix_map = charger(fichier)
                trajectoire.append((1,1)) #départ
                choix = False
            # Ouverture de la map test
            if position_choix[-1][0] >= 150 and position_choix[-1][0] <= 350 and position_choix[-1][1] >= 650 and position_choix[-1][1] <= 750:
                trajectoire.append((3,31))
                fichier = "pistes/maps-texte/map_test.txt"
                choix_map = charger(fichier)
                choix = False
            # Ouverture de la map 1
            if position_choix[-1][0] >= 400 and position_choix[-1][0] <= 600 and position_choix[-1][1] >= 450 and position_choix[-1][1] <= 550:
                trajectoire.append((33,5))
                fichier = "pistes/maps-texte/map1.txt"
                choix_map = charger(fichier)
                choix = False
            # Ouverture de la map 2
            if position_choix[-1][0] >= 650 and position_choix[-1][0] <= 850 and position_choix[-1][1] >= 250 and position_choix[-1][1] <= 350:
                trajectoire.append((6,6))
                fichier = "pistes/maps-texte/map2.txt"
                choix_map = charger(fichier)
                choix = False
            # Ouverture de la map 3
            if position_choix[-1][0] >= 650 and position_choix[-1][0] <= 850 and position_choix[-1][1] >= 650 and position_choix[-1][1] <= 750:
                trajectoire.append((32,5))
                fichier = "pistes/maps-texte/map3.txt"
                choix_map = charger(fichier)
                choix = False
            elif tev == 'Quitte':
                    break
            mise_a_jour()

        efface_tout()
        
        nombre_colonnes = len(choix_map[0])
        nombre_lignes = len(choix_map)
        taille_case_x = largeur_fenetre // nombre_colonnes
        taille_case_y = hauteur_fenetre // nombre_lignes
        
        while solver: #boucle du solver
            
            efface_tout()
            
            dessine_map(choix_map, taille_case_x, taille_case_y)
            option = options(trajectoire, choix_map)
            dessine_trajectoire(vitesse(trajectoire), trajectoire, taille_case_x, taille_case_y,ligne_lst)
            
            for elem in option: #affichage des points disponibles pour déplacement
                cercle(taille_case_x*elem[0], taille_case_y*elem[1], 4, couleur="black", remplissage="white")
                
            ev = donne_ev()
            tev = type_ev(ev)
            if tev == 'ClicGauche':
                position = (abscisse(ev), ordonnee(ev))
                x, y = pixel_vers_case(abscisse(ev), ordonnee(ev), taille_case_y)
            elif tev == 'Touche':
                nom_touche = touche(ev)
                if nom_touche == 'Escape':
                    efface_tout()
                    solver=False
            elif tev == 'Quitte':
                ferme_fenetre()
                break
            
            solveur(trajectoire, visite, choix_map, taille_case_x, taille_case_y, ligne_lst)

            if verification_victoire(trajectoire, choix_map):
                texte(360,450,"Vous avez gagné!", couleur="black")
                mise_a_jour()
                solver = False
                boucle = False
                break
            
            mise_a_jour()

        ligne_lst = []

        while jouer: #boucle du jeu (ou on choisis les positions où on va)
            
            efface_tout()

            dessine_map(choix_map, taille_case_x, taille_case_y)
            option = options(trajectoire, choix_map)           
            dessine_trajectoire(vitesse(trajectoire), trajectoire, taille_case_x, taille_case_y,ligne_lst)
        
            for elem in option: #affichage des points disponibles pour déplacement
                cercle(taille_case_x*elem[0], taille_case_y*elem[1], 4, couleur="black", remplissage="white")
            cercle(taille_case_x*trajectoire[-1][0],taille_case_y*trajectoire[-1][1], 4, couleur="black", remplissage="black") #affichage de la voiture
            
            ev = donne_ev()
            tev = type_ev(ev)
            if tev == 'ClicGauche':
                position = (abscisse(ev), ordonnee(ev))
                x, y = pixel_vers_case(abscisse(ev), ordonnee(ev), taille_case_y)
                if (x,y) in option:
                    trajectoire.append((x,y)) #on ajoute la position des options où on a appuyé           
            elif tev == 'Touche':
                nom_touche = touche(ev)
                if nom_touche == 'BackSpace' and len(trajectoire) >= 2 : #condition pour que on ne pop pas le vide
                    trajectoire.pop()
                if nom_touche == 'Escape':
                    efface_tout()
                    jouer=False
                    
            elif tev == 'Quitte':
                ferme_fenetre()
                break
            
            if option == []:
                texte(360,450, "Vous avez perdu!", couleur="red")
                boucle = False
                break 
    
            if verification_victoire(trajectoire, choix_map):
                dessine_trajectoire(vitesse(trajectoire), trajectoire, taille_case_x, taille_case_y,ligne_lst) #on dessine la dernière ligne vers la dernière position où on a appuyé
                texte(360,450,"Vous avez gagné!", couleur="black")
                mise_a_jour()
                boucle = False
                break
            
            mise_a_jour()


