
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
    bikeScooterCategoryChoice = "bikeScooterCategoryChoice"
    bikeMotoCategoryChoice = "bikeMotoCategoryChoice"

    bikeParameters = "bikeParameters"
    bikeButtonCriteria = "bikeButtonCriteria"
    bikeCriteriaChoice = "bikeCriteriaChoice"
    bikeButtonShowAll = "bikeButtonShowAll"

    timeRequest  = "timeRequest"
    timeButtonRequestDay = "timeButtonRequestDay"
    timeButtonRequestWeek = "timeButtonRequestWeek"
    timeButtonRequestMonth = "timeButtonRequestMonth"

    timeRequestDayWeekWhen = "timeRequestDayWeekWhen"
    timeButtonRequestWhenToday = "timeButtonRequestWhenToday"
    timeButtonRequestWhenTomorrow = "timeButtonRequestWhenTomorrow"
    timeButtonRequestWhenSetDate = "timeButtonRequestWhenSetDate"
    timeRequestDayWeekWhenSetDate = "timeRequestDayWeekWhenSetDate"
    timeRequestHowManyDays = "timeRequestHowManyDays"
    timeRequestHowManyMonths = "timeRequestHowManyMonths"
    timeButtonRequestHowManyMonths1 = "timeButtonRequestHowManyMonths1"
    timeButtonRequestHowManyMonths2 = "timeButtonRequestHowManyMonths2"
    timeButtonRequestHowManyMonths3 = "timeButtonRequestHowManyMonths3"
    timeButtonRequestHowManyMonthsMore = "timeButtonRequestHowManyMonthsMore"
    timeRequestHowManyMonthsSet = "timeRequestHowManyMonthsSet"
    timeRequestMonthWhen = "timeRequestMonthWhen"
    timeButtonRequestMonthWhenToday = "timeRequestMonthWhenToday"
    timeButtonRequestMonthWhenTomorrow = "timeRequestMonthWhenTomorrow"
    timeButtonRequestMonthWhenComingDays = "timeRequestMonthWhenComingDays"
    timeRequestMonthWhenSetDate = "timeRequestMonthWhenSetDate"
    bikeHelmet = "bikeHelmet"
    bikeHelmet1 = "bikeHelmet1"
    bikeHelmet2 = "bikeHelmet2"
    bikeHelmet0 = "bikeHelmet0"
    requestGeoposition = "requestGeoposition"

    carSize = "carSize"
    carButtonSizeSmall = "carButtonSizeSmall"
    carButtonSizeBig = "carButtonSizeBig"
    carButtonSizeMinivan = "carButtonSizeMinivan"
    carButtonSizePremium = "carButtonSizePremium"
    carButtonSizeShowAll = "carButtonSizeShowAll"
    carTransmission = "carTransmission"
    carButtonTransmissionAutomatic = "carButtonTransmissionAutomatic"
    carButtonTransmissionManual = "carButtonTransmissionManual"
    carButtonTransmissionShowAll = "carButtonTransmissionShowAll"
    carModels = "carModels"
    carModelsFurther = "carModelsFurther"
    
    messageAfterFillingOutForm = "messageAfterFillingOutForm"

    commentOrderTextStart = "commentOrderTextStart"
    commentCompleteOrderButton = "commentCompleteOrderButton"
    commentUserWishesButton = "commentUserWishesButton"
    commentUserWishesText = "commentUserWishesText"

    orderNumberMask = "orderNumberMask"
    orderCreationUserText = "orderCreationUserText"
    orderDetailsMessageTitle = "orderDetailsMessageTitle"

    @property
    def get(self) -> str:
        messagesKeys = storage.getJsonData(storage.path.botContentUniqueMessages)
        if self.value in messagesKeys:
            return messagesKeys[self.value]
        else:
            return "Unknown"

    def getAndReplaceOrderMaskWith(self, text: str) -> str:
        messagesKeys = storage.getJsonData(storage.path.botContentUniqueMessages)
        if self.value in messagesKeys:
            value: str = messagesKeys[self.value]
            mask: str = textConstant.orderNumberMask.get
            return value.replace(mask, text)
        else:
            return "Unknown"

textConstant = UniqueMessagesKeys
