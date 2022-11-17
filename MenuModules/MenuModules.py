import enum
from MenuModules.Onboarding.Onboarding import Onboarding
from MenuModules.MainMenu.MainMenu import MainMenu
from MenuModules.MenuModuleInterface import MenuModuleInterface
from MenuModules.AdminMenu.AdminMenu import AdminMenu
from MenuModules.Request.Bike.BikeCommitment import BikeCommitment
from MenuModules.Request.Bike.BikeMotoCategory import BikeMotoCategory
from MenuModules.Request.Bike.BikeParameters import BikeParameters
from MenuModules.Request.Bike.BikeScooterOrMoto import BikeScooterOrMoto
from MenuModules.Request.Bike.BikeScooterCategory import BikeScooterCategory
from MenuModules.Request.Bike.BikeCriteriaChoice import BikeCriteriaChoice
from MenuModules.Request.BikeHelmet import BikeHelmet
from MenuModules.Request.Car.CarModels import CarModels
from MenuModules.Request.Car.CarSize import CarSize
from MenuModules.Request.Car.CarTransmission import CarTransmission
from MenuModules.Request.RequestGeoposition import RequestGeoposition
from MenuModules.Request.Time.TimeRequest import TimeRequest
from MenuModules.Request.Time.TimeRequestDayWeekWhen import TimeRequestDayWeekWhen
from MenuModules.Request.Time.TimeRequestHowManyDays import TimeRequestHowManyDays
from MenuModules.Request.Time.TimeRequestHowManyMonths import TimeRequestHowManyMonths
from MenuModules.Request.Time.TimeRequestMonthWhen import TimeRequestMonthWhen




class MenuModules(enum.Enum):

    onboarding: MenuModuleInterface = Onboarding()
    mainMenu: MenuModuleInterface = MainMenu()
    adminMenu: MenuModuleInterface = AdminMenu()
    bikeCommitment: MenuModuleInterface = BikeCommitment()
    bikeScooterOrMoto: MenuModuleInterface = BikeScooterOrMoto()
    bikeMotoCategory: MenuModuleInterface = BikeMotoCategory()
    bikeScooterCategory: MenuModuleInterface = BikeScooterCategory()
    bikeParameters: MenuModuleInterface = BikeParameters()
    bikeCriteriaChoice: MenuModuleInterface = BikeCriteriaChoice()
    timeRequest: MenuModuleInterface = TimeRequest()
    timeRequestDayWeekWhen: MenuModuleInterface = TimeRequestDayWeekWhen()
    timeRequestHowManyDays: MenuModuleInterface = TimeRequestHowManyDays()
    timeRequestHowManyMonths: MenuModuleInterface = TimeRequestHowManyMonths()
    timeRequestMonthWhen: MenuModuleInterface = TimeRequestMonthWhen()
    bikeHelmet: MenuModuleInterface = BikeHelmet()
    requestGeoposition: MenuModuleInterface = RequestGeoposition()
    carSize: MenuModuleInterface = CarSize()
    carTransmission: MenuModuleInterface = CarTransmission()
    carModels: MenuModuleInterface = CarModels()

    
    @property
    def get(self) -> MenuModuleInterface:
        return self.value