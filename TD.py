#!/usr/bin/env python3
# coding:utf8

#################### INITIATIONS ET IMPORTATIONS ########################
import sys
print(sys.path)
import pygame
pygame.init()
import TDGraphics #on vas chercher du fichier graphique
import TDlevels #on importe le fichier des niveaux
import math
from random import randrange
from pygame.locals import *
### variable importantes
run = True 

proportion = TDlevels.proportion
WINDOWHEIGHT = 1000 * proportion #dimentions de la fenêtre
WINDOWWIDTH = 1000 * proportion
flags = DOUBLEBUF
window = TDGraphics.graphics(int(WINDOWWIDTH+130),int(WINDOWHEIGHT), flags) #on appelle la fonction pour dessiner la fenetre qui provient du fichier graphique
TDGraphics.scale(proportion)#on redimentionne les sprites
################### CLASSES #########################

class Turret(object): #on créé la classe des tourelles
	def __init__(self, x, y,color, clas, cost, ranged = 0,  benefit = 0, damage = 10, rate = 15, width = 64, height = 64):
		self.x = x
		self.y = y
		self.color = color
		self.ranged = ranged * proportion # la portée
		self.width = width * proportion
		self.height = height * proportion
		self.being_placed = True #si elle est en train d'être placée
		self.benefit = benefit # l'argent qu'elle rapporte
		self.locked = False #si elle cible une unité adverse
		self.lock = 0 # l'unité adverse qu'elle cible
		self.damage = damage
		self.selected = False #si elle est sélectionnée par le joueur
		self.rate = rate #sa cadence de tir (en frames) plus elle est elevée, plus elle est lente
		self.reload = rate #cela servira pour la cadence
		self.level = 1
		self.cost = cost
		self.clas = clas
		self.exists = True
		self.location = 0

class Button(object): #on créé la classe des boutons pour les tourelles
	def __init__(self, x, y, use, reloading = 0):
		self.x = x
		self.y = y
		self.width = 64  * proportion
		self.height = 64  * proportion
		self.use = use
		self.visible = True
		self.clicked = False
		self.reloading = reloading * 100 #dans le cas où le bouton aurait un temps de recharge
		self.reloaded = reloading * 100
	
class Location(object): #on créé la classe pour les emplacements de tourelles
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = 64  * proportion
		self.height = 64  * proportion
		self.used = False #si une tourelle est à un emplacement

class Allies(object):
	def __init__(self, x, y, life, damage, ranged, unit, armor = 1, width = 24, height = 24, speed= 1, rate = 20):
		self.x = x
		self.y = y
		self.life = float(life)
		self.max_life = life
		self.damage = damage
		self.ranged = ranged * proportion
		self.width = width * proportion
		self.height = height * proportion
		self.alive = True
		self.rate = rate 
		self.reload = rate 
		self.being_placed = True
		self.locked = False #si elle cible une unité adverse
		self.lock = 0 # l'unité adverse qu'elle cible
		self.armor = armor
		self.unit = unit

class Base(object):
	def __init__(self, x, y, life = 2000, damage = 45, benefit = 0.03, ranged= 150, width = 100, height = 100, rate = 130):
		self.x = x
		self.y = y
		self.life = life
		self.damage = damage
		self.benefit = benefit
		self.ranged = ranged * proportion
		self.width = width * proportion
		self.height = height * proportion
		self.locked = False
		self.lock = 0
		self.selected = False
		self.rate = rate 
		self.reload = rate 
		self.max_life = life

class Ennemy(object):
	def __init__(self, x, y, life, damage, direction, ranged, delay, typ, speed = 0.6, width = 24, height = 24, rate = 15, armor = 0):
		self.x = x
		self.y = y
		self.life = life
		self.damage = damage
		self.ranged = ranged * proportion
		self.direction = direction
		self.speed = speed * proportion # la vitesse en pixel/frames
		self.width = width * proportion
		self.height = height * proportion
		self.max_life = life
		self.alive = False
		self.locked = False
		self.lock = 0
		self.rate = rate 
		self.reload = rate 
		self.armor = armor #réduction de dégats
		self.delay = delay
		self.typ = typ #le type d'ennemi
		self.walk = 0 #pour l'animation de marche

class Plane(object):
	def __init__(self, x, y, life, damage, delay, typ, speed = 1.5, width = 60, height = 60, rate = 300, armor = 0):
		self.x = x
		self.y = y
		self.life = life
		self.damage = damage
		self.speed = speed * proportion # la vitesse en pixel/frames
		self.max_speed = speed*proportion
		self.width = width * proportion
		self.height = height * proportion
		self.max_life = life
		self.alive = False
		self.locked = False
		self.lock = 0
		self.rate = rate 
		self.reload = rate 
		self.armor = armor #réduction de dégats
		self.delay = delay
		self.direction = str()
		self.movementx = 0.0
		self.movementy = 0.0
		self.walk = 0 #pour l'animation de vol
		self.bombing = []
		self.typ = typ
		
class Mortar(object):
	def __init__(self, x, y, distancex, distancey, damage, lock , radius = 7):
		self.x = float(x)
		self.y = float(y)
		self.radius = int(radius * proportion)
		self.progress = 60
		self.distancex = float(distancex) #la distance horizontale entre la tourelle et l'ennemi
		self.distancey =float(distancey) #la distance verticale
		self.direction = 0
		self.damage = damage
		self.lock = lock

class Road(object):
	def __init__(self, x, y, width, height, direction):
		self.x = x
		self.y = y
		self.width = width 
		self.height = height 
		self.direction = direction
##################### FONCTIONS #########################
def createnewturret1(Turret):
	return(Turret(
	pygame.mouse.get_pos()[0]-(turretWidth//2), 
	pygame.mouse.get_pos()[1]-(turretHeight//2),
	(0,122,15), 1, 50, 140, 0, 10, 15, turretWidth, turretHeight))

def createnewfarm(Turret):
	return(Turret(
	pygame.mouse.get_pos()[0]-(turretWidth//2), 
	pygame.mouse.get_pos()[1]-(turretHeight//2),
	(239,209,88), 2, 50,0, 0.02, 0, 0, turretWidth, turretHeight))

def createnewsniper(Turret):
	return(Turret(
	pygame.mouse.get_pos()[0]-(turretWidth//2), 
	pygame.mouse.get_pos()[1]-(turretHeight//2),
	(70,160,70), 3, 75, 240, 0, 25, 55, turretWidth, turretHeight))

def createnewsoldier1(Allies):
	return(Allies(
	pygame.mouse.get_pos()[0]-(12*proportion), 
	pygame.mouse.get_pos()[1]-(12*proportion),
	50, 5, 130, 1))

def createnewwall(Allies):
	return(Allies(
	pygame.mouse.get_pos()[0]-(12*proportion), 
	pygame.mouse.get_pos()[1]-(12*proportion),
	200, 0, 0, 2, 3))
	
def createnewennemy(Ennemy, direction, placement, delay, ennemy_type):
	if ennemy_type == 0:#pour éviter les bugs
		return(Ennemy(0,0, 0, 0, 0, 0,0, 0)) 
	if ennemy_type == 1:
		return(Ennemy(placement[0],placement[1], 50, 5, direction, 100,delay, 1)) 
	if ennemy_type == 2:
		return(Ennemy(placement[0],placement[1], 200, 25, direction, 110,delay,2, 0.4, 32, 32, 50, 2)) 
		
def createnewplane(Plane, x, y, delay, typ):
	if typ == 1:
		return(Plane(x,y, 250, 100,delay, typ))


def createnewroad(Road, x, y, width, height,direction):
	return(Road(x, y, width, height, direction))

def MortarShot(Mortar, ennemies):
	if Mortar.direction < 2:
		Mortar.x += Mortar.distancex/120 #il parcourt la distance en 120 frames
		
	if Mortar.progress == Mortar.direction and Mortar.direction == 0: #il y a quatre partie, la 0 où il monte, la 1 ou il descend, la 2 et 3 où il explose et la 4 ou il disparait
		Mortar.direction = 1
		
	elif Mortar.progress == 60 and Mortar.direction == 1:
		Mortar.direction = 2 #la partie 2 signifie que il a fini donc il explose puis disparait
		Mortar.progress = 0
		
	elif Mortar.direction == 3 and Mortar.progress == 10: #transition vers la disparition
		Mortar.direction = 4
		
	elif Mortar.direction == 0: #quand il monte
		Mortar.y -= (Mortar.progress+(Mortar.distancey//24))/15 
		Mortar.progress -= 1
		
	elif Mortar.direction == 1 : #quand il descend
		Mortar.y += (Mortar.progress+(Mortar.distancey/24))/15 - Mortar.distancey/65
		Mortar.progress += 1
		
	elif Mortar.direction == 2:#quand il explose
		for ennemy in ennemies :
			if ennemy.alive == True:
				if ((ennemy.y + ennemy.height//2)-Mortar.y)**2 + (((ennemy.x + (ennemy.width//2))-Mortar.x))**2 <= (Mortar.radius*3+(ennemy.width//2))**2: #le rayon de l'explosion est trois fois plus grand que le rayon de boulet, et même si il ne touche pas le centre de l'ennemi il doit pouvoir le blesser
					ennemy.life -= Mortar.damage-ennemy.armor
		Mortar.direction = 3
	elif Mortar.direction == 3:
		Mortar.progress += 1

		
	return(Mortar) 	#cette fonction a été faite avec beaucoup de tatonnement mais surtout beaucoup de temps 
					#donc désolé pour le manque d'expliquation, mais aucune aide n'a été trouvée sur internet pour écrire cette fonction
	
##################### VARIABLES #########################

turretbutton = [] #La liste de tout les boutons
turrets = [] #la liste de toutes les tourelles 
locations = [] #la liste de tout les emplacements
ennemies = [] # la liste de tout les ennemis
ennemies.append(createnewennemy(Ennemy, 0,0, 0, 0))
ennemies[-1].alive = False #cela sert à éviter les bugs

mortars = [] #la liste de tout les tirs de mortier
roads = [] #la liste de toutes les routes
flying = [] #la liste de tout les ennemis volants

flying.append(createnewennemy(Ennemy, 0,0, 0, 0))
flying[-1].alive = False #cela sert à éviter les bugs
base = Base((WINDOWWIDTH)//2 - 50 * proportion + 65, WINDOWHEIGHT//2 -50 * proportion, 2000, 45, 0.05, 200, 100, 100)
soldiers = []
#on créé tout les boutons
turretbutton.append(Button(0, WINDOWHEIGHT -64, "turret")) #on ajoute des boutons (premier bouton, tourelle simple)
turretbutton.append(Button(0, WINDOWHEIGHT -129, "farm"))#deuxième bouton ferme
turretbutton.append(Button(0,  WINDOWHEIGHT -195, "sniper"))#bouton de sniper
turretbutton.append(Button(0, 170, "upgrade"))# avant dernier bouton destruction
turretbutton[-1].visible = False #on met ces deux boutons en invisible
turretbutton.append(Button(0, 105, "destroy"))#dernier bouton amélioration
turretbutton[-1].visible = False
unitbutton = []
unitbutton.append(Button(WINDOWWIDTH + 66, WINDOWHEIGHT - 64, "units", 14))
unitbutton.append(Button(WINDOWWIDTH + 66, WINDOWHEIGHT - 170, "wall", 10))

selected = int() #la tourelle sélectionnée

#cout des tourelles
costturret1 = 50
costfarm = 50
costsniper = 75
wave = 0
money = float(100)
turretWidth = 64
turretHeight = 64

moneypersecond = 0#ces deux variables servent à l'équilibrage de l'argent
moneytime = 0

level1 = TDlevels.level1()
for i in range(len(level1[3])): #on créé les routes
	roads.append(createnewroad(Road, level1[3][i][1], level1[3][i][2], level1[3][i][3], level1[3][i][4], level1[3][i][0]))
	
for i in range(len(level1[1][0])): #on créé les ennemis
	ennemies.append(createnewennemy(Ennemy, level1[1][0][i][0],level1[1][0][i][1], level1[1][0][i][2], level1[1][0][i][3]))
for i in range(len(level1[2][0])): #on créé les ennemis aériens
	flying.append(createnewplane(Plane, level1[2][0][i][0],level1[2][0][i][1], level1[2][0][i][2], level1[2][0][i][3]))
	
for i in range(len(level1[0])): #on créé les emplacements
	locations.append(Location(level1[0][i][0]-32,level1[0][i][1] -32))
time = 0 #variable servant à chronometrer la partie
#################### MAIN LOOP ######################


while run: # tant que on joue
	pygame.time.delay(10) #il capte une information toutes les x milisecondes
	time += 1 #avancée du temps
			
	for event in pygame.event.get(): # si on appuie sur une touche
		### QUITTER
		if event.type == pygame.QUIT:#si on quitte
			run = False
		if event.type == pygame.MOUSEBUTTONUP: #si on clique quelque part
			for button in turretbutton:
				button.clicked = False
			
			#### BOUTONS
			#tourelle
			if pygame.mouse.get_pos()[0] <= turretbutton[0].x + turretbutton[0].width and pygame.mouse.get_pos()[0] >= turretbutton[0].x and pygame.mouse.get_pos()[1] <= turretbutton[0].y + turretbutton[0].height and pygame.mouse.get_pos()[1] >= turretbutton[0].y :
					if len(turrets) > 0: #si c'est le cas et que il y a déjà une tourelle
						if turrets[-1].being_placed == True: #si la tourelle est en train d'être placée
							del turrets[-1] #on l'annule
							money += costturret1
						elif money >= costturret1: #sinon on créé une nouvelle tourelle
							turrets.append(createnewturret1(Turret))
							money -= costturret1
							
					elif money >= costturret1:#si il n'y a aucune tourelle on en créé une par défault
						turrets.append(createnewturret1(Turret))
						money -= costturret1
			#ferme
			elif pygame.mouse.get_pos()[0] <= turretbutton[1].x + turretbutton[1].width and pygame.mouse.get_pos()[0] >= turretbutton[1].x and pygame.mouse.get_pos()[1] <= turretbutton[1].y + turretbutton[1].height and pygame.mouse.get_pos()[1] >= turretbutton[1].y :
					if len(turrets) > 0: #si on ré appuie sur un bouton alors que on a déjà une tourelle sur le terrain
						if turrets[-1].being_placed == True: #si la tourelle est en train d'être placée
							del turrets[-1] #on l'annule
							money += costfarm
						elif money >= costfarm: #sinon on créé une nouvelle tourelle
							turrets.append(createnewfarm(Turret))
							money -= costfarm
							
					elif money >= costfarm:#si il n'y a aucune tourelle on en créé une par défault
						turrets.append(createnewfarm(Turret))
						money -= costfarm
			#sniper
			elif pygame.mouse.get_pos()[0] <= turretbutton[2].x + turretbutton[2].width and pygame.mouse.get_pos()[0] >= turretbutton[2].x and pygame.mouse.get_pos()[1] <= turretbutton[2].y + turretbutton[2].height and pygame.mouse.get_pos()[1] >= turretbutton[2].y :
					if len(turrets) > 0: #si on ré appuie sur un bouton alors que on a déjà une tourelle sur le terrain
						if turrets[-1].being_placed == True: #si la tourelle est en train d'être placée
							del turrets[-1] #on l'annule
							money += costsniper
						elif money >= costsniper: #sinon on créé une nouvelle tourelle
							turrets.append(createnewsniper(Turret))
							money -= costsniper
							
					elif money >= costsniper:#si il n'y a aucune tourelle on en créé une par défault
						turrets.append(createnewsniper(Turret))
						money -= costsniper
			#unités
			elif pygame.mouse.get_pos()[0] <= unitbutton[0].x + unitbutton[0].width and pygame.mouse.get_pos()[0] >= unitbutton[0].x and pygame.mouse.get_pos()[1] <= unitbutton[0].y + unitbutton[0].height and pygame.mouse.get_pos()[1] >= unitbutton[0].y :
					if len(soldiers) > 0: #si on appuie sur un bouton alors que il y a déjà des unités sur le terrain
						if soldiers[-1].being_placed == True: #si ces unités sont en train d'être placées
							del soldiers[-1] #on les annules
							unitbutton[0].reloaded = unitbutton[0].reloading
						elif unitbutton[0].reloaded == unitbutton[0].reloading: #sinon on les créé 
							soldiers.append(createnewsoldier1(Allies))
							unitbutton[0].reloaded = 0
							
					elif unitbutton[0].reloaded == unitbutton[0].reloading:#si il n'y a aucune unité on en créé une par défault
						soldiers.append(createnewsoldier1(Allies))
						unitbutton[0].reloaded = 0
			#wall
			elif pygame.mouse.get_pos()[0] <= unitbutton[1].x + unitbutton[1].width and pygame.mouse.get_pos()[0] >= unitbutton[1].x and pygame.mouse.get_pos()[1] <= unitbutton[1].y + unitbutton[1].height and pygame.mouse.get_pos()[1] >= unitbutton[1].y :
					if len(soldiers) > 0: #si on appuie sur un bouton alors que il y a déjà des unités sur le terrain
						if soldiers[-1].being_placed == True: #si ces unités sont en train d'être placées
							del soldiers[-1] #on les annules
							unitbutton[1].reloaded = unitbutton[1].reloading
						elif unitbutton[1].reloaded == unitbutton[1].reloading: #sinon on les créé 
							soldiers.append(createnewwall(Allies))
							unitbutton[1].reloaded = 0
							
					elif unitbutton[1].reloaded == unitbutton[1].reloading:#si il n'y a aucune unité on en créé une par défault
						soldiers.append(createnewwall(Allies))
						unitbutton[1].reloaded = 0
			
			else: #si on clique autre part que sur un bouton
				if len(turrets) > 0: #les len() servent à éviter les "index out of range"
					if turrets[-1].being_placed == True: #dans ce cas on place la tourelle dans l'emplacement
						for location in range(len(locations)): #on regarde si on a cliqué sur un emplacement
							if pygame.mouse.get_pos()[0] <= locations[location].x + locations[location].width and pygame.mouse.get_pos()[0] >= locations[location].x and pygame.mouse.get_pos()[1] <= locations[location].y + locations[location].height and pygame.mouse.get_pos()[1] >= locations[location].y and locations[location].used == False:
								turrets[-1].x = locations[location].x
								turrets[-1].y = locations[location].y
								turrets[-1].being_placed = False
								turrets[-1].location = location
								locations[location].used = True
					#### SELECTIONNER UNE TOURELLE PRÉ-EXISTANTE ET L'AMÉLIORER
					elif turrets[-1].being_placed == False:
						for turret in range(len(turrets)):
							if turrets[turret].exists == True :
								if turrets[turret].selected == True :
									if pygame.mouse.get_pos()[0] <= turretbutton[-1].x + turretbutton[-1].width and pygame.mouse.get_pos()[0] >= turretbutton[-1].x and pygame.mouse.get_pos()[1] <= turretbutton[-1].y + turretbutton[-1].height and pygame.mouse.get_pos()[1] >= turretbutton[-1].y:
										money += turrets[turret].cost//2
										turrets[turret].exists = False
										locations[turrets[turret].location].used = False
										turrets[turret].selected = False
										turretbutton[-1].visible = False
										turretbutton[-2].visible = False
									elif pygame.mouse.get_pos()[0] <= turretbutton[-2].x + turretbutton[-2].width and pygame.mouse.get_pos()[0] >= turretbutton[-2].x and pygame.mouse.get_pos()[1] <= turretbutton[-2].y + turretbutton[-2].height and pygame.mouse.get_pos()[1] >= turretbutton[-2].y:
										if turrets[turret].clas == 1:
											if turrets[turret].level == 1 and money >= 100:
												turrets[turret].damage += 5
												turrets[turret].ranged += 80
												turrets[turret].level += 1
												turrets[turret].cost += 100
												turrets[turret].rate -= 2
												money -= 100
										elif turrets[turret].clas == 2:
											if turrets[turret].level == 1 and money >= 80:
												turrets[turret].benefit += 0.02
												money -= 80
												turrets[turret].level += 1
												turrets[turret].cost += 80
										elif turrets[turret].clas == 3:
											if turrets[turret].level == 1 and money >= 5:
												turrets[turret].damage += 15
												turrets[turret].ranged += 100
												turrets[turret].level += 1
												turrets[turret].cost += 125
												turrets[turret].rate -= 5
												money -= 125
									else:
										selected = None
										turrets[turret].selected = False
										turretbutton[-1].visible = False
										turretbutton[-2].visible = False
								elif turrets[turret].selected == False and turrets[turret].being_placed == False:
									if pygame.mouse.get_pos()[0] <= turrets[turret].x + turrets[turret].width and pygame.mouse.get_pos()[0] >= turrets[turret].x and pygame.mouse.get_pos()[1] <= turrets[turret].y + turrets[turret].height and pygame.mouse.get_pos()[1] >= turrets[turret].y:
										selected = turret
										turrets[turret].selected = True
										turretbutton[-1].visible = True
										turretbutton[-2].visible = True
										
				## placement des soldats
				if len(soldiers) > 0:
					if soldiers[-1].being_placed == True:
						for road in range(len(roads)):
							if soldiers[-1].unit == 1:
								if pygame.mouse.get_pos()[0] <= roads[road].x + roads[road].width and pygame.mouse.get_pos()[0] >= roads[road].x and pygame.mouse.get_pos()[1] <= roads[road].y + roads[road].height and pygame.mouse.get_pos()[1] >= roads[road].y:
									if pygame.mouse.get_pos()[0] > base.x + base.width or pygame.mouse.get_pos()[0] < base.x or pygame.mouse.get_pos()[1] > base.y + base.height or pygame.mouse.get_pos()[1] < base.y: 
										if roads[road].direction == "right" or roads[road].direction == "left":
											soldiers[-1].being_placed = False
											soldiers[-1].y = roads[road].y
											soldiers.append(createnewsoldier1(Allies))
											soldiers[-1].being_placed = False
											soldiers[-1].y = roads[road].y + 20 * proportion
											soldiers.append(createnewsoldier1(Allies))
											soldiers[-1].being_placed = False
											soldiers[-1].y = roads[road].y + 40 * proportion
											soldiers.append(createnewsoldier1(Allies))
											soldiers[-1].being_placed = False
											soldiers[-1].y = roads[road].y + 60 * proportion
										elif roads[road].direction == "top" or roads[road].direction == "bottom":
											soldiers[-1].being_placed = False
											soldiers[-1].x = roads[road].x
											soldiers.append(createnewsoldier1(Allies))
											soldiers[-1].being_placed = False
											soldiers[-1].x = roads[road].x + 20 * proportion
											soldiers.append(createnewsoldier1(Allies))
											soldiers[-1].being_placed = False
											soldiers[-1].x = roads[road].x + 40 * proportion
											soldiers.append(createnewsoldier1(Allies))
											soldiers[-1].being_placed = False
											soldiers[-1].x = roads[road].x + 60 * proportion
				## placement des MUUUURS BUILD A WALL
							if soldiers[-1].unit == 2:
								if pygame.mouse.get_pos()[0] <= roads[road].x + roads[road].width and pygame.mouse.get_pos()[0] >= roads[road].x and pygame.mouse.get_pos()[1] <= roads[road].y + roads[road].height and pygame.mouse.get_pos()[1] >= roads[road].y:
									if pygame.mouse.get_pos()[0] > base.x + base.width or pygame.mouse.get_pos()[0] < base.x or pygame.mouse.get_pos()[1] > base.y + base.height or pygame.mouse.get_pos()[1] < base.y: 
										if roads[road].direction == "right" or roads[road].direction == "left":
											soldiers[-1].being_placed = False
											soldiers[-1].y = roads[road].y
											soldiers[-1].height = roads[road].height
										elif roads[road].direction == "top" or roads[road].direction == "bottom":
											soldiers[-1].being_placed = False
											soldiers[-1].x = roads[road].x
											soldiers[-1].width = roads[road].width
								
								
			### SELECTIONNER LA BASE
			if pygame.mouse.get_pos()[0] <= base.x + base.width and pygame.mouse.get_pos()[0] >= base.x and pygame.mouse.get_pos()[1] <= base.y + base.height and pygame.mouse.get_pos()[1] >= base.y:
				if base.selected == False:
					base.selected = True
				elif base.selected == True:
					base.selected = False
			else:
				base.selected = False
				
		# pour l'animation de clickage sur un bouton
		if event.type == pygame.MOUSEBUTTONDOWN: 
			for button in turretbutton:
				if pygame.mouse.get_pos()[0] <= button.x + button.width and pygame.mouse.get_pos()[0] >= button.x and pygame.mouse.get_pos()[1] <= button.y + button.height and pygame.mouse.get_pos()[1] >= button.y :
					button.clicked = True
	
	#### TIR ET GAINS DES TOURELLES
	for turret in turrets: # On prend chaques tourelles
		if turret.exists == True:
			if turret.being_placed == False:
				money += turret.benefit #celles qui peuvent rapportent de l'argent
				moneypersecond += turret.benefit
				if turret.locked == False: #on prend toutes les tourelles qui ne tirent pas
					if turret.clas == 3:
						for ennemy in range(len(flying)):
							if ((flying[ennemy].y + flying[ennemy].height//2)-(turret.y + turret.width//2))**2 + (((flying[ennemy].x + (flying[ennemy].width//2))-(turret.x+(turret.width//2))))**2 <= turret.ranged**2 and flying[ennemy].alive == True: #si un ennemi est dans sa ligne de mire alors :
								turret.lock = ennemy+len(ennemies) # on regarde quel ennemi elle vas viser
								turret.locked = True # elle ne pourra viser que un ennemi à la fois
								break #pas la peine de chercher plus d'ennemis, on break le "for ennemy in range(len(ennemies))
							
					if turret.locked == False:
						for ennemy in range(len(ennemies)): # on prend tout les ennemis
							if ((ennemies[ennemy].y + ennemies[ennemy].height//2)-(turret.y + turret.width//2))**2 + (((ennemies[ennemy].x + (ennemies[ennemy].width//2))-(turret.x+(turret.width//2))))**2 <= turret.ranged**2 and ennemies[ennemy].alive == True: #si un ennemi est dans sa ligne de mire alors :
								turret.lock = ennemy # on regarde quel ennemi elle vas viser
								turret.locked = True # elle ne pourra viser que un ennemi à la fois
								break #pas la peine de chercher plus d'ennemis, on break le "for ennemy in range(len(ennemies))
							
				elif turret.locked == True: #On prend toutes les tourelles qui tirent
					try:
						if turret.lock < len(ennemies):
							if ((ennemies[turret.lock].y + ennemies[turret.lock].height//2)-(turret.y + turret.width//2))**2 + (((ennemies[turret.lock].x + (ennemies[turret.lock].width//2))-(turret.x+(turret.width//2))))**2 >= turret.ranged**2 or ennemies[turret.lock].alive == False: #si l'ennemi qu'elles ciblent est trop loin:
								turret.locked = False #elles arrêtent de le cibler
							elif turret.reload >= turret.rate and turret.locked == True:
								ennemies[turret.lock].life -= (turret.damage-ennemies[turret.lock].armor)
								turret.reload = 0
						elif turret.lock >= len(ennemies): #ici je me suis servi du fait que si la tourelle vise une unité aérienne, alors sa variable lock (sensée être le nombre de l'unité visée dans la liste, est au dessus de la longueur de ennemies[] donc l'ordinateur en déduit que la tourelle vise en l'air
							if ((flying[turret.lock-(len(ennemies))].y + flying[turret.lock-(len(ennemies))].height//2)-(turret.y + turret.width//2))**2 + (((flying[turret.lock-(len(ennemies))].x + (flying[turret.lock-(len(ennemies))].width//2))-(turret.x+(turret.width//2))))**2 >= turret.ranged**2 or flying[turret.lock-(len(ennemies))].alive == False: #si l'ennemi qu'elles ciblent est trop loin:
								turret.locked = False #elles arrêtent de le cibler
							elif turret.reload >= turret.rate and turret.locked == True:
								flying[turret.lock-(len(ennemies))].life -= (turret.damage-flying[turret.lock-(len(ennemies))].armor)
								turret.reload = 0
						if turret.reload < turret.rate:
							turret.reload += 1
					except IndexError:
					#	print("wesh wesh cannapesh")
						turret.locked = False #elles arrêtent de le cibler
			
			elif turrets[-1].being_placed == True: #si la dernière tourelle est en train d'être placée
				turrets[-1].x = pygame.mouse.get_pos()[0]-(turrets[-1].width//2) #et on fixe la tourelle
				turrets[-1].y = pygame.mouse.get_pos()[1]-(turrets[-1].height//2)
		
	# BASE
	money += base.benefit #la base rapporte de l'agent
	moneypersecond += base.benefit
	if base.locked == False: #on prend toutes les tourelles qui ne tirent pas
		for ennemy in range(len(ennemies)): # on prend tout les ennemis
			if ((ennemies[ennemy].y + ennemies[ennemy].height//2)-(base.y + base.width//2))**2 + (((ennemies[ennemy].x + (ennemies[ennemy].width//2))-(base.x+(base.width//2))))**2 <= base.ranged**2 and ennemies[ennemy].alive == True: #si un ennemi est dans sa ligne de mire alors :
				base.lock = ennemy # on regarde quel ennemi elle vas viser
				base.locked = True # elle ne pourra viser que un ennemi à la fois
				break #pas la peine de chercher plus d'ennemis, on break le "for ennemy in range(len(ennemies))
				
	elif base.locked == True: #On prend toutes les tourelles qui tirent
		if ((ennemies[base.lock].y + ennemies[base.lock].height//2)-(base.y + base.width//2))**2 + (((ennemies[base.lock].x + (ennemies[base.lock].width//2))-(base.x+(base.width//2))))**2 >= base.ranged**2 or ennemies[base.lock].alive == False: #si l'ennemi qu'elles ciblent est trop loin:
			base.locked = False #elles arrêtent de le cibler
		elif base.reload == base.rate : #cela sert à ce que le mortier touche sa cible au lieu de tirer derrière
			if ennemies[base.lock].direction == "right":
				if ennemies[base.lock].locked == True:
					mortars.append(Mortar((base.x + base.width//2), (base.y + base.height//2), ((ennemies[base.lock].x + (ennemies[base.lock].width//2))-(base.x + base.width//2)), (base.y + base.height//2)-(ennemies[base.lock].y + (ennemies[base.lock].height//2)), base.damage, base.lock))
				elif ennemies[base.lock].x + ennemies[base.lock].speed * 120 >= base.x+base.width//2 - ennemies[base.lock].ranged:
					mortars.append(Mortar((base.x + base.width//2), (base.y + base.height//2), -1 * ennemies[base.lock].ranged, (base.y + base.height//2)-(ennemies[base.lock].y + (ennemies[base.lock].height//2)), base.damage, base.lock))
				else:
					mortars.append(Mortar((base.x + base.width//2), (base.y + base.height//2), ((ennemies[base.lock].x + (ennemies[base.lock].width//2))-(base.x + base.width//2)) + ennemies[base.lock].speed * 120 , (base.y + base.height//2)-(ennemies[base.lock].y + (ennemies[base.lock].height//2)), base.damage, base.lock))
			elif ennemies[base.lock].direction == "left":
				if ennemies[base.lock].locked == True:
					mortars.append(Mortar((base.x + base.width//2), (base.y + base.height//2), ((ennemies[base.lock].x + (ennemies[base.lock].width//2))-(base.x + base.width//2)), (base.y + base.height//2)-(ennemies[base.lock].y + (ennemies[base.lock].height//2)), base.damage, base.lock))
				elif ennemies[base.lock].x - ennemies[base.lock].speed * 120 <= base.x+base.width//2 + ennemies[base.lock].ranged:
					mortars.append(Mortar((base.x + base.width//2), (base.y + base.height//2), ennemies[base.lock].ranged, (base.y + base.height//2)-(ennemies[base.lock].y + (ennemies[base.lock].height//2)), base.damage, base.lock))
				else:
					mortars.append(Mortar((base.x + base.width//2), (base.y + base.height//2), ((ennemies[base.lock].x + (ennemies[base.lock].width//2))-(base.x + base.width//2)) - ennemies[base.lock].speed * 120 , (base.y + base.height//2)-(ennemies[base.lock].y + (ennemies[base.lock].height//2)), base.damage, base.lock))
			elif ennemies[base.lock].direction == "top":
				if ennemies[base.lock].locked == True:
					mortars.append(Mortar((base.x + base.width//2), (base.y + base.height//2), ((ennemies[base.lock].x + (ennemies[base.lock].width//2))-(base.x + base.width//2)), (base.y + base.height//2)-(ennemies[base.lock].y + (ennemies[base.lock].height//2)), base.damage, base.lock))
				elif ennemies[base.lock].y + ennemies[base.lock].speed * 120 >= base.y+base.height//2 + ennemies[base.lock].ranged:
					mortars.append(Mortar((base.x + base.width//2), (base.y + base.height//2), ((ennemies[base.lock].x + (ennemies[base.lock].width//2))-(base.x + base.width//2)), -1 *ennemies[base.lock].ranged - 20, base.damage, base.lock))
				else:
					mortars.append(Mortar((base.x + base.width//2), (base.y + base.height//2), ((ennemies[base.lock].x + (ennemies[base.lock].width//2))-(base.x + base.width//2)), (base.y + base.height//2)-(ennemies[base.lock].y + (ennemies[base.lock].height//2)) - ennemies[base.lock].speed * 120, base.damage, base.lock))
			elif ennemies[base.lock].direction == "bottom":
				if ennemies[base.lock].locked == True:
					mortars.append(Mortar((base.x + base.width//2), (base.y + base.height//2), ((ennemies[base.lock].x + (ennemies[base.lock].width//2))-(base.x + base.width//2)), (base.y + base.height//2)-(ennemies[base.lock].y + (ennemies[base.lock].height//2)) , base.damage, base.lock))
				elif ennemies[base.lock].y - ennemies[base.lock].speed * 120 <= base.y+base.height//2 + ennemies[base.lock].ranged:
					mortars.append(Mortar((base.x + base.width//2), (base.y + base.height//2), ((ennemies[base.lock].x + (ennemies[base.lock].width//2))-(base.x + base.width//2)), ennemies[base.lock].ranged, base.damage, base.lock))
				else:
					mortars.append(Mortar((base.x + base.width//2), (base.y + base.height//2), ((ennemies[base.lock].x + (ennemies[base.lock].width//2))-(base.x + base.width//2)), (base.y + base.height//2)-(ennemies[base.lock].y + (ennemies[base.lock].height//2)) + ennemies[base.lock].speed * 120, base.damage, base.lock))
			base.reload = 0
		elif base.reload < base.rate:
			base.reload += 1
	
	if unitbutton[0].reloaded < unitbutton[0].reloading :
		unitbutton[0].reloaded += 1
	if unitbutton[1].reloaded < unitbutton[1].reloading :
		unitbutton[1].reloaded += 1
	# Unités alliées
	for unit in soldiers:
		if unit.alive == True:
			if unit.life > 0:
				if unit.being_placed == False :
					if unit.unit == 1:
						if unit.locked == False: #on prend toutes les tourelles qui ne tirent pas
							for ennemy in range(len(ennemies)): # on prend tout les ennemis
								if ((ennemies[ennemy].y + ennemies[ennemy].height//2)-(unit.y + unit.width//2))**2 + (((ennemies[ennemy].x + (ennemies[ennemy].width//2))-(unit.x+(unit.width//2))))**2 <= unit.ranged**2 and ennemies[ennemy].alive == True: #si un ennemi est dans sa ligne de mire alors :
									unit.lock = ennemy # on regarde quel ennemi elle vas viser
									unit.locked = True # elle ne pourra viser que un ennemi à la fois
									break #pas la peine de chercher plus d'ennemis, on break le "for ennemy in range(len(ennemies))
									
						elif unit.locked == True: #On prend toutes les tourelles qui tirent
							if ((ennemies[unit.lock].y + ennemies[unit.lock].height//2)-(unit.y + unit.width//2))**2 + (((ennemies[unit.lock].x + (ennemies[unit.lock].width//2))-(unit.x+(unit.width//2))))**2 >= unit.ranged**2 or ennemies[unit.lock].alive == False: #si l'ennemi qu'elles ciblent est trop loin:
								unit.locked = False #elles arrêtent de le cibler
							elif unit.reload == unit.rate :
								ennemies[unit.lock].life -= (unit.damage-ennemies[unit.lock].armor)
								unit.reload = 0
							elif unit.reload < unit.rate:
								unit.reload += 1
				elif unit.being_placed == True:
					soldiers[-1].x = pygame.mouse.get_pos()[0]-(soldiers[-1].width//2) 
					soldiers[-1].y = pygame.mouse.get_pos()[1]-(soldiers[-1].height//2)
			elif unit.life <= 0:
				unit.alive = False
	
	### ENNEMIS
	# AU SOL
	for ennemy in ennemies: #pour chaques ennemis
		if ennemy.delay*20 == time:
			ennemy.alive = True
		if ennemy.alive == True:
			if ennemy.life <= 0:
				ennemy.alive = False
			if ennemy.locked == False:#si ils sont en vie et pas en train de tirer
				if ennemy.typ == 1:#animation de marche
					if ennemy.walk == 79:
						ennemy.walk = 0
					else:
						ennemy.walk += 1
				if ennemy.life >= 0:
					for soldier in range(len(soldiers)):
						if ((soldiers[soldier].y + soldiers[soldier].height//2)-(ennemy.y + ennemy.width//2))**2 + (((soldiers[soldier].x + (soldiers[soldier].width//2))-(ennemy.x+(ennemy.width//2))))**2 <= ennemy.ranged**2 and soldiers[soldier].alive == True and soldiers[soldier].being_placed == False: #si un ennemi est dans sa ligne de mire alors :
							ennemy.lock = soldier # on regarde quel ennemi elle vas viser
							ennemy.locked = True # elle ne pourra viser que un ennemi à la fois
							break #pas la peine de chercher plus d'ennemis, on break le "for ennemy in range(len(ennemies))
							
					if ennemy.locked == False and((base.x + (base.width//2))-(ennemy.x + (ennemy.width//2)))**2 + ((base.y + (base.height//2))-(ennemy.y + (ennemy.height//2)))**2 <= ennemy.ranged**2: #si la base est dans sa ligne de mire alors :
						ennemy.lock = "base" # il vise la base
						ennemy.locked = True # il ne pourra viser que un ennemi à la fois
						
					else: # si aucun ennemis ne sont à portée, les unités avancent
						for road in roads :
							if ennemy.x + ennemy.width//2 < road.x + road.width and ennemy.x + ennemy.width//2 > road.x and ennemy.y + ennemy.height//2 < road.y + road.height and ennemy.y + ennemy.height//2 > road.y :
								if road.direction == "right":
									ennemy.x += ennemy.speed
								elif road.direction == "left":
									ennemy.x -= ennemy.speed					
								elif road.direction == "top":
									ennemy.y -= ennemy.speed
								elif road.direction == "bottom":
									ennemy.y += ennemy.speed

			elif ennemy.locked == True: #On prend tout les ennemis qui tirent
				if ennemy.rate > ennemy.reload:
					ennemy.reload += 1
				elif ennemy.lock == "base" and ennemy.rate == ennemy.reload: #si ils sont à portée de la base, ils tirent
					base.life -= ennemy.damage
					ennemy.reload = 0
				elif (((soldiers[ennemy.lock].x + (soldiers[ennemy.lock].width//2))
					-(ennemy.x + (ennemy.width//2)))**2 + ((soldiers[ennemy.lock].y 
					+ (soldiers[ennemy.lock].height//2))-(ennemy.y + (ennemy.height//2)))**2
					>= ennemy.ranged**2 or soldiers[ennemy.lock].alive == False): #si l'ennemi qu'ils ciblent est trop loin:
					ennemy.locked = False #ils arrêtent de le cibler
				else:
					soldiers[ennemy.lock].life -= (ennemy.damage-soldiers[ennemy.lock].armor)
					ennemy.reload = 0
	# AÉRIENS
	for ennemy in flying:
		if ennemy.delay*20 == time:
			ennemy.alive = True
		if ennemy.alive == True:
			if ennemy.life <= 0:
				ennemy.alive = False
			else:	
				if ennemy.walk == 14:
					ennemy.walk = 0
				else:
					ennemy.walk += 1
				if math.sqrt(((base.x+base.width//2)-(ennemy.x+ennemy.width//2))**2+((base.y+base.height//2)-(ennemy.y+ennemy.height//2))**2) < ennemy.max_speed and ennemy.reload == ennemy.rate:
					base.life -= ennemy.damage
					ennemy.bombing = [ennemy.x+randrange(-20, 20), ennemy.y+randrange(-20, 20)]
					ennemy.reload = 0
					ennemy.speed = ennemy.max_speed
				if (base.x+base.width//2)-(ennemy.x+ennemy.width//2) > 100:
					ennemy.y += 0.5*(ennemy.speed/ennemy.max_speed)
				if (base.x+base.width//2)-(ennemy.x+ennemy.width//2) < -100:
					ennemy.y -= 0.5*(ennemy.speed/ennemy.max_speed)
				if (base.y+base.height//2)-(ennemy.y+ennemy.height//2) > 100:
					ennemy.x -= 0.5*(ennemy.speed/ennemy.max_speed)
				if (base.y+base.height//2)-(ennemy.y+ennemy.height//2) < -100:
					ennemy.x += 0.5*(ennemy.speed/ennemy.max_speed)
									
				if ennemy.reload < ennemy.rate:
					if ennemy.speed >= 0:
						ennemy.reload += 1
						ennemy.speed -= (ennemy.max_speed*1)/ennemy.rate #animation de ralentissement de l'avion
						ennemy.x += ennemy.movementx * (ennemy.speed/ennemy.max_speed)
						ennemy.y += ennemy.movementy * (ennemy.speed/ennemy.max_speed)
				elif ennemy.reload == ennemy.rate:
					if ((base.x+base.width//2)-(ennemy.x+ennemy.width//2)) > 0:
						ennemy.direction = "right"
					elif ((base.x+base.width//2)-(ennemy.x+ennemy.width//2)) < 0:
						ennemy.direction = "left"
					if ennemy.speed < ennemy.max_speed:
						ennemy.speed += (ennemy.max_speed)/(ennemy.rate/2)
					else:
						ennemy.speed = ennemy.max_speed #pour ne pas dépasser la vitesse max
					ennemy.movementx = ((base.x+base.width//2)-(ennemy.x+ennemy.width//2)) * (ennemy.speed/math.sqrt(((base.x+base.width//2)-(ennemy.x+ennemy.width//2))**2+((base.y+base.height//2)-(ennemy.y+ennemy.height//2))**2)) # j'ai fait cette équation pour permettre le déplacement horizontal, elle n'est probablement la meilleure mais elle est fonctionnelle
					ennemy.movementy = ((base.y+base.height//2)-(ennemy.y+ennemy.height//2)) * (ennemy.speed/math.sqrt(((base.x+base.width//2)-(ennemy.x+ennemy.width//2))**2+((base.y+base.height//2)-(ennemy.y+ennemy.height//2))**2)) # ennemy.speed/sqrt((base.x-ennemy.x)²+(base.y-ennemy.y)²) représente la proportion entre la distance restante à parcourir (calculée avec le théorème de pythagore) et la vitesse de l'unité
					# et ensuite je multiplie la distance en x et la distance en y par cette proportion
					ennemy.x += ennemy.movementx
					ennemy.y += ennemy.movementy

				
	### TIRS DE MORTIER
	for mortar in mortars:
		mortar = MortarShot(mortar, ennemies)
	#test pour voir l'argent gagné par secondes
	#if moneytime == 100:
	#	moneytime = 0
	#	print(moneypersecond)
	#	moneypersecond = 0
	#else :
	#	moneytime += 1
	
	### vague suivante
	if ennemies[-1].alive == False and flying[-1].alive == False:
		count = 0
		for ennemy in ennemies :
			if ennemy.alive == False and ennemy.life <= 0:
				count += 1
			else :
				count = 0
		for ennemy in flying :
			if ennemy.alive == False and ennemy.life <= 0:
				count += 1
			else :
				count = 0
		if count == len(ennemies)+len(flying):
			while count > len(flying):
				del(ennemies[-1])
				count -= 1
			while count > 0:
				del(flying[-1])
				count -= 1
			wave += 1
			if wave < len(level1[1]):
				time = 0
				ennemies.append(createnewennemy(Ennemy, 0,0, 0, 0))
				ennemies[-1].alive = False 
				flying.append(createnewennemy(Ennemy, 0,0, 0, 0))
				flying[-1].alive = False 
				for soldier in soldiers :
					soldier.life = soldier.max_life
				for i in range(len(level1[1][wave])): #on créé les ennemis
					ennemies.append(createnewennemy(Ennemy, level1[1][wave][i][0],level1[1][wave][i][1], level1[1][wave][i][2], level1[1][wave][i][3]))
				for i in range(len(level1[2][wave])): #on créé les ennemis aériens
					flying.append(createnewplane(Plane, level1[2][wave][i][0],level1[2][wave][i][1], level1[2][wave][i][2], level1[2][wave][i][3]))
			else:
				run = False
	
	TDGraphics.redrawGameWindow(window, turretbutton, turrets, locations, money, base, roads, soldiers, ennemies, base.life, mortars, unitbutton, selected, flying) #on actualise en important la fonction
time = 0
pygame.quit()
