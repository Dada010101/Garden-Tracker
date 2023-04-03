import tkinter as tk
from tkinter import ttk, Frame, messagebox
import sv_ttk
from PIL import Image, ImageTk
from services.UserService import UserService
from services.PlantsService import PlantsService
from services.PotsService import PotsService, Pots
from components.PlantsComponent import PlantsComponent, PlantsDTO
from datasources.tk.TkUsers import TkUsers
from datasources.dto.Users import UsersDTO
from screens.WelcomeScreen import WelcomeScreen
from components.ProfileDetail import ProfileDetail



class LoginWindow(Frame):

    def __init__(self, mainWindow, service: UserService, plantS: PlantsService, potS: PotsService):
        super().__init__(master=mainWindow)
        self.grid()
        sv_ttk.use_dark_theme()
        self.service = service
        self.plantS = plantS
        self.potS = potS
        self.user = UsersDTO()
        self.toggleVisibility = False
        self.tkUser = TkUsers()
        self.LoginScreen()
        #self.pyFloraScreen()

    def LoginScreen(self):

        self.canvas = tk.Canvas(self, width=1300, height=620)
        #self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.grid(row=1, column=1)
        self.canvas.bind("<Configure>", self.resize_image)

        self.username = tk.StringVar()
        self.username = tk.Entry(self.canvas, font=("Vivaldi", 33), width=14, bd=0, fg="white", background="forestgreen")
        self.username.grid(row=3, column=1)
        self.windowUsername = self.canvas.create_window(88, 290, anchor="nw", window=self.username)

        self.password = tk.StringVar()
        self.password = tk.Entry(self.canvas, font=("Vivaldi", 33), width=14, bd=0, fg="forestgreen", show="*")
        self.password.grid(row=5, column=1)
        self.windowPassword = self.canvas.create_window( 88, 400, anchor="nw", window=self.password)

        login_btn = tk.Button(self.canvas, text="Login", font=("Vivaldi", 18), width=15, fg="white", bg="forestgreen", command=self.login)
        login_btn_window = self.canvas.create_window(88, 480, anchor="nw", window=login_btn)

        registration_btn = tk.Button(self.canvas, text="Register", font=("Vivaldi", 16), width=17,  fg="white", bg="forestgreen",
                           command=self.registerScreen)
        registration_btn_window = self.canvas.create_window(88, 560, anchor="nw", window=registration_btn)

        imgShow = Image.open("./images/show.png")
        imgHide = Image.open("./images/hide.png")
        self.tkImgShow = ImageTk.PhotoImage(imgShow)
        self.tkImgHide = ImageTk.PhotoImage(imgHide)

        self.btnShowPhoto = tk.Button(self.canvas, image=self.tkImgHide, background="forestgreen", command=self.changeVisibility)
        self.windowShowPhoto = self.canvas.create_window(340, 417, window=self.btnShowPhoto)

    def changeVisibility(self):
        if not self.toggleVisibility:
            self.password.config(show="")
            self.btnShowPhoto.config(image=self.tkImgShow)
            self.toggleVisibility = True
        else:
            self.password.config(show="*")
            self.btnShowPhoto.config(image=self.tkImgHide)
            self.toggleVisibility = False


    def resize_image(self, e):
        global image, resized, image2
        image = Image.open("./images/proba1.jpg")
        resized = image.resize((e.width, e.height), Image.Resampling.LANCZOS)
        image2 = ImageTk.PhotoImage(resized)

        self.canvas.create_image(0, 0, image=image2, anchor='nw')
        self.canvas.create_text(300, 150, text="PyFlora", font=("Vivaldi", 100, "bold"), fill="forestgreen", anchor="center", activefill="greenyellow")
        self.canvas.create_text(130, 270, text="Username:", font=("Vivaldi", 22, "bold"), fill="forestgreen")
        self.canvas.create_text(130, 380, text="Password:", font=("Vivaldi", 22, "bold"), fill="forestgreen")
        self.canvas.create_text(210, 540, text="or", font=("Vivaldi", 26, "bold"), fill="white")


    def login(self):
        username = self.username.get()
        password = self.password.get()
        userDto: UsersDTO = self.service.getUserByUsernameAndPass(username, password)
        print(userDto)
        if userDto is not None:
            self.canvas.grid_remove()
            self.tkUser.id = userDto.id
            self.tkUser.name.set(userDto.name)
            self.tkUser.surname.set(userDto.surname)
            self.tkUser.username.set(userDto.username)
            self.tkUser.password.set(userDto.password)
            self.pyFloraScreen()

        else:
            self.canvas.create_text(385, 466, text="Username or password are not match! Please try again!", font=("Vivaldi", 24, "bold"), fill="white")

    def registerScreen(self):

        self.registrationScreen = tk.Toplevel(self)
        self.registrationScreen.geometry("400x400")
        self.registrationScreen.title("Registration")
        #self.registrationScreen.grid(row=0, column=0, pady=5, padx=5)

        self.lblname = ttk.Label(self.registrationScreen, text="Name: ")
        self.lblname.grid(row=0, column=0, padx=10, pady=10)
        self.eName = ttk.Entry(self.registrationScreen, textvariable=self.tkUser.name)
        self.eName.grid(row=0, column=1, padx=10, pady=10)

        self.lblSurname = ttk.Label(self.registrationScreen, text="Surname: ")
        self.lblSurname.grid(row=1, column=0, padx=10, pady=10)
        self.eSurname = ttk.Entry(self.registrationScreen, textvariable=self.tkUser.surname)
        self.eSurname.grid(row=1, column=1, padx=10, pady=10)

        self.lblUsername = ttk.Label(self.registrationScreen, text="Username: ")
        self.lblUsername.grid(row=3, column=0, padx=10, pady=10)
        self.eUsername = ttk.Entry(self.registrationScreen, textvariable=self.tkUser.username)
        self.eUsername.grid(row=3, column=1, padx=10, pady=10)

        self.lblPassword = ttk.Label(self.registrationScreen, text="Password: ")
        self.lblPassword.grid(row=4, column=0, padx=10, pady=10)
        self.ePassword = ttk.Entry(self.registrationScreen, show="*", textvariable=self.tkUser.password)
        self.ePassword.grid(row=4, column=1, padx=10, pady=10)

        self.btnSubmit = ttk.Button(self.registrationScreen, text="Register", command=self.register)
        self.btnSubmit.grid(row=6, column=1, padx=10, pady=10)

        self.btnBack = ttk.Button(self.registrationScreen, text="Back", command=self.registrationScreen.destroy)
        self.btnBack.grid(row=6, column=0, padx=10, pady=10)

    def register(self):

        self.eName = self.tkUser.name.get()
        self.eSurname = self.tkUser.surname.get()
        self.eUsername = self.tkUser.username.get()
        if self.eUsername == self.service.checkUsername(self.eUsername):
            messagebox.showinfo("Korisnicko ime vec postoji", "Molim izaberite drugacije ime")
            self.ePassword = self.tkUser.password.get()
        elif self.eUsername != self.service.checkUsername(self.eUsername):

            self.service.addUser(self.eName, self.eSurname, self.eUsername, self.ePassword)
            self.registrationScreen.destroy()
            messagebox.showinfo("Registracija", "Uspjesno ste se registrirali!")

    def pyFloraScreen(self):

        self.welcomeScreen = WelcomeScreen(self, 0, 0, self.service, self.potS, self.plantS)

    def profileDetails(self):
        ProfileDetail(self, self.service)



