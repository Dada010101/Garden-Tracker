

class UsersDTO:

    def __init__(self):
        self.id = None
        self.name = None
        self.surname = None
        self.username = None
        self.password = None

    def __repr__(self):
        return str(self.__dict__)

    def getInfo(self):
        return f"{self.name}"

    @staticmethod
    def createFromResult(result: tuple):
        userDto = UsersDTO()
        userDto.id = result[0]
        userDto.name = result[1]
        userDto.surname = result[2]
        userDto.username = result[3]
        userDto.password = result[4]
        return userDto

    @staticmethod
    def createFromTkModel(tkModel):
        userDto = UsersDTO()
        userDto.id = tkModel.id
        userDto.name = tkModel.name.get()
        userDto.surname = tkModel.surname.get()
        userDto.username = tkModel.username.get()
        userDto.password = tkModel.password.get()
        return userDto
