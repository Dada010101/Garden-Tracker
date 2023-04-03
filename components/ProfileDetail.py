import tkinter as tk
from tkinter import ttk, LabelFrame, StringVar
from PIL import ImageTk, Image
from datasources.dto.Users import UsersDTO
from datasources.tk.TkUsers import TkUsers
from services.UserService import UserService


class ProfileDetail(ttk.LabelFrame):

    def __init__(self, parent, s: UserService):
        super().__init__(master=parent, text="Profile details")
        self.grid(pady=5, padx=5)
        self.loginWindow = parent
        self.service = s
        self.tkUser = TkUsers()
        self.usersDto = UsersDTO()
        self._loadImages()
        self.createProfilePanel()

    def createProfilePanel(self):

        self.top = tk.Toplevel(self.master)
        self.top.geometry("900x400")
        self.top.title("My profile")

        self.lblprofilePicture = ttk.Label(self.top, text="Profile picture", font=("Vivaldi", 22), foreground="green")
        self.lblprofilePicture.grid(row=1, column=0, padx=5, pady=5)
        self.labelPhoto = tk.Label(self.top, image=None)
        self.labelPhoto.grid(row=1, column=0, pady=5, padx=5, rowspan=5, columnspan=2)
        self.profilePhoto()

        self.lblName = ttk.Label(self.top, text="Name:", font=("Vivaldi", 22), foreground="green")
        self.lblName.grid(row=1, column=3, padx=5, pady=5)
        self.name = ttk.Label(self.top, textvariable=self.loginWindow.tkUser.name, font=("Vivaldi", 22, "bold"), foreground="khaki2")
        self.name.grid(row=1, column=4, padx=5, pady=5)

        self.lblSurname = ttk.Label(self.top, text="Surname:", font=("Vivaldi", 22), foreground="green")
        self.lblSurname.grid(row=2, column=3, padx=5, pady=5)
        self.surname = ttk.Label(self.top, textvariable=self.loginWindow.tkUser.surname, font=("Vivaldi", 22, "bold"), foreground="khaki2")
        self.surname.grid(row=2, column=4, padx=5, pady=5)

        self.lblUsername = ttk.Label(self.top, text="Username:", font=("Vivaldi", 22), foreground="green")
        self.lblUsername.grid(row=3, column=3, padx=5, pady=5)
        self.username = ttk.Label(self.top, textvariable=self.loginWindow.tkUser.username, font=("Vivaldi", 22, "bold"),
                                  foreground="khaki2")
        self.username.grid(row=3, column=4, padx=5, pady=5)

        self.lblPassword = ttk.Label(self.top, text="Password:", font=("Vivaldi", 22), foreground="green")
        self.lblPassword.grid(row=4, column=3, padx=5, pady=5)
        self.password = ttk.Entry(self.top, textvariable=self.loginWindow.tkUser.password, font=("Vivaldi", 22, "bold"),
                                  foreground="khaki2")
        self.password.grid(row=4, column=4, padx=5, pady=5)

        btnChangePass = ttk.Button(self.top, text="Edit password", command=self.editPassWindow)
        btnChangePass.grid(row=4, column=5, padx=5, pady=5)

        btnBack = ttk.Button(self.top, text="   Close   ",  command=self.top.destroy)
        btnBack.grid(row=5, column=5,padx=5, pady=5, sticky=tk.SW)

    def editPassWindow(self):

        self.top1 = tk.Toplevel(self.master)
        self.top1.geometry("320x150")
        self.top1.title("Change password")

        newPass = ttk.Label(self.top1, text="New password: ", font=("Vivaldi", 14, "bold"), foreground="green")
        newPass.grid(row=0, column=0, padx=5, pady=5)

        self.a = ttk.Entry(self.top1, font=('Vivaldi', 14))
        self.a.grid(row=0, column=1, padx=5, pady=5)

        btnSavePass = ttk.Button(self.top1, text="Save and exit", command=self.editPass)
        btnSavePass.grid(row=1, column=0, padx=5, pady=5)
        BtnCancel = ttk.Button(self.top1, text="Cancel", command=self.top1.destroy)
        BtnCancel.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)

    def editPass(self):

        new = self.a.get()
        b = self.loginWindow.tkUser.password.set(new)
        userDto = UsersDTO.createFromTkModel(self.loginWindow.tkUser)
        self.service.updateUser(userDto)
        self.fetchAndSetUserList()
        self.top1.destroy()

    def fetchAndSetUserList(self):

        self.userList = self.service.getAllUsers()
        simplifiedUserList = []
        for user in self.userList:
            u: UsersDTO = user
            simplifiedUserList.append(u.getInfo())

        self.tkUserList = StringVar(value=simplifiedUserList)

    def profilePhoto(self):
        name = self.loginWindow.tkUser.name.get()
        if name == "Andreas":
            self.labelPhoto.config(image=self.tkImgAndreas)
        elif name == "Daniela":
            self.labelPhoto.config(image=self.tkImgDaniela)
        elif name == "Ana":
            self.labelPhoto.config(image=self.tkImgAni)
        else:
            self.labelPhoto.config(image=self.tkNoImg)

    def _loadImages(self):
        imgAndreas = Image.open("./images/profileImg/andreas.jpg")
        imgDaniela = Image.open("./images/profileImg/Daniela.jpg")
        imgAni = Image.open("./images/profileImg/Ani2.jpg")
        imgNophoto = Image.open("./images/No_image_available.svg.png")

        self.tkImgAndreas = ImageTk.PhotoImage(imgAndreas)
        self.tkImgDaniela = ImageTk.PhotoImage(imgDaniela)
        self.tkImgAni = ImageTk.PhotoImage(imgAni)
        self.tkNoImg = ImageTk.PhotoImage(imgNophoto)





