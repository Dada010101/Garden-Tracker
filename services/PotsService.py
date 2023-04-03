from utils.DBUtils import DBUtils
from datasources.dto.Pots import Pots
from datetime import datetime as dt


class PotsService:

    TABLE_NAME = "Posude"

    def __init__(self, sqlConnection):
        self.connection = sqlConnection
        self.createTable()
        self._createPots()

    def createTable(self):
        query = f""" CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(30) NOT NULL UNIQUE,
                plant_name VARCHAR(60),
                temperature INTEGER,
                humidity INTEGER, 
                time TEXT NOT NULL
                
                 ); """
        DBUtils.izvrsiIZapisi(self.connection, query)

    def addPot(self, name, plantname):
        query = f""" 
            INSERT INTO {self.TABLE_NAME} (name, plant_name, time)
            VALUES ('{name}', '{plantname}','{str(dt.now().timestamp())}');
        """
        DBUtils.izvrsiIZapisi(self.connection, query)

    def _createPots(self):
        self.addPot("Zelena", "Ruzmarin")
        self.addPot("Bijela", "Lovor")
        self.addPot("Siva", None)

    def updateTime(self):

        query = f"""
                       UPDATE {self.TABLE_NAME}
                       SET time='{str(dt.now().timestamp())}'
                       WHERE id={dto.id};
                   """
        DBUtils.izvrsiIZapisi(self.connection, query)



    def getPotByName(self, name):
        query = f"SELECT * FROM {self.TABLE_NAME} where name='{name}';"
        result = DBUtils.dohvatiPodatke(self.connection, query, one=True)
        if result is not None:
            potsDto: Pots = Pots.createFromResult(result)
            print(potsDto)
            return potsDto
        else:
            return None


    def getAllPots(self):
        query = f"SELECT * FROM {self.TABLE_NAME};"
        result = DBUtils.dohvatiPodatke(self.connection, query)
        potsList = []
        if result is not None:
            for pot in result:
                potsDto = Pots.createFromResult(pot)
                print(potsDto)
                potsList.append(potsDto)
            return potsList
        else:
            return None

    def updatePot(self, dto: Pots):
        query = f"""
               UPDATE {self.TABLE_NAME}
               SET name='{dto.name}', plant_name='{dto.plantName}', temperature='{dto.temperature}', humidity='{dto.humidity}', time='{str(dt.now().timestamp())}'
               WHERE id={dto.id};
           """
        DBUtils.izvrsiIZapisi(self.connection, query)

    def deletePot(self, id):
        query = f"DELETE FROM {self.TABLE_NAME} where id={id};"
        DBUtils.izvrsiIZapisi(self.connection, query)
