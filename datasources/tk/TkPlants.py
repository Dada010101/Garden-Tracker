from tkinter import StringVar


class TkPlants:

    def __init__(self):
        self.id = None
        self.name = StringVar()
        self.char = StringVar()

    def fillFromDto(self, plantsDto):
        self.id = plantsDto.id
        self.name.set(plantsDto.name)
        self.char.set(plantsDto.char)

    def clear(self):
        self.id = None
        self.name.set("")
        self.char.set("")

