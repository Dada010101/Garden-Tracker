from tkinter import ttk, IntVar, StringVar
import tkinter as tk
from PIL import Image, ImageTk
from datasources.dto.Users import UsersDTO
from components.PlantsComponent import PlantsComponent
from services.PlantsService import PlantsService
from components.PotsComponent import PotsComponent
from services.UserService import UserService
from services.PotsService import PotsService
from datasources.tk.TkUsers import TkUsers


class WelcomeScreen(ttk.LabelFrame):

    def __init__(self, parent, row, column, service: UserService, potsService: PotsService, plaS: PlantsService):
        super().__init__(master=parent, text="Welcome to PyFlora")
        self.grid(row=row, column=column, padx=5, pady=5)
        self.loginWindow = parent
        self.service = service
        self.potsService = potsService
        self.plaS = plaS
        self.plantsComponent = PlantsComponent
        self.potsComponents = PotsComponent
        self.user = UsersDTO()
        self.tkUser = TkUsers()
        self._loadImages()
        self.setView()



    def setView(self):

        self.b = ttk.Frame(self)
        self.b.grid(row=0, column=0)

        btnMyProfile = tk.Button(self.b, text="My profile", background="green",anchor=tk.E, command=self.profileD, font=("Arial", 10))
        btnMyProfile.grid(row=0, column=9, sticky=tk.E)

        menub = tk.Menubutton(self.b, text='Menu',  background="green", font=("Arial", 12))
        menub.grid(row=0, column=1, sticky=tk.E)
        menub.menu = tk.Menu(menub, tearoff=0)
        menub["menu"] = menub.menu

        pots = IntVar()
        plants = IntVar()
        menub.menu.add_command(label='Plants',  command=self.openPlantComponents)
        menub.menu.add_command(label='Pots', command=self.openPotsComponents)#, c=plants)
        if self.loginWindow.username.get() == "profa":
            menub.menu.add_command(label="Korisnici", command=self.adminPanel)
        menub.menu.add_command(label="Log out", command=self.master.quit)

        self.canvas = tk.Canvas(self.b, width=1150, height=620)
        self.canvas.grid(row=2, column=8)
        self.canvas.bind("<Configure>", self.resize_image2)

    def adminPanel(self):

        self.adminTop = tk.Toplevel(self)
        self.adminTop.geometry("600x600")

        self.adminTop.title("Admin Panel")

        self.infoUsers = tk.Listbox(self.adminTop)
        self.infoUsers.grid(row=0, column=0, padx=5, pady=5, rowspan=5)
        self.infoUsers.bind("<Double-1>", self.selectUserFromList)

        self.fetchAndSetUserList()

        nameUser = ttk.Label(self.adminTop, text="Name: ")
        nameUser.grid(row=0, column=1, padx=5, pady=5)
        eNameUser = ttk.Label(self.adminTop, textvariable=self.tkUser.name)
        eNameUser.grid(row=0, column=2, pady=5, padx=5)

        surnameUser = ttk.Label(self.adminTop, text="Surname: ")
        surnameUser.grid(row=1, column=1, padx=5, pady=5)
        esurnameUser = ttk.Label(self.adminTop, textvariable=self.tkUser.surname)
        esurnameUser.grid(row=1, column=2, pady=5, padx=5)

        usernameUser = ttk.Label(self.adminTop, text="Username: ")
        usernameUser.grid(row=2, column=1, padx=5, pady=5)
        eusernameUser = ttk.Label(self.adminTop,  textvariable=self.tkUser.username)
        eusernameUser.grid(row=2, column=2, pady=5, padx=5)

        btnDelete = ttk.Button(self.adminTop, text=" Delete ", command=self.deleteUser)
        btnDelete.grid(row=6, column=2, pady=5, padx=5, columnspan=3, rowspan=3)

    def deleteUser(self):

        self.service.deleteUser(self.tkUser.id)
        self.fetchAndSetUserList()

    def resize_image2(self, e):
        global image3, resized, image4
        image3 = Image.open("./images/ova.jpg")
        resized = image3.resize((e.width, e.height), Image.Resampling.LANCZOS)
        image4 = ImageTk.PhotoImage(resized)
        self.canvas.create_image(0, 0, image=image4, anchor='nw')
        self.canvas.create_text(300, 250, text="Za informacije o biljkama \ni posudama birajte Menu \nili za informacije o profilu\nbirajte MyProfile", font=("Vivaldi", 38, "bold"), fill="khaki2")

    def openPlantComponents(self):

        self.canvas.grid_remove()
        self.plantsComponent = PlantsComponent(self, 1, 0, self.plaS)

    def openPotsComponents(self):

        self.canvas.grid_remove()
        if self.plantsComponent is not None:
            self.plantsComponent.destroy()
            self.plantsComponent = None
        self.potsComponents = PotsComponent(self, 1, 0, self.potsService)

    def clear(self):
        for widget in self.plantsComponent.winfo_children():
            widget.destroy()

    def clear1(self):
        for widget in self.potsComponents.winfo_children():
            widget.destroy()

    def profileD(self):

        self.loginWindow.profileDetails()

    def selectUserFromList(self, event):
        self.selectedIndex = event.widget.curselection()
        userDto: UsersDTO = self.userList[self.selectedIndex[0]]
        self.tkUser.fillFromDto(userDto)

    def fetchAndSetUserList(self):
        self.userList = self.service.getAllUsers()
        simplifiedUserList = []
        for user in self.userList:
            u: UsersDTO = user
            simplifiedUserList.append(u.getInfo())

        self.tkUserList = StringVar(value=simplifiedUserList)
        self.infoUsers.config(listvariable=self.tkUserList)

    def _loadImages(self):

        imgNophoto = Image.open("./images/No_image_available.svg.png")
        imgBosiljak = Image.open("./images/imagesBiljke/bosiljak.jpg")
        imgFeferon = Image.open("./images/imagesBiljke/feferon.jpg")
        imgKopar = Image.open("./images/imagesBiljke/Kopar.jpg")
        imgLovor = Image.open("./images/imagesBiljke/lovor.jpg")
        imgMaslina = Image.open("./images/imagesBiljke/maslina.jpg")
        imgTikvica = Image.open("./images/imagesBiljke/tikvica.jpg")
        imgOrigano = Image.open("./images/imagesBiljke/origano.jpg")
        imgPaprika = Image.open("./images/imagesBiljke/paprika.jpg")
        imgPoma = Image.open("./images/imagesBiljke/poma.jpg")
        imgRuzmarin = Image.open("./images/imagesBiljke/ruzmarin.jpg")

        self.tkNoImg = ImageTk.PhotoImage(imgNophoto)
        self.tkImgBosiljka = ImageTk.PhotoImage(imgBosiljak)
        self.tkImgFeferon = ImageTk.PhotoImage(imgFeferon)
        self.tkImgKopar = ImageTk.PhotoImage(imgKopar)
        self.tkImgLovor = ImageTk.PhotoImage(imgLovor)
        self.tkImgMaslina = ImageTk.PhotoImage(imgMaslina)
        self.tkImgTikvica = ImageTk.PhotoImage(imgTikvica)
        self.tkImgOrigano = ImageTk.PhotoImage(imgOrigano)
        self.tkImgPaprika = ImageTk.PhotoImage(imgPaprika)
        self.tkImgPoma = ImageTk.PhotoImage(imgPoma)
        self.tkImgRuzmarin = ImageTk.PhotoImage(imgRuzmarin)












