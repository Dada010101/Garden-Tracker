import tkinter as tk
from tkinter import ttk, Tk
from tkinter import *
import sqlite3
from services.UserService import UserService
from services.PlantsService import PlantsService
from services.PotsService import PotsService
from screens.LoginWindow import LoginWindow
from components.proba import Proba


class App(Tk):

    def __init__(self, service: UserService, plantS: PlantsService, potS: PotsService):
        super().__init__()
        self.title("PyFlora posude")
        self.geometry("1300x620")
        self.service = service
        self.plantS = plantS
        self.potS = potS
        Proba()
        self.createLoginWindow()

    def createLoginWindow(self):
        LoginWindow(self, self.service, self.plantS, self.potS)

def initDB():
    DB = "PyFlora.db"
    conn = sqlite3.connect(DB)
    return conn

if __name__ == '__main__':
    connection = initDB()
    service = UserService(connection)
    plantS = PlantsService(connection)
    potS = PotsService(connection)
    app = App(service, plantS, potS)
    app.mainloop()













