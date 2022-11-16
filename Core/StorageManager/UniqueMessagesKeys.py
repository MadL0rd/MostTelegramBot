
import enum
import Core.StorageManager.StorageManager as storage 

class UniqueMessagesKeys(enum.Enum):

    unknownState = "unknownState"

    menuButtonReturnToMainMenu = "menuButtonReturnToMainMenu"

    mainMenuText = "mainMenuText"
    menuButtonRentBike = "menuButtonRentBike"
    menuButtonRentCar = "menuButtonRentCar"
    menuButtonMyOrders = "menuButtonMyOrders"
    menuButtonAdmin = "menuButtonAdmin"

    adminMenuText = "adminMenuText"
    adminMenuButtonLoadData = "adminMenuButtonLoadData"
    adminMenuButtonReloadData = "adminMenuButtonReloadData"
    adminMenuButtonEveningReflectionStart = "adminMenuButtonEveningReflectionStart"

    bikeCommitment = "bikeCommitment"
    bikeButtonCommitmentYes = "bikeButtonCommitmentYes"
    bikeButtonCommitmentNo = "bikeButtonCommitmentNo"
    bikeModelsDescription  = "bikeModelsDescription"
    bikeScooterOrMoto = "bikeScooterOrMoto"
    bikeButtonScooterOrMotoMoto = "bikeButtonScooterOrMotoMoto"
    bikeButtonScooterOrMotoScooter = "bikeButtonScooterOrMotoScooter"

    bikeMotoCategory = "bikeMotoCategory"
    bikeScooterCategory = "bikeScooterCategory"

    bikeParameters = "bikeParameters"
    bikeButtonCriteria = "bikeButtonCriteria"
    bikeCriteriaChoice = "bikeCriteriaChoice"
    bikeButtonShowAll = "bikeButtonShowAll"

    timeRequest  = "timeRequest"
    timeButtonRequestDay = "timeButtonRequestDay"
    timeButtonRequestWeek = "timeButtonRequestWeek"
    timeButtonRequestMonth = "timeButtonRequestMonth"





    @property
    def get(self) -> str:
        messagesKeys = storage.getJsonData(storage.path.botContentUniqueMessages)
        if self.value in messagesKeys:
            return messagesKeys[self.value]
        else:
            return "Unknown"

textConstant = UniqueMessagesKeys
