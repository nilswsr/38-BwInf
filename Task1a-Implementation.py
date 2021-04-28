#Für grafische Mitverfolgung
try:
	import matplotlib.pyplot as plt
except:
	pass
#Für Zeitmessung
import time
import math
#Zum Entfernen von störenden Zeichen bei Einlesen der Datei
import re
#Zum Kopieren von Listen in Listen
from copy import deepcopy

#Pfad der Datei
file = "stromrallye7.txt"

#Einlesen der Daten
with open(file, "r") as file:
	groesse = int(file.readline())
	#regex um Zeichen wie \n auszuschliessen
	roboter = [int(x) for x in (re.findall(r'\d+', file.readline()))]
	anzahl_batterien = int(file.readline())
	koordinaten_eingelesen = []
	for i in range(anzahl_batterien):
		koordinaten_eingelesen.append([int(x) for x in (re.findall(r'\d+', file.readline()))])

#Attribut für jede Ersatzbatterie hinzufügen, wenn die Batterie im Laufe des Weges noch nicht erreicht wurde --> 0, wenn schon --> 1
for o in range(len(koordinaten_eingelesen)):
	koordinaten_eingelesen[o].append(0)


#####################################################################################################################
#Bis Ende der Markierung für grafische Ausgabe

def grafisch_grid(gr_roboter, gr_koordinaten):
	grid = []
	#Gitter erstellen
	for i in range(groesse):
		grid.append(["*  "]*groesse)
	
	#Gitter füllen
	for p in range(len(gr_koordinaten)):
		if gr_koordinaten[p][2] > 10:
			grid[gr_koordinaten[p][1] - 1][gr_koordinaten[p][0] - 1] = str(gr_koordinaten[p][2]) + " "
		else:
			grid[gr_koordinaten[p][1] - 1][gr_koordinaten[p][0] - 1] = str(gr_koordinaten[p][2]) + "  "
	try:
		grid[gr_roboter[1]-1][gr_roboter[0]-1] = "X  "
	except:
		pass

	#Gitter zu string lesbar machen
	output = ""
	for f in range(len(grid)):	
		output = output + "".join(str(e) for e in grid[f]) + "\n"

	print("Batterieladung: " + str(roboter[2]))
	print(output)

def grafisch_batterietausch(gr_roboter, gr_koordinaten):
	for j in range(len(gr_koordinaten)):
		if gr_roboter[0] == gr_koordinaten[j][0] and gr_roboter[1] == gr_koordinaten[j][1]:
			gr_roboter[2], gr_koordinaten[j][2] = gr_koordinaten[j][2], gr_roboter[2]

	grafisch_grid(gr_roboter, gr_koordinaten)

def grafisch_bewegen(eingabe, gr_roboter):
	gr_roboter[0] = eingabe[0]
	gr_roboter[1] = eingabe[1]
	
	grafisch_batterietausch(gr_roboter, koordinaten_eingelesen)
	gr_roboter[2] -= 1
def grafisch(liste):
	for elem in liste:
		grafisch_bewegen(elem, roboter)
		time.sleep(0.2)
	print("Geschafft!")

#####################################################################################################################

#Überprüfen, ob eine Ersatzbatterie nicht erreichbar ist
def oballeine(roboter, koordinaten):
	for koord1 in koordinaten:
		erreichbar = []
		for koord2 in koordinaten:
			#Mindestabstand berechnen
			abstand = abs(koord2[0]- koord1[0]) + abs(koord2[1]- koord1[1])
			if abstand <= koord2[2] and abstand != 0:
				erreichbar.append(koord2)
		abstand_start = abs(roboter[0]- koord1[0]) + abs(roboter[1]- koord1[1])
		if abstand_start <= roboter[2]:
			erreichbar.append(roboter)
		if len(erreichbar) == 0:
			return 1



#Grundcheck am Anfang, teilweise kann direkt erkannt werden, dass eingelesene Spielsituation nicht möglich ist
def anfangscheck(roboter, groesse, koordinaten):
	#Anzahl der Ersatzbatterien mit Ladung 1 zählen, die keine Nachbarn haben
	eins_counter = 0
	for koordinate in koordinaten:
		if koordinate[2] == 1:
			obnachbarn = False
			for nachbar in [[koordinate[0] - 1, koordinate[1]], [koordinate[0] + 1, koordinate[1]], [koordinate[0], koordinate[1] - 1], [koordinate[0], koordinate[1] + 1]]:
				for koord in koordinaten:
					if nachbar == [koord[0], koord[1]] or nachbar == [roboter[0], roboter[1]]:
						obnachbarn = True
						break
			if obnachbarn == False:
				eins_counter += 1
	#wenn mehr als eine 1 ohne Nachbar --> Spiel nicht möglich
	if eins_counter > 1:
		print("Da es mehr als eine 1 gibt, die keinen Nachbarn hat, ist diese Spielsituation nicht lösbar")
		exit()
	#Wenn es eine Ersatzbatterie gibt, die nicht erreicht werden kann --> Spielabbruch
	if oballeine(roboter, koordinaten) == 1:
		print("Da mindestens eine Ersatzbatterie nicht erreichbar ist, ist diese Spielsituation nicht lösbar")
		exit()


#Berechnung der Summe der Ladungen aller Ersatzbatterien
def summersatzbatterien(koordinaten):
	summe = 0
	for ersatzbatterie in koordinaten:
		summe += ersatzbatterie[2]

	return summe

#Überprüfen, ob bereits alle Batterien erreicht wurden (durch am Anfang hinzugefügtes Attribut)
def summeerreichtebatterien(koordinaten):
	summe = anzahl_batterien
	for batterie in koordinaten:
		summe -= batterie[3]
	if summe == 0:
		for batterie in koordinaten:
			if batterie[2] != 0:
				if batterie[2] % 2 != 0:
					return 0
		return 1

#Überprüfen ob übergebener Punkt erreichbar ist, also er nicht umschlossen von Ersatzbatterien bzw. der Wand ist
def oberreichbar(standpunkt, endpunkt, ersatzbatterien, grid):
	nachbarn = [[endpunkt[0] - 1, endpunkt[1]], [endpunkt[0] + 1, endpunkt[1]], [endpunkt[0], endpunkt[1] - 1], [endpunkt[0], endpunkt[1] + 1]]
	daneben = 0
	for nachbar in nachbarn:
		if nachbar[0] == standpunkt[0] and nachbar[1] == standpunkt[1]:
			break
		if nachbar in ersatzbatterien:
			daneben += 1
		if 0 < nachbar[0] < grid+1 and 0 < nachbar[1] < grid+1:
			pass
		else:
			daneben += 1
	#wenn sie 4 Nachbarn bzw. Wand hat --> Ersatzbatterie ist nicht erreichbar
	if daneben == 4:
		return 1
	else:
		return 0


#Algorithmus A*
def a_stern(standpunkt, endpunkt, ladung, grid, hindernisse, alle_im_feld):
	#Zielpunkt aus Hindernissen entfernen
	hindernisse.remove(endpunkt)
	#open- und closed-list deklarieren
	open_list = []
	closed_list = []

	#startwert zur open list hinzufügen [koordinaten, g, h, f, vorheriger]
	open_list.append([standpunkt, 0, 0, 0, None])

	#solange es Einträge in der openlist gibt
	while len(open_list) > 0:
		#current bestimmen --> in open list mit niedrigstem f wert
		for i in range(len(open_list)):
			if open_list[i][3] == min([item[3] for item in open_list]):
				current = open_list[i]
				break

		#current aus open löschen und zu closed hinzufügen
		open_list.remove(current)
		closed_list.append(current)

		#wenn current ziel ist --> ende
		if current[0] == endpunkt:
			#Weg zurückverfolgen, in dem immer der "Parent"(Vorgänger) von jedem Punkt genommen wird, bis der "Parent" None ist
			weg = []
			weg.append(current[0])
			momentaner_wert = current[0]
			while momentaner_wert != None:
				for i in range(len(closed_list)):
					if closed_list[i][0] == momentaner_wert:
						weg.append(closed_list[i][4])
						momentaner_wert = closed_list[i][4]
			#reverse Liste und entfernen des Startpunktes
			weg = weg[::-1]
			weg = weg[1:]
			return weg

		#alle Richtungen der Nachbarn
		richtungen = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		neighbours = []

		#Nachbarn bestimmen und prüfen ob sie noch im Feld sind
		for richt in richtungen:
			position = [current[0][0] + richt[0], current[0][1] + richt[1]]
			#wenn Position im Feld
			if position in alle_im_feld:
				#und wenn Position nicht auf einem Hindernis(einer Ersatzbatterie)
				if position not in hindernisse:
					neighbours.append(position)

		#Über Nachbarn iterieren
		for neighbour in neighbours:
			#Wenn Nachbar in closed list ist --> überspringen
			if neighbour in [i[0] for i in closed_list]:
				continue
			#g, h und f bestimmen
			#g ist +10 von dem davor
			g = current[1] + 1
			#h mit Satz des Pythagoras ohne Wurzel bestimmen
			h = math.sqrt(((neighbour[0] - endpunkt[0])**2 + (neighbour[1] - endpunkt[1])**2))
			#f ist die Summe aus g und h
			f = g + h

			#Wenn der Nachbar bereits in open list ist, und der g wert dieses mal größer ist --> continue
			for elem in open_list:
				if elem[0] == neighbour: 
					if g > elem[1]:
						continue
					else:
						open_list.remove(elem)
			#Hinzufügen von Nachbar in open_list
			open_list.append([neighbour, g, h, f, current[0]])
	return

def aufruf_a_stern(standpunkt, ladung, groesse, koordinaten):
	#alle Koordinaten die im Feld sind
	alle_im_feld = []
	for i in range(1, groesse+1):
			for j in range(1, groesse+1):
				alle_im_feld.append([i, j])

	#die Koordinaten der Ersatzbatterien
	hindernisse = []
	ersatzbatterien = []
	for i in range(len(koordinaten)):
		hindernisse.append([koordinaten[i][0], koordinaten[i][1]])
		if [koordinaten[i][0], koordinaten[i][1]] != standpunkt:
			ersatzbatterien.append([koordinaten[i][0], koordinaten[i][1]])

	#Aufruf der Funktion a_stern für jede Ersatzbatterie
	alle_wege = []
	for endpunkt in ersatzbatterien:
		#Mindestabstand zwischen Startpunkt und Endpunkt ohne Hindernisse
		abstand = abs(endpunkt[0]- standpunkt[0]) + abs(endpunkt[1]- standpunkt[1])

		summe = summersatzbatterien(koordinaten)
		#Wenn der Abstand größer ist als die Summe aller Ersatzbatterien sowie der Ladung --> return, da eine Batterie nicht mehr erreichbar ist
		if abstand > summe + ladung:
			return 1
		#Wenn der Abstand größer ist als die Ladung --> continue mit nächster Batterie
		if abstand > ladung:
			continue
		#Wenn Funktion oberreichbar 0 zurückgibt (Batterie ist erreichbar) --> Aufruf der Funktion a_stern
		if oberreichbar(standpunkt, endpunkt, ersatzbatterien, groesse) == 0:
			weg = a_stern(standpunkt, endpunkt, ladung, groesse, hindernisse[:], alle_im_feld)
			#Hinzufügen von weg zu alle_wege
			alle_wege.append(weg)

	return alle_wege


#Rekursive Funktion "bewegen", um die letzte Ladung, die noch übrig geblieben ist und nirgenwo hinführt zu verbrauchen
def bewegen(startpunkt, koordinaten, richtung, richtungen, bewegen_liste):
	#Abbruchbedingung
	global stop
	if stop == True:
		return
	#Wenn die Ladung auf 0 ist --> stop
	if startpunkt[2] == 0:
		global letztekoordinaten
		letztekoordinaten = bewegen_liste
		stop = True
		return
	
	#Überprüfen ob Roboter auf diesen Punkt gehen kann
	x = startpunkt[0] + richtung[0]
	y = startpunkt[1] + richtung[1]
	if 0 < x <= groesse and 0 < y <= groesse:
		if [x,y] not in [[i[0],i[1]] for i in koordinaten_eingelesen]:
			#Richtung auf Koordinaten des Roboters addieren
			startpunkt[0] += richtung[0]
			startpunkt[1] += richtung[1]
			#Ladung um 1 verringern
			startpunkt[2] -= 1
		else:
			return
	else:
		return
	#Neue Koordinaten zu lokaler Liste hinzufügen um am Ende ein Ergbenis zu haben
	bewegen_liste.append([startpunkt[0], startpunkt[1]])

	#Funktion rekursiv aufrufen mit allen 4 Richtungen
	for elem in richtungen:
		bewegen(startpunkt[:], deepcopy(koordinaten), elem, richtungen[:], deepcopy(bewegen_liste))

#Überprüfen ob gefundener Weg geeignet ist
def obwegfertig(startpunkt, koordinaten, lokliste):
	#Weg für die letzte Ladung finden
	richtungen = [(1, 0), (-1, 0), (0, 1), (0, -1)]
	global stop
	stop = False
	global letztekoordinaten
	letztekoordinaten = []
	for elem in richtungen:
		bewegen(startpunkt[:], deepcopy(koordinaten), elem, richtungen[:], [])
	#Wenn nicht gefunden --> weiter nach einem Weg suchen
	if letztekoordinaten == []:
		return 0

	#Überprüfen ob übrig gebliebene Ladungen entfernt werden können
	else:
		ersatzbatterien = [[i[0], i[1]] for i in koordinaten]
		for koord in koordinaten:
			if koord[2] > 0:
				suchkoordinate = [koord[0], koord[1]]
				for index, elem in reversed(list(enumerate(lokliste))):
					if elem == suchkoordinate:
						#Überprüfen ob bei einem Punkt, an dem Ladung übrig geblieben ist, der Weg davor mindestens die Länge von 2 hatte
						if abs(index-2) == index-2:
							if lokliste[index - 1] in ersatzbatterien or lokliste[index-2] in ersatzbatterien:
							
								return 0
							#Die beiden Punkte vor Erreichen des Weges kopieren und so oft in Weg einfügen, sodass Ladung aufgebraucht ist
							else:
								davor = lokliste[index - 1]
								nochmaldavor = lokliste[index - 2]
								for i in range(koord[2]//2):
									lokliste.insert(index, nochmaldavor)
									lokliste.insert(index + 1, davor)
						else:
							davor = lokliste[index-1]
							nochmaldavor = [roboter[0],roboter[1]]
							for i in range(koord[2]//2):
									lokliste.insert(index, nochmaldavor)
									lokliste.insert(index + 1, davor)
	return lokliste
		
		

#Wahlweise Funktion, um aktuelle Berechnungen grafisch zu verfolgen --> In Zeile 414 nicht mehr auskommentieren
#(nur möglich wenn das Modul matplotlib installiert ist)
def matplot(koordinaten, startpunkt, wegliste, groesse):
	plt.plot(startpunkt[0], startpunkt[1], marker = "o", color="red")
	for elem in koordinaten:
		plt.plot(elem[0], elem[1], marker = "o", color="green")
	try:
		plt.plot([startpunkt[0], wegliste[0][0]],[startpunkt[1], wegliste[0][1]], color="blue")
	except:
		pass
	plt.plot([i[0] for i in wegliste], [i[1] for i in wegliste], color="blue")
	plt.xlim(0,groesse + 1)
	plt.ylim(groesse + 1, 0)
	plt.show()



#Hauptfunktion rekursiv
def rekursiv(startpunkt, groesse, koordinaten, ablage_batterie, lokliste, weg_davor, ebene):
	#Hinzufügen des vorherigen Weges zur lokalen Liste lokliste, in der am Ende der komplette Weg gespeichert ist
	lokliste = lokliste + weg_davor[1:]

	#Aktuellen Standort in der Liste "koordinaten" finden, um die Ablagebatterie dort abzulegen
	#Außerdem wird die Batterie als "bereits erreicht" markiert
	for j in range(len(koordinaten)):
		if koordinaten[j][0] == startpunkt[0] and koordinaten[j][1] == startpunkt[1]:
			koordinaten[j][2] = ablage_batterie
			koordinaten[j][3] = 1

	#Wenn alle Batterien als "bereits erreicht" markiert wurden
	if summeerreichtebatterien(koordinaten) == 1:
		#Wenn Funktion obwegfertig() nicht 0 zurückgibt, d.h. Weg geeignet ist --> Programm beenden und Weg sowie Laufzeit ausgeben
		#Danach Programm beenden
		obfertig = obwegfertig(startpunkt, deepcopy(koordinaten), deepcopy(lokliste))
		if obfertig != 0:
			ausgabeliste = obfertig + letztekoordinaten
			ausgabeliste.insert(0, [roboter[0], roboter[1]])
			print("Weg gefunden! Koordinaten des Weges: ", ausgabeliste)
			print(80*"=")
			print("Laufzeit:", time.time() - zeit)
			grafische = input("Grafische Ausgabe erwünscht?[J/n]")
			if grafische == "J" or grafische == "j":
				grafisch(ausgabeliste)
			exit()
		#Wenn Weg nicht geeignet ist --> weitersuchen
		else:
			pass

	#Wenn der momentane Startpunkte bereits in wege_dict gespeichert ist, d.h. alle Wege für diesen Punkt bereits berechnet wurden --> Wege übernehmen
	if str(startpunkt) in wege_dict:
		alle_wege = wege_dict[str(startpunkt)]
	#Sonst alle Wege suchen
	else:
		alle_wege = aufruf_a_stern([startpunkt[0], startpunkt[1]], startpunkt[2], groesse, koordinaten[:])
		#Wenn kein Weg gefunden wurde
		if alle_wege == 1:
			return
	#Alle Wege zum Dictionary hinzufügen
	wege_dict[str(startpunkt)] = alle_wege

	#Wahlweise Funktion um Suchen grafisch zu verfolgen
	#matplot(koordinaten, roboter, lokliste, groesse)

	#Für jeden Weg in alle_wege
	for weg in alle_wege:
		#Wenn der Weg "None" ist --> überspringen
		if weg == None:
			continue
		#Minimalen Batterieverbrauch berechnen
		mind_batterieverbrauch = len(weg) - 1
		#Wenn der minimale Batterieverbrauch größer als die momentane Ladung ist --> continue
		if mind_batterieverbrauch > startpunkt[2]:
			continue

		#Neuen Startpunkt bestimmen
		for l in range(len(koordinaten)):
			if koordinaten[l][0] == weg[-1][0] and koordinaten[l][1] == weg[-1][1]:
				neuer_startpunkt = koordinaten[l]
		#Wenn der neue Startpunkt eine Ladung von 0 hat --> mit nächstem Weg weitermachen
		if neuer_startpunkt[2] == 0:
			continue

		#rekursiver Aufruf der Funktion
		rekursiv(neuer_startpunkt[:], groesse, deepcopy(koordinaten), startpunkt[2] - mind_batterieverbrauch, deepcopy(lokliste), deepcopy(weg), ebene + 1)


def main():
	global wege_dict
	wege_dict = {}
	#Zeitstart
	global zeit
	zeit = time.time()
	#Grundüberprüfung, ist eingelesene Spielsituation möglich?
	anfangscheck(roboter, groesse, koordinaten_eingelesen)
	#Aufruf der Rekursion
	rekursiv(roboter[:], groesse, deepcopy(koordinaten_eingelesen), 0, [], [], 0)

	#Wenn kein Weg gefunden wurde
	print("Es wurde kein Weg gefunden.")
	print(time.time() - zeit)

main()


