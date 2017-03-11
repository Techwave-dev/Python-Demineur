#!/usr/bin/python
#-*-coding: utf-8 -*-

from Tkinter import *
import Tkinter
import tkMessageBox
import random
import tkFont

#TODO redimensionnement fenetre
#TODO message pour recommencer
#TODO ajouter les drapeaux

class NbEntry(Tk):
	def __init__(self):
		Tk.__init__(self)
		
		self.title("Configuration")
		
		self.label = Label(self, text="Entrer le nombre de cases sur le coté")
		self.label.pack()
		self.entry = Entry(self)
		self.entry.pack()
		self.valider = Button(self, text="Valider", command=self.valider)
		self.valider.pack()
		
	def valider(self):
		try:
			nbCases = int(self.entry.get())
			if nbCases < 8:
				tkMessageBox.showerror("Erreur", "Le nombre doit être supérieur ou égal à 8!")
				return
			
			self.destroy()
			window = MainWindow(nbCases)
			window.mainloop()
		except ValueError:
			tkMessageBox.showerror("Erreur", "Vous devez rentrer un nombre!")
			return

class MainWindow(Tk):

	def __init__(self, nbCases):
		Tk.__init__(self)
		
		self.gris = "u"
		self.bombe = "b"
		self.drapeau = "d"
		self.ras = "r"
		
		self.nbCases = nbCases
		self.nbBombes = random.randrange(((nbCases*nbCases)*5)/100)+((nbCases*nbCases)*15)/100
		print str(self.nbBombes)
		
		self.title("Démineur")
		
		self.initValue()
		self.font = tkFont.Font(family="Times", size=int(480.0/nbCases-(480.0/nbCases)/8), weight="bold", underline=1)
		self.fontScores = tkFont.Font(family="Times", size=int(480.0/nbCases-(480.0/nbCases)/8))
		
		self.canvas = Canvas(width=480, height=480)
		self.canvas.pack()
		self.tileSize = 480.0 / self.nbCases
		self.indic = Label(self, text="Clique gauche pour découvrir la case, Clique droit pour poser un drapeau")
		self.indic.pack()
		
		self.canvas.bind("<Button-1>", self.clicCase)
		self.canvas.bind("<Button-3>", self.placerDrapeau)
		self.bind("<Return>", self.restart)
		self.bind("<F1>", self.activeDebug)
		#self.bind("<Configure>", self.resize)
		
		self.loop()
		
	def resize(self, event):
		minValue = min(event.width, event.height)
		self.tileSize = float(minValue) / len(self.gameState)
		self.canvas.configure(width=minValue, height=minValue)
		
	def activeDebug(self, event):
		if self.debug:
			self.debug = False
		else:
			self.debug = True
		
	def restart(self, event):
		if self.aGagner or self.aPerdu:
			self.initValue()
			
	def initValue(self):
		self.aGagner = False
		self.aPerdu = False
		self.debug = False
		
		self.gameState = []
		for i in range(self.nbCases):
			self.gameState.append(self.gris*self.nbCases)
			
		self.mapActuel = []
		for i in range(self.nbCases):
			self.mapActuel.append(self.gris*self.nbCases)
		self.createBombs()
		
	def createBombs(self):
		for i in range(self.nbBombes):
			x = random.randrange(self.nbCases)
			y = random.randrange(self.nbCases)
			self.gameState[y] = setChar(self.gameState[y], x, self.bombe)
			
		self.updateNumbers()
		
	def updateNumbers(self):
		for y in range(self.nbCases):
			for x in range(self.nbCases):
				nb = 0
				if self.gameState[y][x] == self.bombe:
					continue
				for yMalus in range(-1, 2):
					for xMalus in range(-1, 2):
						if xMalus == 0 and yMalus == 0:
							continue
						if x + xMalus < 0 or x + xMalus > self.nbCases - 1:
							continue
						if y + yMalus < 0 or y + yMalus > self.nbCases - 1:
							continue
							
						if self.gameState[y+yMalus][x+xMalus] == self.bombe:
							nb = nb + 1
				self.gameState[y] = setChar(self.gameState[y], x, str(nb))
			
	def loop(self):
		if self.gagnant():
			self.aGagner = True

		self.render()

		self.after(1000/60, self.loop)

	def render(self):
		self.canvas.delete(ALL)
		
		for i in range(0, len(self.gameState)+1):
			self.canvas.create_line(0, i*self.tileSize, self.canvas.winfo_width(), i*self.tileSize, fill="#000000")
		for j in range(0, len(self.gameState)+1):
			self.canvas.create_line(j * self.tileSize, 0, j * self.tileSize, self.canvas.winfo_height(), fill="#000000")
			
		for i in range(self.nbCases):
			for j in range(self.nbCases):
				if self.mapActuel[i][j] == self.drapeau:
					self.canvas.create_rectangle(j * self.tileSize, i * self.tileSize, j * self.tileSize + self.tileSize, i * self.tileSize + self.tileSize, fill="#00FFFF")
				if self.mapActuel[i][j] == self.ras:
					self.canvas.create_rectangle(j * self.tileSize, i * self.tileSize, j * self.tileSize + self.tileSize, i * self.tileSize + self.tileSize, fill="#999999")
					self.canvas.create_text(j * self.tileSize + self.tileSize/2, i * self.tileSize + self.tileSize/2, text=self.gameState[i][j], font=self.fontScores)
				if self.gameState[i][j] == self.bombe and (self.aPerdu or self.debug):
					self.canvas.create_rectangle(j * self.tileSize, i * self.tileSize, j * self.tileSize + self.tileSize, i * self.tileSize + self.tileSize, fill="#FF0000")
				
		if self.aGagner:
			pass
			
		if self.aPerdu:
			pass
			
			
	def gagnant(self):
		for x in range(self.nbCases):
			for y in range(self.nbCases):
				if self.mapActuel[y][x] != self.ras and self.gameState[y][x] != self.bombe:
					return False
		return True
		
		
	def clicCase(self, event):
		if self.aGagner or self.aPerdu:
			return
			
		y = event.y / self.tileSize
		x = event.x / self.tileSize
		
		y = int(y)
		x = int(x)
		
		self.decouvrirCase(x, y)
		
	def decouvrirCase(self, x, y):		
		if self.gameState[y][x] == self.bombe:
			self.aPerdu = True 
		
		if self.mapActuel[y][x] == self.ras:
			return
			
		else:
			self.mapActuel[y] = setChar(self.mapActuel[y], x, self.ras)
			if self.gameState[y][x] == "0":
				for yMalus in range(-1, 2):
						for xMalus in range(-1, 2):
							if xMalus == 0 and yMalus == 0:
								continue
							if x + xMalus < 0 or x + xMalus > self.nbCases - 1:
								continue
							if y + yMalus < 0 or y + yMalus > self.nbCases - 1:
								continue
							self.decouvrirCase(x+xMalus, y+yMalus)
		
	def placerDrapeau(self, event):
		if self.aGagner or self.aPerdu:
			return
			
		y = event.y / self.tileSize
		x = event.x / self.tileSize
		
		y = int(y)
		x = int(x)
		
		#self.mapActuel[y] = setChar(self.mapActuel[y], x, self.drapeau)
		
def setChar(string, index, char):
	string = string[:index] + char + string[index+1:]
	return string
	
if __name__ == "__main__":
	window = NbEntry()
	window.mainloop()
