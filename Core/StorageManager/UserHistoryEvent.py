import enum

class UserHistoryEvent(enum.Enum):

    start = "Старт"
    sendMessage = "Отправил сообщение"
    callbackButtonDidTapped = "Нажал на кнопку в сообщении"
    becomeAdmin = "Стал администратором"
    startModuleOnboarding = "Начал смотреть онбординг"
    startModuleMainMenu = "Перешел в главное меню" 

    startModuleGetLicense = "Перешёл в модуль покупки прав"
    startModuleFindInstructor = "Перешёл в модуль поиска инструктора"
    startModuleStartBikeOrCarChoice = "Приступил к выбору байка или машины"

    startModuleBikeCommitment = "Приступил к выбору байка"
    startModuleBikeScooterOrMoto = "Приступил к выбору скутера или мотоцикла"
    startModuleBikeMotoCategory = "Приступил к выбору категории мотоцикла"
    startModuleBikeScooterCategory = "Приступил к выбору категории скутера"
    startModuleBikeScooterCategoryChoice = "Приступил к точному указанию желаемой модели скутера"
    strartModuleBikeMotoCategoryChoice = "Приступил к точному указанию желаемой модели мотоцикла"
    startModuleBikeParameters = "Приступил к выбору параметров байка"
    startModuleBikeCriteriaChoice = "Приступил к выбору критериев"

    startModuleTimeRequest = "Приступил к выбору времени"
    startModuleTimeRequestDayWeekWhen = "Приступил к выбору даты начала аренды (длительность в днях/неделях)"
    startModuleTimeRequestDayWeekWhenSetDate = "Приступил к указанию точной даты начала аренды (длительность в днях/неделях)"
    startModuleTimeRequestHowManyDays = "Приступил к выбору длительности аренды в днях"
    startModuleTimeRequestHowManyMonths = "Приступил к выбору длительности аренды в месяцах"
    startModuleTimeRequestHowManyMonthsSet = "Приступил к указанию точного количества месяцев аренды"
    startModuletimeRequestMonthWhen = "Приступил к выбору даты начала аренды (длительность в месяцах)"
    startModuleTimeRequestMonthWhenSetDate = "Приступил к указанию точной даты начала аредны (длительность в месяцах)"

    startModuleBikeHelmet = "Приступил к выбору количества шлемов"

    startModuleRequestGeoposition = "Приступил к указанию геопозиции"
    startModuleCarSize = "Приступил к выбору размера машины"
    startModuleCarTransmission = "Приступил к выбору коробки передач"
    startModuleCarModels = "Приступил к выбору моделей"
    geopositionHasBeenSpecified = "Указал геопозицию и оказался в меню продолжить или оставить коммент"
    orderHasBeenCreated = "Заказ был создан"