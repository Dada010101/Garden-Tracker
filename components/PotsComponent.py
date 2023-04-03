import tkinter as tk
from tkinter import ttk, StringVar, messagebox
from datasources.dto.Pots import Pots
from datasources.tk.TkPotsSimulatedValues import TkPotsSimulatedValues
from services.PotsService import PotsService
from components.PlantsComponent import PlantsComponent
from services.PlantsService import PlantsService
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime as dt


class PotsComponent(ttk.LabelFrame):

    def __init__(self, parent, row, column, service: PotsService):
        super().__init__(master=parent, text="Posude")
        self.grid(row=row, column=column, padx=5, pady=5)
        self.welcomeWindow = parent
        self.service = service
        self.tkPots = TkPotsSimulatedValues()
        self.potsDto = Pots()
        self.setView()

    def setView(self):
        print(self.tkPots.name)
        self.pots = ttk.Frame(self)
        self.pots.grid(row=0, column=0)

        self.lbPots = tk.Listbox(self.pots)
        self.lbPots.grid(row=0, column=0, pady=5, padx=5, rowspan=5)
        self.lbPots.bind("<Double-1>", self.selectPotFromList)
        print(self.tkPots.name)
        self.fetchAndSetPotsList()
        print(self.tkPots.name)

        btnAddNewPot = ttk.Button(self.pots, text="Dodaj novu posudu", command=self.addNewPot)
        btnAddNewPot.grid(row=5, column=0, pady=5, padx=5)

        lblname = ttk.Label(self.pots, text="Name:")
        lblname.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        name = ttk.Entry(self.pots, textvariable=self.tkPots.name)
        name.grid(row=0, column=2, padx=5, pady=5, sticky=tk.EW)

        lblPlantName = ttk.Label(self.pots, text="Plant name:")
        lblPlantName.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)

        plantName = ttk.Entry(self.pots, textvariable=self.tkPots.plantName)
        plantName.grid(row=1, column=2, padx=5, pady=5, sticky=tk.EW)

        lblTemperature = ttk.Label(self.pots, text="Temperature:")
        lblTemperature.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        temperature = ttk.Entry(self.pots, textvariable=self.tkPots.temperature)
        temperature.grid(row=2, column=2, padx=5, pady=5)

        lblHunmidity = ttk.Label(self.pots, text="Humidity:")
        lblHunmidity.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        humidity = ttk.Entry(self.pots, textvariable=self.tkPots.humidity)
        humidity.grid(row=3, column=2, pady=5, padx=5)

        lblSimulate = ttk.Label(self.pots, text="\nSimulate values\n", font=("Arial", 14))
        lblSimulate.grid(row=6, column=0)

        lblTemperature = ttk.Label(self.pots, text="Temperature: ")
        lblTemperature.grid(row=7, column=0, pady=5, padx=5, sticky=tk.NW)
        scaleTemperature = ttk.Scale(self.pots, from_=-30, to=60, variable=self.tkPots.temperature)
        scaleTemperature.grid(row=7, column=1, pady=5, padx=5, sticky=tk.W)
        lblSimTemp = ttk.Label(self.pots, textvariable=self.tkPots.temperature)
        lblSimTemp.grid(row=7, column=2, padx=5, pady=5)

        lblHumidity = ttk.Label(self.pots, text="Humidity: ")
        lblHumidity.grid(row=8, column=0, pady=5, padx=5, sticky=tk.NW)
        scaleHumidity = ttk.Scale(self.pots, from_=950, to=1100, variable=self.tkPots.humidity)
        scaleHumidity.grid(row=8, column=1, pady=5, padx=5, sticky=tk.W)
        lblSimHumidity = ttk.Label(self.pots, textvariable=self.tkPots.humidity)
        lblSimHumidity.grid(row=8, column=2, padx=5, pady=5)

        self.lblPhotosPlant = ttk.Label(self.pots, image=None)
        self.lblPhotosPlant.grid(row=0, column=3, pady=5, padx=5, rowspan=5)

        btnSave = ttk.Button(self.pots, text="Save simulated values", command=self.saveSimValues)
        btnSave.grid(row=9, column=0, padx=10, pady=10, columnspan=1)

    def addNewPot(self):

        self.top = tk.Toplevel(self)
        self.top.geometry("400x400")

        self.top.title("Add new pot")

        self.lblPot = ttk.Label(self.top, text="Unesite naziv posude: ")
        self.lblPot.grid(row=1, column=0, pady=5, padx=5)
        self.lblEntryPot = StringVar()
        self.lblEntryPot = ttk.Entry(self.top)
        self.lblEntryPot.grid(row=1, column=2, pady=5, padx=5)

        self.lblPlant = ttk.Label(self.top, text="Unesite naziv biljke: ")
        self.lblPlant.grid(row=2, column=0, pady=5, padx=5)
        self.lblEntryPlant = StringVar()
        self.lblEntryPlant = ttk.Entry(self.top)
        self.lblEntryPlant.grid(row=2, column=2, pady=5, padx=5)

        btnSave = ttk.Button(self.top, text="Save", command=self.addNew)
        btnSave.grid(row=3, column=0, columnspan=3, rowspan=2, padx=5, pady=5, sticky=tk.EW)

    def addNew(self):

        newPotName = self.lblEntryPot.get()
        plantname = self.lblEntryPlant.get()
        self.service.addPot(newPotName, plantname)
        self.fetchAndSetPotsList()
        self.top.destroy()

    def selectPotFromList(self, event):
        self.selectedIndex = event.widget.curselection()
        potsDto: Pots = self.potsList[self.selectedIndex[0]]
        self.tkPots.fillFromDto(potsDto)

        btnChangeInfo = ttk.Button(self.pots, text="Update", command=self.saveSimValues)
        btnChangeInfo.grid(row=5, column=2, pady=5, padx=5, sticky=tk.E)
        btnDeletePot = ttk.Button(self.pots, text="Izbrisi", command=self.deletePot)
        btnDeletePot.grid(row=5, column=2, padx=5, pady=5, sticky=tk.W)
        self.lblInfo = ttk.Label(self.pots, text="Stanje biljke: ", font=("Arial", 14))
        self.lblInfo.grid(row=5, column=3, padx=5, pady=5)
        self.info = tk.StringVar(value="")
        self.lblEntryInfo = ttk.Label(self.pots, textvariable=self.info)
        self.lblEntryInfo.grid(row=6, column=3, pady=5, padx=5)
        self.btnSync = ttk.Button(self.pots, text=" SYNC ", command=self.syncValues)
        self.btnSync.grid(row=9, column=1, sticky=tk.E)
        a = ttk.Button(self.pots, text="Graf", command=self.graf)
        a.grid(row=9, column=2)
        self.changeImage()
        self.syncValues()

    def graf(self):

        fig, ax = plt.subplots()
        names = ["Temperature", "Humidity"]
        marks = [self.tkPots.temperature.get(), self.tkPots.humidity.get()]
        ax.bar(names, marks)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid(row=0, column=4)

    def saveSimValues(self):
        potsDto = Pots.createFromTkModel(self.tkPots)
        if self.tkPots.temperature and self.tkPots.humidity == None:
            self.service.updatePot(potsDto)
            self.service.updateTime()
            self.changeImage()
            self.fetchAndSetPotsList()
        else:
            self.service.updatePot(potsDto)
            self.changeImage()
            self.fetchAndSetPotsList()
            self.syncValues()

    def clearInfo(self):
        self.lblEntryInfo.grid_remove()

    def deletePot(self):

        potvrda = messagebox.askyesno("Potvrda", "Potvrdite brisanje")
        if potvrda:
            self.service.deletePot(self.tkPots.id)
            self.fetchAndSetPotsList()
            self.tkPots.clear()

    def syncValues(self):

        if self.tkPots.temperature.get() >= 25:
            self.info.set("Potrebno zalijevanje")
        elif self.tkPots.temperature.get() < 25 and self.tkPots.temperature.get() > 15:
            self.info.set("Ok")
        else:
            self.info.set("Potrebno pregledati biljku")

    def fetchAndSetPotsList(self):

        self.potsList = self.service.getAllPots()
        simplifiedPotsList = []
        for pot in self.potsList:
            p: Pots = pot
            simplifiedPotsList.append(p.getInfo())
        self.tkPotsList = StringVar(value=simplifiedPotsList)
        self.lbPots.config(listvariable=self.tkPotsList)

    def changeImage(self):

        plantName = self.tkPots.plantName.get()
        if plantName == "Origano":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgOrigano)
        elif plantName == "Ruzmarin":
            #self.clearInfo()
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgRuzmarin)
        elif plantName == "Bosiljak":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgBosiljak)
            self.lblEntryInfo.config(text="")
        elif plantName == "Lovor":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgLovor)
            self.lblEntryInfo.config(text="")
        elif plantName == "Kopar":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgKopar)
            self.lblEntryInfo.config(text="")
        elif plantName == "Paprika":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgPaprika)
            self.lblEntryInfo.config(text="")
        elif plantName == "Rajcica":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgPoma)
            self.lblEntryInfo.config(text="")
        elif plantName == "Tikvica":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgTikvica)
            self.lblEntryInfo.config(text="")
        elif plantName == "Feferon":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgFeferon)
            self.lblEntryInfo.config(text="")
        elif plantName == "Maslina":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgMaslina)
            self.lblEntryInfo.config(text="")
        else:
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkNoImg)
            self.lblEntryInfo.config(text="")
            print("No profile photo")

