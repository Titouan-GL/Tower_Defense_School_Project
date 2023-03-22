#!/usr/bin/env python3
# coding:utf8

#################### INITIATIONS ET IMPORTATIONS ########################
import sys
print(sys.path)
import pygame
pygame.init()
import TDGraphics #on vas chercher du fichier graphique
import TDlevels #on importe le fichier des niveaux
from random import randrange
from pygame.locals import *
### variable importantes
run = True 

proportion = 0.8
WINDOWHEIGHT = 1000 * proportion #dimentions de la fenêtre
WINDOWWIDTH = 1000 * proportion
flags = DOUBLEBUF
window = TDGraphics.graphics(int(WINDOWWIDTH+130),int(WINDOWHEIGHT), flags) #on appelle la fonction pour dessiner la fenetre qui provient du fichier graphique

#################### INITIATIONS ET IMPORTATIONS ########################
import pygame
pygame.init()
import TDGraphics #on vas chercher du fichier graphique
from random import randrange

### variable importantes
run = True 

WINDOWHEIGHT = 1000 #dimentions de la fenêtre
WINDOWWIDTH = 1500

window = TDGraphics.graphics(WINDOWWIDTH,WINDOWHEIGHT, flags) #on appelle la fonction pour dessiner la fenetre qui provient du fichier graphique

################### CLASSES #########################

class Turret(object): #on créé la classe des tourelles
	def __init__(self, x, y,color, ranged = 0,  benefit = 0, width = 64, height = 64, damage = 10):
		self.x = x
		self.y = y
		self.color = color
		self.ranged = ranged
		self.width = width
		self.height = height
		self.being_placed = True
		self.benefit = benefit
		self.locked = False
		self.lock = 0
		self.damage = damage

class Newturret(object): #on créé la classe des boutons pour les tourelles
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.width = 64
		self.height = 64
		self.color = color
	
class Location(object): #on créé la classe pour les emplacements de tourelles
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = 64
		self.height = 64
		self.used = False

class Allies(object):
	def __init__(self, x, y, life, damage, ranged, width = 10, height = 10, speed= 2):
		self.x = x
		self.y = y
		self.life = life
		self.damage = damage
		self.benefit = benefit
		self.ranged = ranged
		self.width = width
		self.height = height
		self.alive = True

class Base(object):
	def __init__(self, x, y, life = 2000, damage = 10, benefit = 0.03, ranged= 100, width = 100, height = 100):
		self.x = x
		self.y = y
		self.life = life
		self.damage = damage
		self.benefit = benefit
		self.ranged = ranged
		self.width = width
		self.height = height
		self.locked = False
		self.lock = 0

class Champion(object):
	def __init__(self, x, y, life=100, damage=10, ranged=0, width= 64, height= 64,lvl=1):
		self.x = x
		self.y = y
		self.life = life
		self.damage = damage
		self.ranged = ranged
		self.width = width
		self.height = height
		self.locked = False
		self.lock = 0
		self.lvl = 1


class Ennemy(object):
	def __init__(self, x, y, life, damage, direction, ranged, speed = 2, width = 10, height = 10, ground = True):
		self.x = x
		self.y = y
		self.life = life
		self.damage = damage
		self.ranged = ranged
		self.direction = direction
		self.speed = speed
		self.width = width
		self.height = height
		self.ground = ground
		self.alive = True
		self.locked = False
		self.lock = 0
##################### FONCTIONS #########################
def createnewturret1(Turret):
	return(Turret(
	pygame.mouse.get_pos()[0]+(turretWidth//2), 
	pygame.mouse.get_pos()[1]+(turretHeight//2),
	(0,122,15), 100, 0, turretWidth, turretHeight))

def createnewfarm(Turret):
	return(Turret(
	pygame.mouse.get_pos()[0]+(turretWidth//2), 
	pygame.mouse.get_pos()[1]+(turretHeight//2),
	(239,209,88), 0, 0.01, turretWidth, turretHeight))

def createnewsoldier1(Allies):
	return(Allies(
	pygame.mouse.get_pos()[0]+(5), 
	pygame.mouse.get_pos()[1]+(5),
	50, 5, 0, 70))

def createnewennemy1(Ennemy):
	return(Ennemy(0, WINDOWHEIGHT//2, 50, 5, "right", 70))

##################### VARIABLES #########################

turretbutton = [] #La liste de tout les boutons
turrets = [] #la liste de toutes les tourelles 
locations = [] #la liste de tout les emplacements
ennemies = [] # la liste de tout les ennemis
ennemies.append(createnewennemy1(Ennemy))
base = Base(WINDOWWIDTH//2 - 50, WINDOWHEIGHT//2 -50, 2000, 25, 0.1, 100, 100, 100)
soldiers = []
turretbutton.append(Newturret(0, WINDOWHEIGHT -64, (255, 0, 0))) #on ajoute des boutons
turretbutton.append(Newturret(65, WINDOWHEIGHT -64, (100, 100, 0)))
money = 50
turretWidth = 64
turretHeight = 64
for i in range(5):
	locations.append(Location(randrange(50,WINDOWWIDTH-50),randrange(50,WINDOWHEIGHT-200)))

#################### MAIN LOOP ######################


while run: # tant que on joue
	pygame.time.delay(10) #il capte une information toutes les x milisecondes
	
	for event in pygame.event.get(): # si on appuie sur une touche
		### QUITTER
		if event.type == pygame.QUIT:#si on quitte
			run = False
		if event.type == pygame.MOUSEBUTTONUP: #si on clique quelque part
			
			#### BOUTON POUR NOUVELLES TOURELLES
			if pygame.mouse.get_pos()[0] <= turretbutton[0].x + turretbutton[0].width and pygame.mouse.get_pos()[0] >= turretbutton[0].x and pygame.mouse.get_pos()[1] <= turretbutton[0].y + turretbutton[0].height and pygame.mouse.get_pos()[1] >= turretbutton[0].y :
					if len(turrets) > 0: #si c'est le cas et que il y a déjà une tourelle
						if turrets[-1].being_placed == True: #si la tourelle est en train d'être placée
							del turrets[-1] #on l'annule
							money += 50
						elif money >= 50: #sinon on créé une nouvelle tourelle
							turrets.append(createnewturret1(Turret))
							money -= 50
							
					elif money >= 50:#si il n'y a aucune tourelle on en créé une par défault
						turrets.append(createnewturret1(Turret))
						money -= 50
						
			elif pygame.mouse.get_pos()[0] <= turretbutton[1].x + turretbutton[1].width and pygame.mouse.get_pos()[0] >= turretbutton[1].x and pygame.mouse.get_pos()[1] <= turretbutton[1].y + turretbutton[1].height and pygame.mouse.get_pos()[1] >= turretbutton[1].y :
					if len(turrets) > 0: #si c'est le cas et que il y a déjà une tourelle
						if turrets[-1].being_placed == True: #si la tourelle est en train d'être placée
							del turrets[-1] #on l'annule
							money += 50
						elif money >= 50: #sinon on créé une nouvelle tourelle
							turrets.append(createnewfarm(Turret))
							money -= 50
							
					elif money >= 50:#si il n'y a aucune tourelle on en créé une par défault
						turrets.append(createnewfarm(Turret))
						money -= 50
											
			else: #si on clique autre part que sur un bouton
				if len(turrets) > 0:
					for location in locations: #on regarde si on a cliqué sur un emplacement
						if pygame.mouse.get_pos()[0] <= location.x + location.width and pygame.mouse.get_pos()[0] >= location.x and pygame.mouse.get_pos()[1] <= location.y + location.height and pygame.mouse.get_pos()[1] >= location.y and location.used == False:
							if turrets[-1].being_placed == True: #dans ce cas on place la tourelle dans l'emplacement
								turrets[-1].x = location.x
								turrets[-1].y = location.y
								turrets[-1].being_placed = False
								location.used = True
			####PROMOTION DU CHAMPION####
			if Champion.lvl == 1 and pygame.mouse.get_pos()[0] == Champion.x and pygame.mouse.get_pos()[1] == Champion.y:
				Champion.lvl += 1
				Champion.damage += 10
				Champion.ranged += 10
				Champion.life = Champion.life + (life- Champion.life) + 100
			if Champion.lvl == 2 and pygame.mouse.get_pos()[0] == Champion.x and pygame.mouse.get_pos()[1] == Champion.y:
				Champion.lvl += 1
				Champion.damage += 10
				Champion.ranged += 10
				Champion.life = Champion.life + (life- Champion.life) + 100
			if Champion.lvl == 3 and pygame.mouse.get_pos()[0] == Champion.x and pygame.mouse.get_pos()[1] == Champion.y:
				Champion.lvl += 1
				Champion.damage += 10
				Champion.ranged += 10
				Champion.life = Champion.life + (life- Champion.life) + 100
				
	#### TIR ET GAINS
	# TOURELLES
	for turret in turrets: # On prend chaques tourelles
		if turret.being_placed == False:
			money += turret.benefit #celles qui peuvent rapportent de l'argent
			if turret.locked == False: #on prend toutes les tourelles qui ne tirent pas
				for ennemy in range(len(ennemies)): # on prend tout les ennemis
					if (ennemies[ennemy].x-turret.x)**2 + (ennemies[ennemy].y-turret.y)**2 <= turret.ranged**2: #si un ennemi est dans sa ligne de mire alors :
						turret.lock = ennemy # on regarde quel ennemi elle vas viser
						turret.locked = True # elle ne pourra viser que un ennemi à la fois
						break #pas la peine de chercher plus d'ennemis, on break le "for ennemy in range(len(ennemies))
						
			elif turret.locked == True: #On prend toutes les tourelles qui tirent
				if (ennemies[turret.lock].x-turret.x)**2 + (ennemies[turret.lock].y-turret.y)**2 >= turret.ranged**2: #si l'ennemi qu'elles ciblent est trop loin:
					turret.locked = False #elles arrêtent de le cibler
				else:
					ennemies[turret.lock].life -= turret.damage
	# BASE
	money += base.benefit #celles qui peuvent rapportent de l'argent
	if base.locked == False: #on prend toutes les tourelles qui ne tirent pas
		for ennemy in range(len(ennemies)): # on prend tout les ennemis
			if (ennemies[ennemy].x-base.x)**2 + (ennemies[ennemy].y-base.y)**2 <= base.ranged**2: #si un ennemi est dans sa ligne de mire alors :
				base.lock = ennemy # on regarde quel ennemi elle vas viser
				base.locked = True # elle ne pourra viser que un ennemi à la fois
				break #pas la peine de chercher plus d'ennemis, on break le "for ennemy in range(len(ennemies))
				
	elif base.locked == True: #On prend toutes les tourelles qui tirent
		if (ennemies[base.lock].x-base.x)**2 + (ennemies[base.lock].y-base.y)**2 >= base.ranged**2: #si l'ennemi qu'elles ciblent est trop loin:
			base.locked = False #elles arrêtent de le cibler
		else:
			ennemies[base.lock].life -= base.damage
	
	### PLAÇAGE DE TOURELLES
	if len(turrets) > 0: #si il y a déjà une tourelle :
		if turrets[-1].being_placed == True: #si la dernière tourelle est en train d'être placée
			turrets[-1].x = pygame.mouse.get_pos()[0]-(turrets[-1].width//2) #et on fixe la tourelle
			turrets[-1].y = pygame.mouse.get_pos()[1]-(turrets[-1].height//2)
	
	### ENNEMIS
	for ennemy in ennemies: #pour chaques ennemis
		if ennemy.alive == True and ennemy.locked == False:#si ils sont en vie et pas en train de tirer
			if ennemy.life <= 0:
				ennemy.alive = False
			elif len(soldiers) >= 1:
				for soldier in range(len(soldiers)):
					if (soldiers[soldier].x-ennemy.x)**2 + (soldiers[soldier].y-ennemy.y)**2 <= ennemy.ranged**2: #si un ennemi est dans sa ligne de mire alors :
						ennemy.lock = soldier # on regarde quel ennemi elle vas viser
						ennemy.locked = True # elle ne pourra viser que un ennemi à la fois
						break #pas la peine de chercher plus d'ennemis, on break le "for ennemy in range(len(ennemies))
					else: # si aucun ennemis ne sont à portée, les unités avancent
						if ennemy.direction == "right":
							ennemy.x += ennemy.speed
						elif ennemy.direction == "left":
							ennemy.x -= ennemy.speed					
						elif ennemy.direction == "top":
							ennemy.y -= ennemy.speed
						elif ennemy.direction == "bottom":
							ennemy.y += ennemy.speed
			elif len(soldiers) == 0:
				print(ennemy.life)
				if (base.x-ennemy.x)**2 + (base.y-ennemy.y)**2 <= ennemy.ranged**2: #si la base est dans sa ligne de mire alors :
					ennemy.lock = "base" # il vise la base
					ennemy.locked = True # il ne pourra viser que un ennemi à la fois
				else:
					if ennemy.direction == "right":
						ennemy.x += ennemy.speed
					elif ennemy.direction == "left":
						ennemy.x -= ennemy.speed					
					elif ennemy.direction == "top":
						ennemy.y -= ennemy.speed
					elif ennemy.direction == "bottom":
						ennemy.y += ennemy.speed
		elif ennemy.locked == True: #On prend toutes les tourelles qui tirent
			if ennemy.lock == "base":
				base.life -= ennemy.damage
			elif (soldiers[ennemy.lock].x-ennemy.x)**2 + (soldiers[ennemy.lock].y-ennemy.y)**2 >= ennemy.ranged**2: #si l'ennemi qu'elles ciblent est trop loin:
				ennemy.locked = False #elles arrêtent de le cibler
			else:
				soldiers[ennemy.lock].life -= ennemy.damage

####################CHAMPION####################
	####DEPLACEMENTS####
	key = pygame.key.get_pressed()

	if key[pygame.K_LEFT]:
		Champion.x -= 1
	if key[pygame.K_RIGHT]:
		Champion.x += 1
	if key[pygame.K_UP]:
		Champion.y += 1
	if key[pygame.K_DOWN]:
		Champion.y -= 1
	####ATTAQUE ET TIR####
	"""
	for Champion in Champion:  # On prend chaques tourelles
		if Champion.being_placed == False:
			if Champion.locked == False:  # on prend toutes les tourelles qui ne tirent pas
				for ennemy in range(len(ennemies)):  # on prend tout les ennemis
					if (ennemies[ennemy].x - Champion.x) ** 2 + (ennemies[ennemy].y - Champion.y) ** 2 <= Champion.ranged ** 2:  # si un ennemi est dans sa ligne de mire alors :
						Champion.lock = ennemy  # on regarde quel ennemi elle vas viser
						Champion.locked = True  # elle ne pourra viser que un ennemi à la fois
						break  # pas la peine de chercher plus d'ennemis, on break le "for ennemy in range(len(ennemies))

			elif Champion.locked == True:  # On prend toutes les tourelles qui tirent
				if (ennemies[Champion.lock].x - Champion.x) ** 2 + (ennemies[Champion.lock].y - Champion.y) ** 2 >= Champion.ranged ** 2:  # si l'ennemi qu'elles ciblent est trop loin:
					Champion.locked = False  # elles arrêtent de le cibler
				else:
					ennemies[turret.lock].life -= Champion.damage"""







	TDGraphics.redrawGameWindow(window, turretbutton, turrets, locations, money, base, soldiers, ennemies, base.life) #on actualise en important la fonction

pygame.quit()
