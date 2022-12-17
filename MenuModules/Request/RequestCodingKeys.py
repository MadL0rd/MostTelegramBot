import enum

titles = {
    "bikeHelmet": "Сколько шлемов нужно",
    "comment": "Комментарий",
    "requestGeoposition": "Геопозиция",
    "bikeCommitment": "Тип",
    "carCommitment": "Тип",
    "bikeCriteriaChoice": "Критерий байка",
    "bikeMotoCategory": "Категорий мотоцикла",
    "bikeMotoCategoryChoice": "Категорий мотоцикла",
    "bikeScooterCategory": "Модель скутера",
    "bikeScooterCategoryChoice": "Модель скутера",
    "bikeScooterOrMoto": "Вид байка",
    "carModels": "Модель авто",
    "carSize": "Размер авто",
    "carTransmission": "Трансмиссия",
    "timeRequest": "Вид аренды",
    "timeRequestDayWeekWhen": "Когда нужен транспорт",
    "timeRequestDayWeekWhenSetDate": "Когда нужен транспорт",
    "timeRequestHowManyDays": "На сколько дней нужен транспорт",
    "timeRequestHowManyMonths": "На сколько месяцев нужен транспорт",
    "timeRequestHowManyMonthsSet": "На сколько месяцев нужен транспорт",
    "timeRequestMonthWhen": "Когда начнётся помесячная аренда",
    "timeRequestMonthWhenSetDate": "Когда начнётся помесячная аренда"
}

class RequestCodingKeys(enum.Enum):
    bikeHelmet : str = "bikeHelmet"
    comment : str = "comment"
    requestGeoposition : str = "requestGeoposition"
    bikeCommitment : str = "bikeCommitment"
    carCommitment : str = "carCommitment"
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
    def getKey(self) -> str:
        return self.value

    @property
    def getTitle(self) -> str:
        return titles[self.getKey]