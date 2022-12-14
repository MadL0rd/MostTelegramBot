import enum

class MenuModuleName(enum.Enum):

    onboarding: str = "onboarding"
    mainMenu: str = "mainMenu"
    getLicense: str = "getLicense"
    findInstructor: str = "findInstructor"
    languageSettings: str = "languageSettings"
    languageSettingsFirstLaunch:str = "languageSettingsFirstLaunch"
    menuButtonAdmin: str = "menuButtonAdmin"
    myOrders: str = "myOrders"
    admin: str = "admin"
    adminNewsletter: str = "adminNewsletter"
    bikeCommitment: str = "bikeCommitment"
    bikeButtonCommitmentYes: str = "bikeButtonCommitmentYes"
    bikeButtonCommitmentNo: str = "bikeButtonCommitmentNo"
    bikeScooterOrMoto: str = "bikeScooterOrMoto"
    bikeButtonScooterOrMotoMoto: str = "bikeButtonScooterOrMotoMoto"
    bikeButtonScooterOrMotoScooter: str = "bikeButtonScooterOrMotoScooter"

    bikeMotoCategory: str = "bikeMotoCategory"
    bikeScooterCategory: str = "bikeScooterCategory"
    bikeScooterCategoryChoice: str = "bikeScooterCategoryChoice"
    bikeMotoCategoryChoice: str = "bikeMotoCategoryChoice"

    bikeParameters: str = "bikeParameters"
    bikeButtonCriteria: str = "bikeButtonCriteria"
    bikeCriteriaChoice: str = "bikeCriteriaChoice"
    bikeButtonShowAll: str = "bikeButtonShowAll"

    timeRequest: str = "timeRequest"
    timeButtonRequestDay: str = "timeButtonRequestDay"
    timeButtonRequestWeek: str = "timeButtonRequestWeek"
    timeButtonRequestMonth: str = "timeButtonRequestMonth"
    timeRequestDayWeekWhen: str = "timeRequestDayWeekWhen"
    timeRequestDayWeekWhenSetDate: str = "timeRequestDayWeekWhenSetDate"
    timeRequestHowManyDays: str = "timeRequestHowManyDays"
    timeRequestHowManyMonths: str = "timeRequestHowManyMonths"
    timeRequestHowManyMonthsSet: str = "timeRequestHowManyMonthsSet"
    timeRequestMonthWhen: str = "timeRequestMonthWhen"
    timeRequestMonthWhenSetDate: str = "timeRequestMonthWhenSetDate"

    bikeHelmet: str = "bikeHelmet"

    requestGeoposition: str = "requestGeoposition"

    carSize: str = "carSize"
    carButtonSizeSmall: str = "carButtonSizeSmall"
    carButtonSizeBig: str = "carButtonSizeBig"
    carButtonSizeMinivan: str = "carButtonSizeMinivan"
    carButtonSizePremium: str = "carButtonSizePremium"
    carButtonSizeShowAll: str = "carButtonSizeShowAll"
    carTransmission: str = "carTransmission"
    carButtonTransmissionAutomatic: str = "carButtonTransmissionAutomatic"
    carButtonTransmissionManual: str = "carButtonTransmissionManual"
    carButtonTransmissionShowAll: str = "carButtonTransmissionShowAll"
    carModels: str = "carModels"

    comment: str = "comment"

    @property
    def get(self) -> str:
        return self.value