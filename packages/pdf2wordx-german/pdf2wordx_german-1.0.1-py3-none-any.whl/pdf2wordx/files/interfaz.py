from tkinter import Button,Label,Entry,Tk

# Klasse, die das Basisfenster erstellt
class Window:
	def __init__(self,root:any,width:int=300,height:int=300,bgColor:str='green',title:str='Window',resizable:list=[False,False]) -> None:
		self.root=root
		self.width=width
		self.height=height
		self.bgColor=bgColor
		self.title=title
		self.resizable=resizable
		self.__window()

	# Methode, die das Fenster mit seinen Attributen erstellt
	def __window(self) -> None:
		self.root['bg']=self.bgColor
		self.root.title(self.title)
		self.root.geometry(f'{self.width}x{self.height}{self.__centerWindow()}')
		self.root.resizable(self.resizable[0],self.resizable[1])

	# Fenster zentrieren
	def __centerWindow(self) -> str:
		screenWidth:int=self.root.winfo_screenwidth()
		screenHeight:int=self.root.winfo_screenheight()
		winWidthCenter:int=(screenWidth-self.width)//2
		winHeightCenter:int=(screenHeight-self.height)//2
		geometry:str=f'+{winWidthCenter}-{winHeightCenter}'
		return geometry

	# Hauptfenster-Schleife
	def loopWindow(self):
		self.root.mainloop()

# Klasse für die Widgets
class Widgets:
	def __init__(self,master:any,elements:list) -> None:
		self.master=master # Tk Fenster
		self.elements=elements # [[element],...,n,[element]]
		self.widgetsList=[] # [Elemente auf dem Bildschirm]
		self.configItems=[]

	# Gleiche Buttons erstellen
	def widgetsCreate(self,itemsOptions:list[dict]=[{}],package:list=[],optionsPack:list[dict]=[{}]):
		try:
			# Zugriff sowohl auf Index als auch auf das Element |0,Button| |1,Label|
			for i,item in enumerate(self.elements):
				# Programmfluss steuern, prüfen, ob i kleiner als die Länge von "itemsOptions" ist
				self.__createWidget(itemsOptions,package,optionsPack,i,item)
		except Exception as e:
			print('Fehler in normalButton(): ',e)

	def __createWidget(self,opcionItem,packType,packOps,i,widget):
		if self.__verifyIndexRange(i,opcionItem):
			# widget ist das Element mit seinen Attributen: Button(master=tkinter.Tk(),text='Click Me',command=click)
			widget = widget(self.master,opcionItem[i])
			# Jedes Widget wird der Widgetliste hinzugefügt (falls später zusätzliche Informationen benötigt werden)
			self.widgetsList.append(widget)
			# Attribute des Elements abrufen
			self.__getAtributtesItem(opcionItem[i])
			# Prüfen, ob i kleiner als die Länge von "packOps" ist
			self.__choosePackOptions(i,packOps,packType,widget)
			

	def __choosePackOptions(self,i,opPack,packList,wid):
		if self.__verifyIndexRange(i,opPack):
			if i < len(packList):
				# Variante 1, um __packItem() fehlerfrei aufzurufen
				self.__packItem(wid,packList[i],opPack[i])
			else:
				# Variante 1, um __packItem() fehlerfrei aufzurufen
				self.__packItem(wid,opPack[i])
		else:
			self.__exePack(i,packList,wid)
	
	def __exePack(self,pos,packs,wid):
		if pos < len(packs):
			# Wenn i größer als "opPack" ist, bedeutet das, dass es nicht existiert
			# und daher dieses Element seine Konfigurationen (configure()) leer hat
			self.__packItem(wid,packs[pos])
		else:
			# Wenn i größer als "opPack" ist, bedeutet das, dass es nicht existiert
			# und daher dieses Element seine Konfigurationen (configure()) leer hat
			self.__packItem(wid)

	# Methode zum Verpacken der Elemente, einzeln
	def __packItem(self,item:any,typePack:str='pack',opsPack:dict={}):
		# Es wird geprüft, ob "typePack" eine gültige Methode ist, z.B. bei 'pack': item.pack()
		# Gibt True oder False zurück
		# getattr(item,typePack) -> item.typePack()
		if callable(getattr(item,typePack)):
			# Die Verpackungsmethode wird aufgerufen und erhält die entsprechenden Optionen
			getattr(item,typePack)(opsPack)

	# Attribute jedes Items zur Konfigurationsliste hinzufügen
	def __getAtributtesItem(self,option):
		self.configItems.append(option)

	def getText(self,pos):
		return self.widgetsList[pos].get()

	def __verifyIndexRange(self,value,item):
		if value < len(item):
			return True
		else:
			return False


if __name__ == '__main__':
	# Klasse, die alle Teile zusammenführt und ausführt
	class App(Window):
		def __init__(self,root:any,width:int,height:int,colorBg:str,title:str):
			Window.__init__(self,root,width,height,colorBg,title)
			self.root=root
			self.elements=[Button,Label,Entry,Entry]
			# Widgets-Objekte
			self.widgets=Widgets(self.root,self.elements)
			self.elementsOptions=[
							{'width':3,'wrap':5,'text':'Say Hello','bg':'yellow'},
							{'text':'Hello World','fg':'green','bg':'Black'},
							{'bg':'red','fg':'white','font':('Helvetica',10,'bold')},
							{'bg':'green','fg':'white','font':12,'insertwidth':2}
						]
			self.elementsPack=['pack','pack','place']
			self.optionsPack=[
							{'fill':'both','expand':False,'side':'right'},
							{'expand':True},
							{'relx':0.3,'rely':0.2}
						]
			
			# Methode zum Erstellen der Buttons
			self.widgets.widgetsCreate(self.elementsOptions,self.elementsPack,self.optionsPack)
			
			# Befehl zum Button hinzufügen
			self.widgets.widgetsList[0].configure(command=lambda:self.click(self.widgets.getText(2)))

		# Text aus einem Entry holen
		def click(self,txt):
			#txt=item.get()
			self.widgets.widgetsList[1].configure(text=f'Hello {txt}')

	tk=Tk()
	app=App(tk,300,200,'Black','Window')
	tk.mainloop()