#!/usr/bin/env python3
# coding:utf8

#################### INITIATIONS ET IMPORTATIONS ########################

import pygame
pygame.init()
from random import randrange

window = pygame.display.set_mode((1000,1000))

def graphics(WINDOWWIDTH,WINDOWHEIGHT, flags): #on créé la fenêtre a partir de valeurs de l'autre fichier
		window = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT), flags) #on initie la fenêtre
		pygame.display.set_caption("TD") #le petit message en haut de la fenêtre
		return(window)
buttonturret = [pygame.image.load("sprites/buttons/ButtonTurret0.png"), pygame.image.load("sprites/buttons/ButtonTurret1.png")]
buttonfarm = [pygame.image.load("sprites/buttons/ButtonFarm0.png"), pygame.image.load("sprites/buttons/ButtonFarm1.png")]
buttonunit = [pygame.image.load("sprites/buttons/ButtonUnit0.png"), pygame.image.load("sprites/buttons/ButtonUnit1.png")]
buttonwall = [pygame.image.load("sprites/buttons/Buttonwall0.png"), pygame.image.load("sprites/buttons/Buttonwall1.png")]
buttonsniper = [pygame.image.load("sprites/buttons/ButtonSniper0.png"), pygame.image.load("sprites/buttons/ButtonSniper1.png")]

buttonupgrade80 = [pygame.image.load("sprites/buttons/Button80UP0.png"), pygame.image.load("sprites/buttons/Button80UP1.png")]
buttonupgrade100 = [pygame.image.load("sprites/buttons/Button100UP0.png"), pygame.image.load("sprites/buttons/Button100UP1.png")]
buttonupgrade125 = [pygame.image.load("sprites/buttons/Button125UP0.png"), pygame.image.load("sprites/buttons/Button125UP1.png")]
buttonupgrade150 = [pygame.image.load("sprites/buttons/Button150UP0.png"), pygame.image.load("sprites/buttons/Button150UP1.png")]

buttonDestroy25 = [pygame.image.load("sprites/buttons/Button25Destroy0.png"), pygame.image.load("sprites/buttons/Button25Destroy1.png")]
buttonDestroy33 = [pygame.image.load("sprites/buttons/Button33Destroy0.png"), pygame.image.load("sprites/buttons/Button33Destroy1.png")]
buttonDestroy65 = [pygame.image.load("sprites/buttons/Button65Destroy0.png"), pygame.image.load("sprites/buttons/Button65Destroy1.png")]
buttonDestroy75 = [pygame.image.load("sprites/buttons/Button75Destroy0.png"), pygame.image.load("sprites/buttons/Button75Destroy1.png")]
buttonDestroy100 = [pygame.image.load("sprites/buttons/Button100Destroy0.png"), pygame.image.load("sprites/buttons/Button100Destroy1.png")]

turret1level1 = [pygame.image.load("sprites/turrets/turret 1_sprite_1.png"),pygame.image.load("sprites/turrets/turret 1_sprite_2.png"),pygame.image.load("sprites/turrets/turret 1_sprite_3.png"),pygame.image.load("sprites/turrets/turret 1_sprite_4.png"),pygame.image.load("sprites/turrets/turret 1_sprite_5.png"),pygame.image.load("sprites/turrets/turret 1_sprite_6.png"),pygame.image.load("sprites/turrets/turret 1_sprite_7.png"),pygame.image.load("sprites/turrets/turret 1_sprite_8.png"),]
turret1level2 = [pygame.image.load("sprites/turrets/turret 12_sprite_1.png"),pygame.image.load("sprites/turrets/turret 12_sprite_2.png"),pygame.image.load("sprites/turrets/turret 12_sprite_3.png"),pygame.image.load("sprites/turrets/turret 12_sprite_4.png"),pygame.image.load("sprites/turrets/turret 12_sprite_5.png"),pygame.image.load("sprites/turrets/turret 12_sprite_6.png"),pygame.image.load("sprites/turrets/turret 12_sprite_7.png"),pygame.image.load("sprites/turrets/turret 12_sprite_8.png"),pygame.image.load("sprites/turrets/turret 12_sprite_9.png")]

farm = [pygame.image.load("sprites/turrets/Farm1.png"), pygame.image.load("sprites/turrets/Farm2.png")]

ennemy_infantry = [[pygame.image.load("sprites/ennemies/ennemy1_right_sprite_0.png"), pygame.image.load("sprites/ennemies/ennemy1_right_sprite_1.png"), pygame.image.load("sprites/ennemies/ennemy1_right_sprite_2.png"), pygame.image.load("sprites/ennemies/ennemy1_right_sprite_3.png"), pygame.image.load("sprites/ennemies/ennemy1_right_sprite_2.png"), pygame.image.load("sprites/ennemies/ennemy1_right_sprite_1.png")], #ceux qui vont à droite
[pygame.image.load("sprites/ennemies/ennemy1_left_sprite_0.png"), pygame.image.load("sprites/ennemies/ennemy1_left_sprite_1.png"), pygame.image.load("sprites/ennemies/ennemy1_left_sprite_2.png"), pygame.image.load("sprites/ennemies/ennemy1_left_sprite_3.png"), pygame.image.load("sprites/ennemies/ennemy1_left_sprite_2.png"), pygame.image.load("sprites/ennemies/ennemy1_left_sprite_1.png")]] #ceux qui vont à gauche

ennemy_plane = [pygame.image.load("sprites/ennemies/Plane1_0.png"), pygame.image.load("sprites/ennemies/Plane1_1.png"), pygame.image.load("sprites/ennemies/Plane1_2.png")]

explosion1 = [pygame.image.load("sprites/others/explosion1_0.png"), pygame.image.load("sprites/others/explosion1_1.png"), pygame.image.load("sprites/others/explosion1_2.png"), pygame.image.load("sprites/others/explosion1_3.png"), pygame.image.load("sprites/others/explosion1_4.png"), pygame.image.load("sprites/others/explosion1_5.png"), pygame.image.load("sprites/others/explosion1_6.png"), pygame.image.load("sprites/others/explosion1_7.png")]

locations = [pygame.image.load("sprites/others/location.png")]
backgrounds = [pygame.image.load("sprites/others/background1.png").convert()]
def scale(proportion):
	locations[0] = pygame.transform.scale(locations[0], (64*proportion, 64*proportion))
	for i in range(len(ennemy_infantry)):
		for j in range(len(ennemy_infantry[i])):
			ennemy_infantry[i][j] = pygame.transform.scale(ennemy_infantry[i][j], (24*proportion, 24*proportion))
	for i in range(len(ennemy_plane)):
		ennemy_plane[i] = pygame.transform.scale(ennemy_plane[i], (60*proportion, 60*proportion))
	for i in range(len(explosion1)):
		explosion1[i] = pygame.transform.scale(explosion1[i], (40*proportion, 40*proportion))
	for i in range(len(backgrounds)):
		backgrounds[i] = pygame.transform.scale(backgrounds[i], (1000 * proportion, 1000*proportion))
		
#### FONCTIONS DE DESSIN

def buttondraw(window, button, turrets, selected): #on dessine un bouton
	if button.visible == True:
		if button.use == "turret":
			if button.clicked == True:
				window.blit(buttonturret[1],( button.x, button.y))
			if button.clicked == False:
				window.blit(buttonturret[0],( button.x, button.y))
		elif button.use == "farm":
			if button.clicked == True:
				window.blit(buttonfarm[1],( button.x, button.y))
			if button.clicked == False:
				window.blit(buttonfarm[0],( button.x, button.y))
		elif button.use == "sniper":
			if button.clicked == True:
				window.blit(buttonsniper[1],( button.x, button.y))
			if button.clicked == False:
				window.blit(buttonsniper[0],( button.x, button.y))
		# boutons de modifications des tourelles
		elif button.use == "upgrade":
			if turrets[selected].clas == 1 and turrets[selected].level == 1:
				if button.clicked == True:
					window.blit(buttonupgrade100[1],( button.x, button.y))
				if button.clicked == False:
					window.blit(buttonupgrade100[0],( button.x, button.y))
			if turrets[selected].clas == 2 and turrets[selected].level == 1:
				if button.clicked == True:
					window.blit(buttonupgrade80[1],( button.x, button.y))
				if button.clicked == False:
					window.blit(buttonupgrade80[0],( button.x, button.y))
			if turrets[selected].clas == 3 and turrets[selected].level == 1:
				if button.clicked == True:
					window.blit(buttonupgrade125[1],( button.x, button.y))
				if button.clicked == False:
					window.blit(buttonupgrade125[0],( button.x, button.y))
		elif button.use == "destroy":
			if turrets[selected].clas == 1 and turrets[selected].level == 1:
				if button.clicked == True:
					window.blit(buttonDestroy25[1],( button.x, button.y))
				if button.clicked == False:
					window.blit(buttonDestroy25[0],( button.x, button.y))
			if turrets[selected].clas == 1 and turrets[selected].level == 2:
				if button.clicked == True:
					window.blit(buttonDestroy75[1],( button.x, button.y))
				if button.clicked == False:
					window.blit(buttonDestroy75[0],( button.x, button.y))
			if turrets[selected].clas == 2 and turrets[selected].level == 1:
				if button.clicked == True:
					window.blit(buttonDestroy25[1],( button.x, button.y))
				if button.clicked == False:
					window.blit(buttonDestroy25[0],( button.x, button.y))
			if turrets[selected].clas == 2 and turrets[selected].level == 2:
				if button.clicked == True:
					window.blit(buttonDestroy65[1],( button.x, button.y))
				if button.clicked == False:
					window.blit(buttonDestroy65[0],( button.x, button.y))
			if turrets[selected].clas == 3 and turrets[selected].level == 1:
				if button.clicked == True:
					window.blit(buttonDestroy33[1],( button.x, button.y))
				if button.clicked == False:
					window.blit(buttonDestroy33[0],( button.x, button.y))
			if turrets[selected].clas == 3 and turrets[selected].level == 2:
				if button.clicked == True:
					window.blit(buttonDestroy100[1],( button.x, button.y))
				if button.clicked == False:
					window.blit(buttonDestroy100[0],( button.x, button.y))
		#boutons avec un temps de chargement
		elif button.use == "units":
			if button.clicked == True:
				window.blit(buttonunit[1],( button.x, button.y))
			if button.clicked == False:
				window.blit(buttonunit[0],( button.x, button.y))
			pygame.draw.rect(window, (240, 20, 20), (button.x, button.y - 30, button.width, 15))
			pygame.draw.rect(window, (185, 185, 185), (button.x, button.y - 30, button.width*(float(button.reloaded)/float(button.reloading)), 15)) 
		elif button.use == "wall":
			if button.clicked == True:
				window.blit(buttonwall[1],( button.x, button.y))
			if button.clicked == False:
				window.blit(buttonwall[0],( button.x, button.y))
			pygame.draw.rect(window, (240, 20, 20), (button.x, button.y - 30, button.width, 15))
			pygame.draw.rect(window, (185, 185, 185), (button.x, button.y - 30, button.width*(float(button.reloaded)/float(button.reloading)), 15)) 


def turretdraw(window, surface,  turret): #on dessine une tourelle
	if turret.exists == True:
		if turret.being_placed == True or turret.selected == True :
			surface = pygame.Surface((1000,1000), pygame.SRCALPHA)
			cercle = pygame.draw.circle(surface, (120, 120,230, 128), (int(turret.x) + int(turret.width)//2 - 65, int(turret.y) + int(turret.height)//2), int(turret.ranged))
		### première tourelle
		if turret.clas == 1:
			if turret.level == 1:
				if turret.locked == True and turret.reload <= 12:
					window.blit(turret1level1[(turret.reload+1)//2],( turret.x, turret.y))
				else:
					window.blit(turret1level1[0],( turret.x, turret.y))
			if turret.level == 2:
				if turret.locked == True and turret.reload <= 10:
					window.blit(turret1level2[(turret.reload+1)//2],( turret.x, turret.y))
				else:
					window.blit(turret1level2[0],( turret.x, turret.y))
		elif turret.clas == 2:
			if turret.level == 1:
				window.blit(farm[0],( turret.x, turret.y))
			if turret.level == 2:
				window.blit(farm[1],( turret.x, turret.y))
		else:
			if turret.locked == True and turret.reload + 5 >= turret.rate:
				if turret.selected == True:
					pygame.draw.rect(surface, (250, 220, 50), (turret.x - 65,turret.y, turret.width, turret.height))
				else:
					pygame.draw.rect(window, (250, 220, 50), (turret.x,turret.y, turret.width, turret.height))
			else:
				pygame.draw.rect(window, turret.color, (turret.x,turret.y, turret.width, turret.height))
			if turret.level == 2:
				if turret.selected == True:
					pygame.draw.circle(surface, (250, 220, 50), (int(turret.x)+ int(turret.width) - 65, int(turret.y)), 5)
				#else:
					#pygame.draw.cir
	return surface


def locationdraw(window, location): #on dessine une tourelle
	if location.used == False:
		window.blit(locations[0],( location.x, location.y))

def basedraw(window, surface, base):  #on dessine la base principale
	pygame.draw.rect(window, (240, 20, 20), (1, 80, 100, 15)) #sa barre de vie rouge
	if base.life >= 1:
		pygame.draw.rect(window, (80, 230, 65), (1, 80, 100*(float(base.life)/float(base.max_life)), 15)) #sa barre de vie verte
	if base.selected == True :
		surface = pygame.Surface((1000,1000), pygame.SRCALPHA)
		cercle = pygame.draw.circle(surface, (120, 120,230, 128), (int(base.x) + int(base.width)//2 - 65, int(base.y) + int(base.height)//2), int(base.ranged))
	if base.locked == True and base.reload + 5 >= base.rate:
		if base.selected == True :
			pygame.draw.rect(surface, (250, 220, 50), (base.x - 65, base.y, base.width, base.height))
		else :
			pygame.draw.rect(window, (250, 220, 50), (base.x, base.y, base.width, base.height))
	else:
		pygame.draw.rect(window, (50, 50, 220), (base.x, base.y, base.width, base.height))
	return surface
	

def ennemydraw(window, ennemy):
	if ennemy.alive == True:
		if ennemy.typ == 1:
			if ennemy.direction == "right":
				if ennemy.locked == False:
					window.blit(ennemy_infantry[0][ennemy.walk//16],( ennemy.x, ennemy.y))
				else:
					window.blit(ennemy_infantry[0][1],( ennemy.x, ennemy.y))
			elif ennemy.direction == "left":
				if ennemy.locked == False:
					window.blit(ennemy_infantry[1][ennemy.walk//16],( ennemy.x, ennemy.y))
				else:
					window.blit(ennemy_infantry[1][1],( ennemy.x, ennemy.y))
			elif ennemy.direction == "top":
				if ennemy.locked == True and ennemy.reload + 5 >= ennemy.rate:
					pygame.draw.rect(window, (250, 220, 50), (ennemy.x, ennemy.y, ennemy.width, ennemy.height))
				else:
					pygame.draw.rect(window, (200, 50, 170), (ennemy.x, ennemy.y, ennemy.width, ennemy.height))
			elif ennemy.direction == "bottom":
				if ennemy.locked == True and ennemy.reload + 5 >= ennemy.rate:
					pygame.draw.rect(window, (250, 220, 50), (ennemy.x, ennemy.y, ennemy.width, ennemy.height))
				else:
					pygame.draw.rect(window, (200, 50, 170), (ennemy.x, ennemy.y, ennemy.width, ennemy.height))
		elif ennemy.typ == 2:
				pygame.draw.rect(window, (160, 20, 130), (ennemy.x, ennemy.y, ennemy.width, ennemy.height))
		pygame.draw.rect(window, (240, 20, 20), (ennemy.x, ennemy.y - 25, ennemy.width, 10)) #sa barre de vie rouge
		pygame.draw.rect(window, (80, 230, 65), (ennemy.x, ennemy.y - 25, ennemy.width*(float(ennemy.life)/float(ennemy.max_life)), 10)) #sa barre de vie verte

def mortardraw(window, mortar):
	if mortar.direction < 2:
		pygame.draw.circle(window, (115, 115,115), (int(mortar.x), int(mortar.y)), mortar.radius) #boulet normal
	elif mortar.direction >= 2 and mortar.direction < 4:
		pygame.draw.circle(window, (250, 220, 50), (int(mortar.x), int(mortar.y)), mortar.radius*3) #explosion


def roaddraw(window, road):
	pygame.draw.rect(window, (240, 00, 00), (road.x, road.y, road.width, road.height), 2)


def soldierdraw(window, soldier):
	if soldier.alive :
		if soldier.unit == 1:
			if soldier.locked == True and soldier.reload + 5 >= soldier.rate:
				pygame.draw.rect(window, (250, 220, 50), (soldier.x, soldier.y, soldier.width, soldier.height))
			else:
				pygame.draw.rect(window, (120, 140, 200), (soldier.x, soldier.y, soldier.width, soldier.height))
		elif soldier.unit == 2:
			pygame.draw.rect(window, (117, 117, 117), (soldier.x, soldier.y, soldier.width, soldier.height))
		if soldier.being_placed == False:
			pygame.draw.rect(window, (240, 20, 20), (soldier.x, soldier.y - 25, soldier.width, 10)) #sa barre de vie rouge
			pygame.draw.rect(window, (45, 160, 30), (soldier.x, soldier.y - 25, soldier.width*(float(soldier.life)/float(soldier.max_life)), 10)) #sa barre de vie verte

def flyerdraw(window, ennemy, base):
	if ennemy.alive == True:
		if ennemy.reload < 40:
			window.blit(explosion1[ennemy.reload//5],(int(ennemy.bombing[0]+randrange(-1,1)), int(ennemy.bombing[1]+randrange(-1,1))))
		if ennemy.direction == "right":
			window.blit(ennemy_plane[(ennemy.walk//5)],(ennemy.x, ennemy.y))
		elif ennemy.direction == "left":
			window.blit(pygame.transform.flip(ennemy_plane[(ennemy.walk//5)], True, False),(ennemy.x, ennemy.y))
		pygame.draw.rect(window, (240, 20, 20), (ennemy.x, ennemy.y - 25, ennemy.width, 10)) #sa barre de vie rouge
		pygame.draw.rect(window, (80, 230, 65), (ennemy.x, ennemy.y - 25, ennemy.width*(float(ennemy.life)/float(ennemy.max_life)), 10)) #sa barre de vie verte

### FONCTION D'ACTUALISTATION

def redrawGameWindow(window, turretbutton, turrets, locations, money, base, roads, soldiers, ennemies, life, mortars, unitbutton, selected, flying): #on actualise
	surface = pygame.Surface((0,0), pygame.SRCALPHA)  # on créé une surface pour y mettre des trucs transparents
	window.fill((0,0,0)) #fond noir 
	window.blit(backgrounds[0], (64, 0)) #et on rajoute le vrai fond
	#for road in roads:
	#	roaddraw(window, road)
	for location in locations: #on met tout les emplacements 
		locationdraw(window, location)
	for button in turretbutton: #on met tout les boutons
		buttondraw(window,button, turrets, selected)
	for button in unitbutton:
		buttondraw(window, button, turrets, selected)
	surface = basedraw(window, surface, base)
	for turret in turrets: #on met toutes les tourelles
		surface = turretdraw(window, surface, turret)
	for ennemy in ennemies:
		ennemydraw(window, ennemy)
	for soldier in soldiers:
		soldierdraw(window, soldier)
	for mortar in mortars:
		mortardraw(window, mortar)
	for flyer in flying:
		flyerdraw(window, flyer, base)
	### ecriture du score
	font = pygame.font.SysFont("comicsans", 30, True) #POLICE, OUVREZ !!!! (oui bon c'est la police de caractère)
	text = font.render("Money : " + str(int(money//1)), 1 , (110, 110, 110)) #on écrit l'argent possédé
	window.blit(text, (10, 10))
	text = font.render("Life : " + str(int(life//1)), 1 , (110, 110, 110)) #on écrit la vie de la base
	window.blit(text, (10, 50))
	window.blit(surface, (64,0)) #on actualise la surface avec le cercle transparent
	pygame.display.update() #on actualise la fenêtre


