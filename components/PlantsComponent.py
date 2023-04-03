from tkinter import ttk, IntVar, BooleanVar, DoubleVar, StringVar, messagebox
import tkinter as tk
from datasources.tk.TkPlants import TkPlants
from datasources.dto.Plants import PlantsDTO
from services.PlantsService import PlantsService


class PlantsComponent(ttk.LabelFrame):

    def __init__(self, parent, row, column, service: PlantsService):
        super().__init__(master=parent, text="Plants")
        self.grid(row=row, column=column, padx=5, pady=5)
        self.welcomeWindow = parent
        self.service = service
        self.tkPlants = TkPlants()
        self.plantDTO = PlantsDTO()
        self.setView()

    def setView(self):

        self.plants = ttk.Frame(self)
        self.plants.grid(row=0, column=0)

        self.lbPlants = tk.Listbox(self.plants, font=("Arial", 12))
        self.lbPlants.grid(row=0, column=0, pady=5, padx=5, rowspan=5)
        self.lbPlants.bind("<Double-1>", self.selectPlantFromList)

        self.fetchAndSetPlantList()

        lblname = ttk.Label(self.plants, text="Name:")
        lblname.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.name = ttk.Label(self.plants, textvariable=self.tkPlants.name, font=("Arial", 14))
        self.name.grid(row=0, column=2, padx=5, pady=5, sticky=tk.EW)

        lblPlantName = ttk.Label(self.plants, text="Karakteristike: ")
        lblPlantName.grid(row=1, column=1, pady=5, padx=5, sticky=tk.NW)
        self.infoVar = tk.StringVar
        self.lbPlantsInfo = tk.Text(self.plants, font=("Arial", 12))
        self.lbPlantsInfo.config(height=10, width=16)#, state=tk.DISABLED)
        self.lbPlantsInfo.grid(row=1, column=2)

        self.lblPhotosPlant = ttk.Label(self.plants, image=None)
        self.lblPhotosPlant.grid(row=0, column=3, pady=5, padx=5, rowspan=5)

        btnAddNewPot = ttk.Button(self.plants, text="Dodaj novu biljku", command=self.addNewPlant)
        btnAddNewPot.grid(row=5, column=0, pady=5, padx=5)

    def addNewPlant(self):

        self.top2 = tk.Toplevel(self)
        self.top2.geometry("400x400")

        self.top2.title("Add new plant")

        self.lblPlant = ttk.Label(self.top2, text="Unesite naziv biljke: ")
        self.lblPlant.grid(row=1, column=0, pady=5, padx=5)
        self.lblEntryPlant = StringVar()
        self.lblEntryPlant = ttk.Entry(self.top2)
        self.lblEntryPlant.grid(row=1, column=2, pady=5, padx=5)

        self.lblPlantChar = ttk.Label(self.top2, text="Unesite karakteristike: ")
        self.lblPlantChar.grid(row=2, column=0, pady=5, padx=5, sticky=tk.NE)
        self.lblEntryPlantChar = StringVar()
        self.lblEntryPlantChar = tk.Text(self.top2)
        self.lblEntryPlantChar.config(height=10, width=16)
        self.lblEntryPlantChar.grid(row=2, column=2)

        btnSave = ttk.Button(self.top2, text="Save", command=self.addNew)
        btnSave.grid(row=3, column=0, columnspan=3, rowspan=2, padx=5, pady=5, sticky=tk.EW)

    def addNew(self):

        newPlanttName = self.lblEntryPlant.get()
        char = self.lblEntryPlantChar.get("1.0","end-1c")
        self.lbPlantsInfo.insert(tk.END, char)
        self.service.addPlant(newPlanttName, char)
        self.fetchAndSetPlantList()
        self.top2.destroy()



    def selectPlantFromList(self, event):
        self.selectedIndex = event.widget.curselection()
        plantsDto: PlantsDTO = self.plantList[self.selectedIndex[0]]
        self.tkPlants.fillFromDto(plantsDto)
        self.changeImage()

        self.lbPlantsInfo.config(state=tk.NORMAL)
        self.lbPlantsInfo.delete("1.0", tk.END)
        self.lbPlantsInfo.insert(tk.END, self.tkPlants.char.get())

        btnAddNewPot = ttk.Button(self.plants, text="Update", command=self.updatePlant)
        btnAddNewPot.grid(row=5, column=2, pady=5, padx=5, sticky=tk.W)

        btnAddNewPot = ttk.Button(self.plants, text="Delete", command=self.deletePlant)
        btnAddNewPot.grid(row=5, column=2, pady=5, padx=5, sticky=tk.E)

    def deletePlant(self):

        potvrda = messagebox.askyesno("Potvrda", "Potvrdite brisanje")
        if potvrda:
            self.service.deletePlant(self.tkPlants.id)
            self.fetchAndSetPlantList()
            self.lbPlantsInfo.config(state=tk.NORMAL)
            self.lbPlantsInfo.delete(1.0, tk.END)
            self.tkPlants.clear()

    def updatePlant(self):

        self.top2 = tk.Toplevel(self)
        self.top2.geometry("400x400")
        self.top2.title("Update plant")

        self.lblPlantChar = ttk.Label(self.top2, text="Unesite karakteristike: ")
        self.lblPlantChar.grid(row=2, column=0, pady=5, padx=5, sticky=tk.NE)
        self.lblEntryPlantChar1 = StringVar()
        self.lblEntryPlantChar1 = tk.Text(self.top2)
        self.lblEntryPlantChar1.config(height=10, width=16)
        self.lblEntryPlantChar1.grid(row=2, column=2)
        newChar = self.tkPlants.char.get()
        self.lblEntryPlantChar1.insert(tk.END, newChar)
        self.lbPlantsInfo.config(state=tk.NORMAL)
        self.lbPlantsInfo.config(state=tk.DISABLED)

        btnSave = ttk.Button(self.top2, text="Save", command=self.update)
        btnSave.grid(row=3, column=0, columnspan=3, rowspan=2, padx=5, pady=5, sticky=tk.EW)

    def update(self):

        b = self.lblEntryPlantChar1.get("1.0", tk.END)
        self.tkPlants.char.set(b)
        self.lbPlantsInfo.insert(tk.END, b)
        potsDto = PlantsDTO.createFromTkModel(self.tkPlants)
        print(potsDto.name)
        self.service.updatePlant(potsDto)
        self.fetchAndSetPlantList()
        self.top2.destroy()


    def fetchAndSetPlantList(self):

        self.plantList = self.service.getAllPlants()
        simplifiedPlantList = []
        for plant in self.plantList:
            p: PlantsDTO = plant
            simplifiedPlantList.append(p.getInfo())

        self.tkPlantList = StringVar(value=simplifiedPlantList)
        self.lbPlants.config(listvariable=self.tkPlantList)

    def changeImage(self):

        plantName = self.tkPlants.name.get()
        if plantName == "Origano":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgOrigano)
        elif plantName == "Ruzmarin":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgRuzmarin)
        elif plantName == "Bosiljak":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgBosiljka)
        elif plantName == "Lovor":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgLovor)
        elif plantName == "Kopar":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgKopar)
        elif plantName == "Paprika":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgPaprika)
        elif plantName == "Rajcica":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgPoma)
        elif plantName == "Tikvica":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgTikvica)
        elif plantName == "Feferon":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgFeferon)
        elif plantName == "Maslina":
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkImgMaslina)
        else:
            self.lblPhotosPlant.config(image=self.welcomeWindow.tkNoImg)





