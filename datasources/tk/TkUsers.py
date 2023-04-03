from tkinter import StringVar

class TkUsers:

    def __init__(self):
        self.id = None
        self.name = StringVar()
        self.surname = StringVar()
        self.username= StringVar()
        self.password = StringVar()

    def fillFromDto(self, userDto):
        self.id = userDto.id
        self.name.set(userDto.name)
        self.surname.set(userDto.surname)
        self.username.set(userDto.username)
        self.password.set(userDto.password)

