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
from MenuModules.Request.Time.TimeRequest import TimeRequest




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
    

    
    @property
    def get(self) -> MenuModuleInterface:
        return self.value