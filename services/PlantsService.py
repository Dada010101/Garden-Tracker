from utils.DBUtils import DBUtils
from datasources.dto.Plants import PlantsDTO


class PlantsService:

    TABLE_NAME = "Plants"

    def __init__(self, sqlConnection):
        self.connection = sqlConnection
        self.createTable()
        self._createPlants()

    def createTable(self):
        query = f""" CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(30) NOT NULL UNIQUE,
                char VARCHAR(500)
                 ); """
        DBUtils.izvrsiIZapisi(self.connection, query)

    def addPlant(self, name, char):
        query = f""" 
            INSERT INTO {self.TABLE_NAME} (name, char)
            VALUES ('{name}', '{char}');
        """
        DBUtils.izvrsiIZapisi(self.connection, query)

    def _createPlants(self):
        self.addPlant("Origano", "Preporučuje se odabrati tlo koje je suho, umjereno plodno i rastresito. Voli mediteransku klimu i puno svjetla")
        self.addPlant("Bosiljak", "Bosiljak najbolje uspijeva na područjima gdje je vlažno i vrlo toplo, tj. gdje prevladava umjereno topla klima.")
        self.addPlant("Lovor", "Traži toplu i vlažnu klimu, kod nas raste jedino u priobalnom području do 400 m nadmorske visine.")
        self.addPlant("Ruzmarin", "Ružmarin je biljka toplog podneblja i voli sunce. Međutim, unatoč toga, uspješno podnosi i niske temperature te mraz.")
        self.addPlant("Kopar", "Kopar je biljka umjerene klime i odgovaraju mu topla ljeta. Nije otporan na mraz, ali kao jednogodišnja biljka se ubere do zime.")
        self.addPlant("Paprika", "Za normalno klijanje paprike potrebna je temperatura zraka od oko 15°C dok je optimalna ona između 20 – 30°C")
        self.addPlant("Rajcica", "Rajčice traže obilje svjetlosti i topline, treba im osigurati najtoplije mjesto u vrtu.")
        self.addPlant("Tikvica", "Tikvica je biljka koja voli toplinu i sunčevu svjetlost.")
        self.addPlant("Feferon","Fefereon treba toplu klimu sa sunčanim mjestima; optimalna temperatura rasta je između 20 ° C i 25 ° C, uz minimalno 15 ° C")
        self.addPlant("Maslina", "Pogodna klima je vruće i suho ljeto, blaga i vlažna zima.")

    def getPlantByName(self, name):
        query = f"SELECT * FROM {self.TABLE_NAME} where name='{name}';"
        result = DBUtils.dohvatiPodatke(self.connection, query, one=True)
        if result is not None:
            plantDto: PlantsDTO = PlantsDTO.createFromResult(result)
            print(plantDto)
            return plantDto
        else:
            return None

    def nameinfo(self):
        query = f"SELECT name FROM {self.TABLE_NAME};"
        result = DBUtils.dohvatiPodatke(self.connection, query)
        a = PlantsDTO.createFromResult(result)
        return a

    def getAllPlants(self):
        query = f"SELECT * FROM {self.TABLE_NAME};"
        result = DBUtils.dohvatiPodatke(self.connection, query)
        plantList = []
        if result is not None:
            for plant in result:
                plantDto = PlantsDTO.createFromResult(plant)
                print(plantDto)
                plantList.append(plantDto)
            return plantList
        else:
            return None

    def updatePlant(self, dto: PlantsDTO):
        query = f"""
               UPDATE {self.TABLE_NAME}
               SET name='{dto.name}', char='{dto.char}'
               WHERE id={dto.id};
           """
        DBUtils.izvrsiIZapisi(self.connection, query)

    def deletePlant(self, id):
        query = f"DELETE FROM {self.TABLE_NAME} where id={id};"
        DBUtils.izvrsiIZapisi(self.connection, query)

