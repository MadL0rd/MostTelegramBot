import enum

titles = {
    "bikeHelmet": "bikeHelmet"
    "comment": "comment"
    "requestGeoposition": "requestGeoposition"
    "bikeCommitment": "bikeCommitment"
    "bikeCriteriaChoice": "bikeCriteriaChoice"
    "bikeMotoCategory": "bikeMotoCategory"
    "bikeMotoCategoryChoice": "bikeMotoCategoryChoice"
    "bikeScooterCategory": "bikeScooterCategory"
    "bikeScooterCategoryChoice": "bikeScooterCategoryChoice"
    "bikeScooterOrMoto": "bikeScooterOrMoto"
    "carModels": "carModels"
    "carSize": "carSize"
    "carTransmission": "carTransmission"
    "timeRequest": "timeRequest"
    "timeRequestDayWeekWhen": "timeRequestDayWeekWhen"
    "timeRequestDayWeekWhenSetDate": "timeRequestDayWeekWhenSetDate"
    "timeRequestHowManyDays": "timeRequestHowManyDays"
    "timeRequestHowManyMonths": "timeRequestHowManyMonths"
    "timeRequestHowManyMonthsSet": "timeRequestHowManyMonthsSet"
    "timeRequestMonthWhen": "timeRequestMonthWhen"
    "timeRequestMonthWhenSetDate": "timeRequestMonthWhenSetDate"
}

class RequestCodingKeys(enum.Enum):
    bikeHelmet : str = "bikeHelmet"
    comment : str = "comment"
    requestGeoposition : str = "requestGeoposition"
    bikeCommitment : str = "bikeCommitment"
    bikeCriteriaChoice : str = "bikeCriteriaChoice"
    bikeMotoCategory : str = "bikeMotoCategory"
    bikeMotoCategoryChoice : str = "bikeMotoCategoryChoice"
    bikeScooterCategory : str = "bikeScooterCategory"
    bikeScooterCategoryChoice : str = "bikeScooterCategoryChoice"
    bikeScooterOrMoto : str = "bikeScooterOrMoto"
    carModels : str = "carModels"
    carSize : str = "carSize"
    carTransmission : str = "carTransmission"
    timeRequest : str = "timeRequest"
    timeRequestDayWeekWhen : str = "timeRequestDayWeekWhen"
    timeRequestDayWeekWhenSetDate : str = "timeRequestDayWeekWhenSetDate"
    timeRequestHowManyDays : str = "timeRequestHowManyDays"
    timeRequestHowManyMonths : str = "timeRequestHowManyMonths"
    timeRequestHowManyMonthsSet : str = "timeRequestHowManyMonthsSet"
    timeRequestMonthWhen : str = "timeRequestMonthWhen"
    timeRequestMonthWhenSetDate : str = "timeRequestMonthWhenSetDate"

    @property
    def get(self) -> str:
        return self.value

    @property
    def getTitle(self) -> str:
        return titles[self.get]