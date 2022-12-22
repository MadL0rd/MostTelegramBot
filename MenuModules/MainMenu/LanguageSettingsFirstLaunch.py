from MenuModules.MainMenu.LanguageSettings import LanguageSettings
from MenuModules.MenuModuleName import MenuModuleName

class LanguageSettingsFirstLaunch(LanguageSettings):
    
    namePrivate = MenuModuleName.languageSettingsFirstLaunch

    nextModule: MenuModuleName = MenuModuleName.onboarding
