#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import time
try:
	import matplotlib.pyplot as plt
	matplot = True
except ModuleNotFoundError:
	matplot = False

pfad = "abbiegen6.txt"

#Einlesen der Datei und Werte in bestimmtes Format umwandeln
with open(pfad) as datei:
	anzahl_str = int(datei.readline())
	start = datei.readline()[1:-2].split(",")
	start = [float(elem) for elem in start]
	ziel = datei.readline()[1:-2].split(",")
	ziel = [float(elem) for elem in ziel]
	liste_koords = datei.readlines()
for i in range(len(liste_koords)):
	liste_koords[i] = liste_koords[i][:-1].split(" ")
	liste_koords[i][0] = liste_koords[i][0][1:-1].split(",")
	liste_koords[i][0] = [float(elem) for elem in liste_koords[i][0]]
	liste_koords[i][1] = liste_koords[i][1][1:-1].split(",")
	liste_koords[i][1] = [float(elem) for elem in liste_koords[i][1]]

#alle Knoten werden in eine Liste geschrieben
alle_knoten = [list(x) for x in set(
			[tuple(e) for e in [*list(x[0] for x in liste_koords),
			*list(x[1] for x in liste_koords)]])]
#Dictionary in dem jeder Knoten mit seinen möglichen
#weiterführenden Knoten aufgelistet wird
#Zeit stoppen
zeit = time.time()
knotenliste = {}
kurv_und_dist = {}
for elem in alle_knoten:
	knotenliste[str(elem)] = []
	kurv_und_dist[str(elem)] = []
	for f in range(len(liste_koords)):
		if liste_koords[f][0] == elem:
			koord = liste_koords[f][1]
			knotenliste[str(elem)].append(koord)
		elif liste_koords[f][1] == elem:
			koord = liste_koords[f][0]
			knotenliste[str(elem)].append(koord)

def berechnungen(ber_knoten, knoten_davor, kurven, strecke, winkel_davor):
	x_alt, y_alt = knoten_davor[0], knoten_davor[1]
	x_neu, y_neu = ber_knoten[0], ber_knoten[1]
	diff_x, diff_y = x_neu - x_alt, y_neu - y_alt
	#Distanz zwischen Knoten davor und jetzigem Knoten errechnen
	dist = math.sqrt(diff_x**2 + diff_y**2)
	#Winkel der Strecke zwischen Knoten davor und jetzigem Knoten errechnen
	if diff_x == 0.0:
		winkel = 1.57
	elif diff_y == 0.0:
		winkel = 0.0
	else:
		winkel = math.atan(diff_y/diff_x)
	if winkel_davor != None:
		#wenn Winkel ungleich ist --> kurven um 1 erhöhen
		if abs(winkel_davor - winkel) > 0.0001:
			kurven += 1
	#bereits zurückgelegte Strecke errechnen
	strecke = strecke + dist
	#Dictionary mit allen Knoten und ihrer niedrigsten
	#Richtungswechselanzahl und Streckenlänge
	if not kurv_und_dist[str(ber_knoten)]:
		kurv_und_dist[str(ber_knoten)].append(kurven)
		kurv_und_dist[str(ber_knoten)].append(strecke)
		return [ber_knoten, kurven, strecke, winkel]
	else:
		#wenn der jetzige Punkt im Dictionary bereits einen Eintrag
		#hat in dem Richtungswechselanzahl
		#und Streckenlänge niedriger ist gibt die Funktion None zurück 
		if kurven >= kurv_und_dist[str(ber_knoten)][0]:
			if strecke >= kurv_und_dist[str(ber_knoten)][1]:
				return None
		#wenn Richtungswechselanzahl und Streckenlänge höher,
		#durch neue Werte ersetzen und Attribute zurückgeben
		else:
			kurv_und_dist[str(ber_knoten)][0] = kurven
			kurv_und_dist[str(ber_knoten)][1] = strecke
			return [ber_knoten, kurven, strecke, winkel]

def bedingungen(knoten, fliste):
	#wenn bei Ziel angekommen, return
	if knoten == ziel:
		liste_davor = fliste[-1]
		#Strecke etc. wird berechnet
		berechnetes = berechnungen(knoten, liste_davor[0],
									liste_davor[1], liste_davor[2],
									 liste_davor[3])
		#wenn None zurückgegeben, return
		if berechnetes == None:
			return
		#niedrigste Anzahl von Richtungswechseln und Streckenlänge
		#bei Ende der Strecke
		global niedrigste_kurv_und_dist
		if niedrigste_kurv_und_dist == []:
			niedrigste_kurv_und_dist = [berechnetes[1],
			 							berechnetes[2]]
		elif berechnetes[1] <= niedrigste_kurv_und_dist[0]:
			if berechnetes[2] <= niedrigste_kurv_und_dist[1]:
				niedrigste_kurv_und_dist = [berechnetes[1],
											berechnetes[2]]

		fliste.append(berechnetes)
		#Weg zur globalen Liste moeglichkeiten hinzugefügen
		moeglichkeiten.append(fliste)
		return
	#wenn der Knoten bereits in der lokalen Liste fliste ist, return
	if knoten in [elem[0] for elem in fliste]:
		return
	try:
		#Versuch auf Eintrag davor in der lokalen Liste zuzugreifen
		liste_davor = fliste[-1]
		#Strecke etc. wird berechnet
		berechnetes = berechnungen(knoten, liste_davor[0], liste_davor[1],
									 liste_davor[2], liste_davor[3])
		#wenn None zurückgegeben, return
		if berechnetes == None:
			return
		#wenn Richtungswechselanzahl und Streckenlänge des jetzigen Punktes
		#höher ist als diese Werte eines schon vollendeten Weges, return
		try:
			if berechnetes[1] >= niedrigste_kurv_und_dist[0]:
				if berechnetes[2] >= niedrigste_kurv_und_dist[1]:
					return
		except IndexError:
			pass
		fliste.append(berechnetes)
	#wenn es keinen Eintrag davor in der lokalen Liste gibt, erster Eintrag
	#--> Kurven = 0, Strecke = 0, Winkel nicht definiert
	except IndexError:
		fliste.append([knoten, 0, 0, None])
	#Rekursion, zu allen moeglichen naechsten Knoten gehen
	for elem in knotenliste[str(knoten)]:
		bedingungen(elem, fliste[:])
	return

def vergleich():
	vergleiche = []
	#kleinste Gesamtstrecke suchen
	min_strecke = 0
	for i in range(len(moeglichkeiten)):
		if min_strecke:
			if moeglichkeiten[i][-1][2] < min_strecke:
				min_strecke = moeglichkeiten[i][-1][2]
		else:
			min_strecke = moeglichkeiten[i][-1][2]

		ende = [moeglichkeiten[i][-1][1], moeglichkeiten[i][-1][2]]
		vergleiche.append(ende)
	#Prozentzahl der Verlängerung des Weges für jede Strecke berechnen
	for j in range(len(vergleiche)):
		prozent = vergleiche[j][1]/min_strecke*100-100
		vergleiche[j].append(prozent)
	unter_prozent = []
	#alle Wege die unter der maximalen Verlängerung liegen
	#in Liste mit Index
	for k in range(len(vergleiche)):
		if vergleiche[k][2] <= max_abweichung:
			unter_prozent.append([vergleiche[k], k])
	#minimale Richtungswechselanzahl bei allen moeglichen
	#unter der maximalen Abweichung suchen
	min_kurv = min([unter_prozent[k][0][0] for k in range(len(unter_prozent))])
	#die Wege mit der minimalen Richtungswechselanzahl extrahieren und
	#den Weg mit der niedrigsten Streckenlänge bestimmen
	kleinste_str = 0
	for elem in unter_prozent:
		if elem[0][0] == min_kurv:
			if kleinste_str:
				if elem[0][1] < kleinste_str:
					kleinste_str = elem[0][1]
					min_kurv_moegl = elem
			else:
				kleinste_str = elem[0][1]
				min_kurv_moegl = elem
	#Koordinaten sowie Richtungswechselanzahl, Streckenlänge und
	#Verlängerung des "besten" Weges zurückgeben
	return [moeglichkeiten[min_kurv_moegl[1]], min_kurv_moegl[0][0],
			 min_kurv_moegl[0][1], min_kurv_moegl[0][2]]

def ausgabe(weg, kurven, strecke, verlaengerung, laufzeit):
	#alle Koordinaten in richtiger Reihenfolge in Liste
	k_liste = []
	for elem in weg:
		k_liste.append(elem[0])
	print("Der Weg mit den wenigsten Richtungswechseln bei einer " +
		"maximalen Verlängerung von " + str(max_abweichung) +
		"% mit einer Verlängerung von " + str(verlaengerung) +
		"%, " + str(kurven) + " Richtungswechsel/n und der Streckenlänge "+
		str(strecke) + " geht über die Punkte: " + str(k_liste))

	print("Laufzeit: " + str(laufzeit) + " Sekunden")
	#wenn matplotlib installiert ist, grafische Ausgabe anbieten
	if matplot == False:
		print("Grafische Ausgabe nicht möglich, da das Modul matplotlib"+
			 "nicht installiert ist")
	else:
		grafische = input("Grafische Ausgabe?[J/n]")
		if grafische == "J" or grafische == "j":
			grafisch(beste_strecke[0])

def grafisch(weg):
	#Grundnetzstruktur plotten
	for i in range(len(liste_koords)):
		plt.plot([liste_koords[i][0][0], liste_koords[i][1][0]],
				 [liste_koords[i][0][1], liste_koords[i][1][1]],
		 		 marker=".", color="blue")
	#die Strecke des "besten" Weges plotten
	x = []
	y = []
	for elem in weg:
		x.append(elem[0][0])
		y.append(elem[0][1])
	plt.plot(x,y, color="green", linewidth=5)
	#Start und Ziel plotten
	plt.plot(start[0], start[1], "o", color="red")
	plt.text(start[0], start[1], "Start")
	plt.plot(ziel[0], ziel[1], "o", color="red")
	plt.text(ziel[0], ziel[1], "Ziel")
	#Grafik aufrufen
	plt.show()

#Benutzereingabe für die maximale Abweichung
def eingabe():
	while True:
		try:
			eingabe = int(input("Maximale Abweichung in Prozent bitte " +
				"als Integer eingeben (für den schnellsten Weg 0 eingeben)"))
			return eingabe
			break
		except ValueError:
			print("Bitte geben Sie einen Integer ein")
def main():
	global moeglichkeiten
	moeglichkeiten = []
	global niedrigste_kurv_und_dist
	niedrigste_kurv_und_dist = []
	#Aufrufen der Funktionen
	bedingungen(start, [])
	#wenn Moeglichkeiten gefunden wurden, beste Strecke suchen und ausgeben
	if moeglichkeiten != []:
		global zeit
		zeit = time.time() - zeit
		global max_abweichung
		max_abweichung = eingabe()
		zeit2 = time.time()
		global beste_strecke
		beste_strecke = vergleich()
		zeit += time.time()-zeit2
		ausgabe(beste_strecke[0], beste_strecke[1], beste_strecke[2],
				 beste_strecke[3], zeit)
	else:
		print("Keine moegliche Strecke gefunden")
main()
