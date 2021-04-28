from random import randint
from random import choice
import math


#Bis zu der Markierung nur für grafische Ausgabe

def grid():
	grid = []
	#Gitter erstellen
	for i in range(groesse):
		grid.append(["*  "]*groesse)
	
	#Gitter füllen
	for p in range(len(koordinaten)):
		if koordinaten[p][2] >= 10:
			grid[koordinaten[p][1] - 1][koordinaten[p][0] - 1] = str(koordinaten[p][2]) + " "
		else:
			grid[koordinaten[p][1] - 1][koordinaten[p][0] - 1] = str(koordinaten[p][2]) + "  "

	grid[startpunkt[1]-1][startpunkt[0]-1] = "X  "

	#Gitter zu string lesbar machen
	output = ""
	for f in range(len(grid)):	
		output = output + "".join(str(e) for e in grid[f]) + "\n"

	return output

def bewegen(x, y):
	if 0 < startpunkt[0] + x <= groesse and 0 < startpunkt[1] + y <= groesse and startpunkt[2] > 0:
		startpunkt[0] += x
		startpunkt[1] += y
		startpunkt[2] -= 1
		batterietausch()
	else:
		print("Out of grid")

def batterietausch():
	for j in range(len(koordinaten)):
		if startpunkt[0] == koordinaten[j][0] and startpunkt[1] == koordinaten[j][1]:
			startpunkt[2], koordinaten[j][2] = koordinaten[j][2], startpunkt[2]

def obfertig():
	summe = 0
	if startpunkt[2] == 0:
		for k in range(len(koordinaten)):
			summe += koordinaten[k][2]
		if summe == 0:
			print("Glückwunsch!")
		else:
			print("Leider verloren :(")
		exit()

def main_grafik():

	while True:
		print("Batterieladung:" + str(startpunkt[2]))
		print(grid())
		inp = input("u=up, d=down, r=right, l=left")
		if inp == "u":
			bewegen(0, -1)
		elif inp == "d":
			bewegen(0, 1)
		elif inp == "r":
			bewegen(1, 0)
		elif inp == "l":
			bewegen(-1, 0)
		else:
			print("Try again")

		obfertig()

############################################################################################################################
############################################################################################################################
############################################################################################################################
#Funktion und Aufrufe des Hauptprogramms


def a_stern(standpunkt, endpunkt, groesse, hindernisse, alle_im_feld):
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
				#print(current)
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



def wegfinden(startpunkt, alle_im_feld, groesse):
	while True:
		#Random naechste Batterie aus ersatzbatterien nehmen
		naechste_batterie = choice(ersatzbatterien)
		if naechste_batterie == startpunkt:
			continue
		#Hindernisse auflisten
		hindernisse = []
		for i in range(len(ersatzbatterien)):
			if [ersatzbatterien[i][0], ersatzbatterien[i][1]] != naechste_batterie[:-1]:
				hindernisse.append([ersatzbatterien[i][0], ersatzbatterien[i][1]])
			else:
				#"bereits erreicht" Index auf 1 setzen
				ersatzbatterien[i][2] = 1

		#schnellsten Weg suchen
		weg = a_stern(startpunkt, [naechste_batterie[0], naechste_batterie[1]], groesse, hindernisse, alle_im_feld)
		#wenn nicht gefunden, anderen naechsten Punkt nehmen
		if weg == None:
			continue
		#Weg in Liste speichern
		global alle_wege
		alle_wege.append([startpunkt, naechste_batterie, len(weg)-1])
		return naechste_batterie

#Berechnet ob bereits alle Batterien mindestens einmal erreicht wurden
def summeerreichtebatterien(anzahl_batterien):
	summe = anzahl_batterien
	for batterie in ersatzbatterien:
		summe -= batterie[2]
	if summe == 0:
		return 1
	return

#Berechnet die Ladungen der Ersatzbatterien
def ladungen():
	koordinaten = []
	neue_ladung = 0
	for i in range(len(alle_wege)):
		changed = False
		for j in range(len(koordinaten)):
			#wenn Ersatzbatterie bereits mindestens einmal im Weg erreicht wurde
			if [koordinaten[j][0], koordinaten[j][1]] == [alle_wege[i][1][0], alle_wege[i][1][1]]:
				changed = True
				#neue Ladung für den nächsten Weg mitnehmen
				temp_neue_ladung = koordinaten[j][2]
				if neue_ladung:
					koordinaten[j][2] =  alle_wege[i][2]+neue_ladung
					neue_ladung = 0
				else:
					#aktuelle Ladung speichern
					koordinaten[j][2] =  alle_wege[i][2]
				neue_ladung = temp_neue_ladung
				break
		#wenn Ersatzbatterie bereits geändert wurde --> weiter mit der nächsten
		if changed == True:
			continue
		#sonst neue Ersatzbatterie in Liste koordinaten[] anlegen
		else:
			if neue_ladung:
				koordinaten.append([alle_wege[i][1][0], alle_wege[i][1][1], alle_wege[i][2]+neue_ladung])
				neue_ladung = 0
			else:
				koordinaten.append([alle_wege[i][1][0], alle_wege[i][1][1], alle_wege[i][2]])
	return koordinaten


def main():
	#Attribute des Schwierigkeitsgrades
	global groesse
	if schwierigkeitsgrad == 0:
		groesse = 5
		anzahl_batterien = randint(2,5) + 1
	elif schwierigkeitsgrad == 1:
		groesse = 10
		anzahl_batterien = randint(10, 15) + 1
	elif schwierigkeitsgrad == 2:
		groesse = 20
		anzahl_batterien = randint(40, 60) + 1

	#Startpunkt ermitteln
	startpunkt = [randint(1, groesse), randint(1, groesse)]
	print("Groesse des Spielfelds:", groesse, " Anzahl der Batterien:", anzahl_batterien-1)
	global ersatzbatterien
	ersatzbatterien = []
	global alle_wege
	alle_wege = []
	#alle Koordinaten im Feld in Liste speichern
	alle_im_feld = []
	for i in range(1, groesse+1):
			for j in range(1, groesse+1):
				alle_im_feld.append([i, j])

	#random Ersatzbatterien im Feld platzieren
	i = 0
	while i < anzahl_batterien:

		x = randint(1, groesse)
		y = randint(1, groesse)
		if [x,y,0] not in ersatzbatterien and [x,y] != startpunkt:
			ersatzbatterien.append([x,y,0])
			i += 1
	while True:
		startpunkt = wegfinden(startpunkt, alle_im_feld, groesse)
		if summeerreichtebatterien(anzahl_batterien) == 1:
			return

def writetofile(file, startpunkt, anzahl_batterien, groesse):
	string = ""
	groesse_string = str(groesse) + "\n"
	startpunkt_string = str(startpunkt).replace("[", "").replace("]", "").replace(" ", "") + "\n"
	anzahl_batterien_string = str(anzahl_batterien) + "\n"
	string += groesse_string + startpunkt_string + anzahl_batterien_string
	for koord in koordinaten:
		string += str(koord).replace("[", "").replace("]", "").replace(" ", "") + "\n"
	
	file = open(file, "w")
	file.write(string)

def eingabe():
	while True:
		try:
			eingabe = int(input("Schwierigkeitsgrad bitte eingeben: '0'-> einfach, '1' -> mittel, '2' -> schwer"))
			if eingabe == 0 or eingabe == 1 or eingabe == 2:
				return eingabe
				break
			else:
				print("Try again")
				continue
		except ValueError:
			print("Bitte geben Sie einen Integer ein")

global schwierigkeitsgrad
schwierigkeitsgrad = eingabe()
"""
Einfach: groesse = 5, anzahl_batterien zwischen 8% und 20% des Feldes
Mittel: groesse = 10, anzahl batterien zwischen 10% und 15% des Feldes
Schwer: groesse = 20, anzahl_batterien zwischen 10% und 15% des Feldes
"""
main()
koordinaten = ladungen()
startpunkt = koordinaten.pop(-1)
#möglich, Beispiel zu Datei zu schreiben
#writetofile("stromrallyebeispiel.txt", startpunkt, len(koordinaten), groesse)
main_grafik()
