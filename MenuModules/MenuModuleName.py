import enum

class MenuModuleName(enum.Enum):

    onboarding: str = "onboarding"
    mainMenu: str = "mainMenu"
    menuButtonAdmin: str = "menuButtonAdmin"
    rentBike: str = "rentBike"
    rentCar: str = "rentCar"
    myOrders: str = "myOrders"
    admin: str = "admin"
    bikeCommitment: str = "bikeCommitment"
    bikeButtonCommitmentYes: str = "bikeButtonCommitmentYes"
    bikeButtonCommitmentNo: str = "bikeButtonCommitmentNo"
    bikeScooterOrMoto: str = "bikeScooterOrMoto"
    bikeButtonScooterOrMotoMoto: str = "bikeButtonScooterOrMotoMoto"
    bikeButtonScooterOrMotoScooter: str = "bikeButtonScooterOrMotoScooter"

    bikeMotoCategory: str = "bikeMotoCategory"
    bikeScooterCategory: str = "bikeScooterCategory"

    bikeParameters: str = "bikeParameters"
    bikeButtonCriteria: str = "bikeButtonCriteria"
    bikeCriteriaChoice: str = "bikeCriteriaChoice"
    bikeButtonShowAll: str = "bikeButtonShowAll"

    timeRequest: str = "timeRequest"
    timeButtonRequestDay: str = "timeButtonRequestDay"
    timeButtonRequestWeek: str = "timeButtonRequestWeek"
    timeButtonRequestMonth: str = "timeButtonRequestMonth"





    @property
    def get(self) -> str:
        return self.value