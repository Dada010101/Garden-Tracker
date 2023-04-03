

class Pots:

    def __init__(self):
        self.id = None
        self.name = None
        self.plantName = None
        self.temperature = 3
        self.humidity = 990


    def __repr__(self):
        return str(self.__dict__)

    def getInfo(self):
        return f"{self.name}"


    @staticmethod
    def createFromResult(result: tuple):
        potsDto = Pots()
        potsDto.id = result[0]
        potsDto.name = result[1]
        potsDto.plantName = result[2]
        potsDto.temperature = result[3]
        potsDto.humidity = result[4]
        return potsDto

    @staticmethod
    def createFromTkModel(tkModel):
        potsDto = Pots()
        if potsDto.temperature is None and potsDto.humidity is None:
            potsDto.id = tkModel.id
            potsDto.name = tkModel.name.get()
            potsDto.plantName = tkModel.plantName.get()

        else:
            potsDto.id = tkModel.id
            potsDto.name = tkModel.name.get()
            potsDto.plantName = tkModel.plantName.get()
            potsDto.temperature = tkModel.temperature.get()
            potsDto.humidity = tkModel.humidity.get()


        return potsDto


