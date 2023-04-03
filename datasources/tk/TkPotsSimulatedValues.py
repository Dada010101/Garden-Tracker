from tkinter import DoubleVar, StringVar


class TkPotsSimulatedValues:

    def __init__(self):
        self.id = None
        self.name = StringVar()
        self.plantName = StringVar()
        self.temperature = DoubleVar()
        self.humidity = DoubleVar()

    def fillFromDto(self, potsDto):
        self.id = potsDto.id
        self.name.set(potsDto.name)
        self.plantName.set(potsDto.plantName)
        self.temperature.set(potsDto.temperature)
        self.humidity.set(potsDto.humidity)

    def clear(self):
        self.id = None
        self.name.set("")
        self.plantName.set("")
        self.temperature.set("")
        self.humidity.set("")