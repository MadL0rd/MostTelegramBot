import enum
from Core.StorageManager.LanguageKey import LanguageKey
from MenuModules.MainMenu.FindInstuctor import FindInstructor
from MenuModules.MainMenu.GetLicense import GetLicense
from MenuModules.MainMenu.LanguageSettings import LanguageSettings
from MenuModules.Onboarding.Onboarding import Onboarding
from MenuModules.MainMenu.MainMenu import MainMenu
from MenuModules.MenuModuleInterface import MenuModuleInterface
from MenuModules.MainMenu.AdminMenu import AdminMenu
from MenuModules.Request.Bike.BikeCommitment import BikeCommitment
from MenuModules.Request.Bike.BikeMotoCategory import BikeMotoCategory
from MenuModules.Request.Bike.BikeParameters import BikeParameters
from MenuModules.Request.Bike.BikeScooterOrMoto import BikeScooterOrMoto
from MenuModules.Request.Bike.BikeScooterCategory import BikeScooterCategory
from MenuModules.Request.Bike.BikeCriteriaChoice import BikeCriteriaChoice
from MenuModules.Request.Bike.BikeMotoCategoryChoice import BikeMotoCategoryChoice
from MenuModules.Request.Bike.BikeScooterCategoryChoice import BikeScooterCategoryChoice
from MenuModules.Request.BikeHelmet import BikeHelmet
from MenuModules.Request.Car.CarModels import CarModels
from MenuModules.Request.Car.CarSize import CarSize
from MenuModules.Request.Car.CarTransmission import CarTransmission
from MenuModules.Request.Comment import Comment
from MenuModules.Request.RequestGeoposition import RequestGeoposition
from MenuModules.Request.Time.TimeRequest import TimeRequest
from MenuModules.Request.Time.TimeRequestDayWeekWhen import TimeRequestDayWeekWhen
from MenuModules.Request.Time.TimeRequestDayWeekWhenSetDate import TimeRequestDayWeekWhenSetDate
from MenuModules.Request.Time.TimeRequestHowManyDays import TimeRequestHowManyDays
from MenuModules.Request.Time.TimeRequestHowManyMonths import TimeRequestHowManyMonths
from MenuModules.Request.Time.TimeRequestHowManyMonthsSet import TimeRequestHowManyMonthsSet
from MenuModules.Request.Time.TimeRequestMonthWhen import TimeRequestMonthWhen
from MenuModules.Request.Time.TimeRequestMonthWhenSetDate import TimeRequestMonthWhenSetDate

from logger import logger as log

class MenuModules(enum.Enum):

    onboarding: MenuModuleInterface = Onboarding
    mainMenu: MenuModuleInterface = MainMenu
    getLicense: MenuModuleInterface = GetLicense
    findInstructor: MenuModuleInterface = FindInstructor
    languageSettings: MenuModuleInterface = LanguageSettings
    adminMenu: MenuModuleInterface = AdminMenu
    bikeCommitment: MenuModuleInterface = BikeCommitment
    bikeScooterOrMoto: MenuModuleInterface = BikeScooterOrMoto
    bikeMotoCategory: MenuModuleInterface = BikeMotoCategory
    bikeScooterCategory: MenuModuleInterface = BikeScooterCategory
    bikeScooterCategoryChoice: MenuModuleInterface = BikeScooterCategoryChoice
    bikeMotoCategoryChoice: MenuModuleInterface = BikeMotoCategoryChoice
    bikeParameters: MenuModuleInterface = BikeParameters
    bikeCriteriaChoice: MenuModuleInterface = BikeCriteriaChoice
    timeRequest: MenuModuleInterface = TimeRequest
    timeRequestDayWeekWhen: MenuModuleInterface = TimeRequestDayWeekWhen
    timeRequestDayWeekWhenSetDate: MenuModuleInterface = TimeRequestDayWeekWhenSetDate
    timeRequestHowManyDays: MenuModuleInterface = TimeRequestHowManyDays
    timeRequestHowManyMonths: MenuModuleInterface = TimeRequestHowManyMonths
    timeRequestHowManyMonthsSet: MenuModuleInterface = TimeRequestHowManyMonthsSet
    timeRequestMonthWhen: MenuModuleInterface = TimeRequestMonthWhen
    timeRequestMonthWhenSetDate: MenuModuleInterface = TimeRequestMonthWhenSetDate
    bikeHelmet: MenuModuleInterface = BikeHelmet
    requestGeoposition: MenuModuleInterface = RequestGeoposition
    carSize: MenuModuleInterface = CarSize
    carTransmission: MenuModuleInterface = CarTransmission
    carModels: MenuModuleInterface = CarModels
    comment: MenuModuleInterface = Comment

    @property
    def get(self) -> MenuModuleInterface:
        return self.value

class MenuModulesFactory:

    language: LanguageKey

    def __init__(self, language: LanguageKey):
        self.language = language

    def generateModuleClass(self, module: MenuModules) -> MenuModuleInterface:
        return module.value(self.language)
      