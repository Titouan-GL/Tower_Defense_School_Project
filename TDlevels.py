#!/usr/bin/env python3
# coding:utf8

#ce document serivra à stocker les différents niveau via une liste. le premier indice est l'emplacement des locations
#le deuxième indice est l'emplacement des unités ennemies au début du niveau, leur direction et leur délai d'apparition (en frames * 10)
proportion = 1 #cette variable sert à redimentionner la fenêtre
WINDOWHEIGHT = 1000 * proportion #dimentions de la fenêtre
WINDOWWIDTH = 1000 * proportion
from random import randrange
margin = 65
#### TRES IMPORTANT :
# Une ligne de largeur 65 est présente des deux cotés pour y mettre des boutons, alors tout les x sont décalés de 65. quand on veut qu'un ennemis commence sa trajectoire à x = 0, on fait x = 65
# les espaces pour se déplacer sont de 85.
# la plupart des calculs sont fait a partir de ses deux valeurs
def level1():
	level1 = [ 
	[ #locations
	[100 * proportion + margin, WINDOWHEIGHT//2 + 100 * proportion],[100 * proportion + margin, WINDOWHEIGHT//2 - 100 * proportion], [300 * proportion + margin, WINDOWHEIGHT//2 + 100 * proportion], [300 * proportion + margin, WINDOWHEIGHT//2 - 100 * proportion], [200 * proportion + margin, WINDOWHEIGHT//2 + 200 * proportion], [200 * proportion + margin, WINDOWHEIGHT//2 - 200 * proportion], #emplacements de gauche
	[800 * proportion + margin, WINDOWHEIGHT//2 + 200 * proportion], [800 * proportion + margin, WINDOWHEIGHT//2 - 200 * proportion], [700 * proportion + margin, WINDOWHEIGHT//2 + 100 * proportion], [700 * proportion + margin, WINDOWHEIGHT//2 - 100 * proportion],[900 * proportion + margin, WINDOWHEIGHT//2 + 100 * proportion], [900 * proportion + margin, WINDOWHEIGHT//2 - 100 * proportion],  #emplacements de droite
	[WINDOWWIDTH//2 + 100 * proportion + margin, 100 * proportion],[WINDOWWIDTH//2 - 99 * proportion + margin, 100 * proportion], [WINDOWWIDTH//2 + 100 * proportion + margin,  300 * proportion], [WINDOWWIDTH//2 - 99 * proportion + margin ,  300 * proportion], [300 * proportion + margin,  200 * proportion], [WINDOWWIDTH//2 + 200 * proportion + margin,  200 * proportion] ,#emplacements du haut (le -99 est du à 23-(165 - 23 - 85)-65
	[WINDOWWIDTH//2 + 100 * proportion + margin, 900 * proportion],[WINDOWWIDTH//2 - 99 * proportion + margin, 900 * proportion], [WINDOWWIDTH//2 + 100 * proportion + margin,  700 * proportion], [WINDOWWIDTH//2 - 99 * proportion + margin ,  700 * proportion], [300 * proportion + margin,  800 * proportion], [WINDOWWIDTH//2 + 200 * proportion + margin,  800 * proportion]#emplacements du bas
	]
	,
	[ #ennemis
	[], [], [], []#j'ai essayé de rendre plus clair le code des ennemis donc il y a leur création plus bas
	]
	,
	[
	[[1064, 0, 1, 1]],[],[], [[1064, 0, 1, 1], [64, 0, 1, 1],[1064, 1000, 1, 1], [64, 1000, 1, 1]]
	]
	,
	[#les routes des ennemis
	["right",margin, WINDOWHEIGHT//2-42 * proportion, 500 * proportion, int(85 * proportion)], 
	["left",WINDOWWIDTH - 500 * proportion + margin, WINDOWHEIGHT//2-42 * proportion, 500 * proportion, int(85 * proportion)], 
	["bottom",WINDOWWIDTH//2 + margin-(85 * proportion/2), -10 , int(85 * proportion), 500 * proportion + 10], # en donnant un peu de marge aux routes d'en haut et en bas elles fonctionnent mieux 
	["top",WINDOWWIDTH//2 + margin-(85 * proportion/2), WINDOWHEIGHT - 500 * proportion , int(85 * proportion), 500 * proportion + 30] 
	]
	]
	
	### EXPLICATIONS
	#les lignes suivantes sont faites pour ajouter des ennemis en continu durant une vague. on met le nombre d'ennemis dans le range (1, 16) correspond à 15 ennemis, c'est basique pour du range
	#delay exprime le nombre de frames multiplié par 20 d'ecart entre l'apparition des ennemis
	#pour mettre plusieurs types d'ennemis en même temps, si ils n'arrivent pas tous en même temps je fais différente boucles. c'est ce que j'ai fait pour la vague 3 où j'ai mis des unités normales et des tanks
	
	#### VAGUE 1
	### fonction des unités simples venant de la gauche
	for i in range (1,16): # le nombre d'ennemis qui vont apparaître grâce à cette fonction
		delay = 7 # délai entre chaques unités
		level1[1][0].append(["right", [65,WINDOWHEIGHT//2 + randrange(int(-42 * proportion), int(18 * proportion))], i*delay, 1])
	### fonction des unités simples venant de la droite
	for i in range (1,16): # le nombre d'ennemis qui vont apparaître grâce à cette fonction
		delay = 7 # délai entre chaques unités
		level1[1][0].append(["left", [WINDOWWIDTH,WINDOWHEIGHT//2 + randrange(int(-42 * proportion), int(18 * proportion))], i*delay, 1])
	### fonction des unités simples venant du haut
	for i in range (1,16): # le nombre d'ennemis qui vont apparaître grâce à cette fonction
		delay = 7 # délai entre chaques unités
		level1[1][0].append(["bottom", [WINDOWWIDTH//2 + randrange(int(-42 * proportion), int(18 * proportion)) + 65, 0 ], i*delay, 1])
	### fonction des unités simples venant du bas
	
	#### VAGUE 2
	### fonction des unités simples venant de la gauche
	for i in range (1,21): # le nombre d'ennemis qui vont apparaître grâce à cette fonction
		delay = 4 # délai entre chaques unités
		level1[1][1].append(["right", [65,WINDOWHEIGHT//2 + randrange(int(-42 * proportion), int(18 * proportion))], i*delay, 1])
	### fonction des unités simples venant de la droite
	for i in range (1,21): # le nombre d'ennemis qui vont apparaître grâce à cette fonction
		delay = 4 # délai entre chaques unités
		level1[1][1].append(["left", [WINDOWWIDTH,WINDOWHEIGHT//2 + randrange(int(-42 * proportion), int(18 * proportion))], i*delay, 1])
	### fonction des unités simples venant du haut
	for i in range (1,21): # le nombre d'ennemis qui vont apparaître grâce à cette fonction
		delay = 4 # délai entre chaques unités
		level1[1][1].append(["bottom", [WINDOWWIDTH//2 + randrange(int(-42 * proportion), int(18 * proportion)) + 65, 0 ], i*delay, 1])
	### fonction des unités simples venant du bas
	for i in range (1,21): # le nombre d'ennemis qui vont apparaître grâce à cette fonction
		delay = 4 # délai entre chaques unités
		level1[1][1].append(["top", [WINDOWWIDTH//2 + randrange(int(-42 * proportion), int(18 * proportion)) + 65, WINDOWHEIGHT], i*delay, 1])
	#### VAGUE 3
	### fonction des unités simples venant de la gauche
	for i in range (1,21): # le nombre d'ennemis qui vont apparaître grâce à cette fonction
		delay = 4 # délai entre chaques unités
		level1[1][2].append(["right", [65,WINDOWHEIGHT//2 + randrange(int(-42 * proportion), int(18 * proportion))], i*delay, 1])
	### fonction des unités simples venant de la droite
	for i in range (1,21): # le nombre d'ennemis qui vont apparaître grâce à cette fonction
		delay = 4 # délai entre chaques unités
		level1[1][2].append(["left", [WINDOWWIDTH,WINDOWHEIGHT//2 + randrange(int(-42 * proportion), int(18 * proportion))], i*delay, 1])
	### fonction des unités simples venant du haut
	for i in range (1,21): # le nombre d'ennemis qui vont apparaître grâce à cette fonction
		delay = 4 # délai entre chaques unités
		level1[1][2].append(["bottom", [WINDOWWIDTH//2 + randrange(int(-42 * proportion), int(18 * proportion)) + 65, 0 ], i*delay, 1])
	### fonction des unités simples venant du bas
	for i in range (1,21): # le nombre d'ennemis qui vont apparaître grâce à cette fonction
		delay = 4 # délai entre chaques unités
		level1[1][2].append(["top", [WINDOWWIDTH//2 + randrange(int(-42 * proportion), int(18 * proportion)) + 65, WINDOWHEIGHT], i*delay, 1])
		
	### fonction des unités blindés venant de la gauche
	for i in range (1,6): # le nombre d'ennemis qui vont apparaître grâce à cette fonction
		delay = 20 # délai entre chaques unités
		level1[1][2].append(["right", [65,WINDOWHEIGHT//2 + randrange(int(-42 * proportion), int(18 * proportion))], i*delay, 2])
	### fonction des unités blindés venant de la droite
	for i in range (1,6): # le nombre d'ennemis qui vont apparaître grâce à cette fonction
		delay = 20 # délai entre chaques unités
		level1[1][2].append(["left", [WINDOWWIDTH,WINDOWHEIGHT//2 + randrange(int(-42 * proportion), int(18 * proportion))], i*delay, 2])
	### fonction des unités blindés venant du haut
	for i in range (1,6): # le nombre d'ennemis qui vont apparaître grâce à cette fonction
		delay = 20 # délai entre chaques unités
		level1[1][2].append(["bottom", [WINDOWWIDTH//2 + randrange(int(-42 * proportion), int(18 * proportion)) + 65, 0 ], i*delay, 2])
	### fonction des unités blindés venant du bas
	for i in range (1,6): # le nombre d'ennemis qui vont apparaître grâce à cette fonction
		delay = 20 # délai entre chaques unités
		level1[1][2].append(["top", [WINDOWWIDTH//2 + randrange(int(-42 * proportion), int(18 * proportion)) + 65, WINDOWHEIGHT], i*delay, 2])
	return(level1)


