

class PlantsDTO:

    def __init__(self):
        self.id = None
        self.name = None
        self.char = None

    def __repr__(self):
        return str(self.__dict__)

    def getInfo(self):
        return f"{self.name}"

    def getInfo2(self):
        return f"{self.name}, {self.char}"

    @staticmethod
    def createFromResult(result: tuple):
        plantsDto = PlantsDTO()
        plantsDto.id = result[0]
        plantsDto.name = result[1]
        plantsDto.char = result[2]
        return plantsDto

    @staticmethod
    def createFromTkModel(tkModel):
        plantsDto = PlantsDTO()
        plantsDto.id = tkModel.id
        plantsDto.name = tkModel.name.get()
        plantsDto.char = tkModel.char.get()
        return plantsDto
