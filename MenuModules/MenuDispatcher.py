import json
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove

from Core.MessageSender import MessageSender, CallbackMessageSender
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant
import Core.StorageManager.StorageFactory as storageFactory

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModules import MenuModules as menu, MenuModulesFactory

from logger import logger as log

msg = MessageSender()
callbackMsg = CallbackMessageSender()

async def handleUserStart(ctx: Message):

    userTg = ctx.from_user
    log.info(f"Did handle User{userTg.id} start message {ctx.text}")

    userLanguage = storageFactory.getLanguageForUser(userTg)
    storage = storageFactory.getStorageForLanguage(userLanguage)
    log.info(userLanguage)
    menuFactory = MenuModulesFactory(userLanguage)
    
    userInfo = storage.getUserInfo(userTg)

    module: MenuModuleInterface = menuFactory.generateModuleClass(menu.languageSettingsFirstLaunch)
    log.debug(module.name)
    completion: Completion = await module.handleModuleStart(ctx, msg)
    if completion.inProgress == True:
        userInfo["state"] = {
            "module": module.name,
            "data": completion.moduleData 
        }
    else:
        userInfo["state"] = {}
    storage.updateUserData(userTg, userInfo)

async def handleUserMessage(ctx: Message):

    userTg = ctx.from_user
    log.info(f"Did handle User{userTg.id} message: {ctx.text}")

    userLanguage = storageFactory.getLanguageForUser(userTg)
    storage = storageFactory.getStorageForLanguage(userLanguage)
    menuFactory = MenuModulesFactory(userLanguage)

    userInfo = storage.getUserInfo(userTg)
    menuState = userInfo["state"]

    storage.logToUserHistory(userTg, event.sendMessage, ctx.text)

    if "ban" in userInfo and userInfo["ban"] == True:
        unknownText = storage.getTextConstant(textConstant.unknownState)
        await msg.answer(ctx, unknownText)
        return
    
    # Try to find current menu module
    menuState = userInfo["state"]
    module: MenuModuleInterface = None
    completion: Completion = None
    data = {}
    try:
        menuModuleName = menuState["module"]
        module = [menuFactory.generateModuleClass(module) for module in menu if menuFactory.generateModuleClass(module).name == menuModuleName][0]
        log.info(f"Founded module: {module.name}")

    except:
        log.info(f"Error while finding module")

    if module is not None and ctx.text != "/back_to_menu":
        data = menuState["data"]
        completion: Completion = await module.handleUserMessage(
            ctx=ctx,
            msg=msg,
            data=data
        )

    userLanguage = storageFactory.getLanguageForUser(userTg)
    storage = storageFactory.getStorageForLanguage(userLanguage)
    menuFactory = MenuModulesFactory(userLanguage)

    # Start next module if needed
    moduleNext: MenuModuleInterface = None
    if completion is None:
        moduleNext = menuFactory.generateModuleClass(menu.mainMenu)
    elif completion.inProgress == False:
        log.info(f"Module {module.name} completed")
        try:
            menuModuleName = completion.nextModuleNameIfCompleted
            moduleNext = [menuFactory.generateModuleClass(module) for module in menu if menuFactory.generateModuleClass(module).name == menuModuleName][0]
            log.info(f"Founded module: {module.name}")

        except:
            log.info(f"Error while finding module from completion")
            moduleNext = menuFactory.generateModuleClass(menu.mainMenu)

    # Emergency reboot
    if ctx.text == "/back_to_menu":
        moduleNext = menuFactory.generateModuleClass(menu.mainMenu)

    if moduleNext is not None:
        module = moduleNext
        menuState = {
            "module": module.name,
            "data": {}
        }
        completion: Completion = await module.handleModuleStart(
            ctx = ctx,
            msg=msg
        )

    adminPassword = "siBkdnPm4jpZASeuyct98F6rMQ7gDhwb"
    if ctx.text == adminPassword:
        if "isAdmin" not in userInfo or userInfo["isAdmin"] == False:
            userInfo = storage.getUserInfo(userTg)
            userInfo["isAdmin"] = True
            storage.updateUserData(userTg, userInfo)
            await msg.answer(
                ctx=ctx, 
                text="Вы получили права администратора\nЧтобы получить доступ к новым функциям вернитесь в главное меню",
                keyboardMarkup=ReplyKeyboardMarkup()
            )
        else:
            await msg.answer(
                ctx=ctx, 
                text="У Вас уже есть права администратора",
                keyboardMarkup=ReplyKeyboardMarkup()
            )
    elif completion.didHandledUserInteraction == False:
        unknownText = storage.getTextConstant(textConstant.unknownState)
        await msg.answer(ctx, unknownText)

    menuState = {
        "module": module.name,
        "data": completion.moduleData 
    }

    userInfo = storage.getUserInfo(userTg)
    userInfo["state"] = menuState
    storage.updateUserData(userTg, userInfo)

async def handleCallback(ctx: CallbackQuery):

    await ctx.message.edit_reply_markup(InlineKeyboardMarkup())

    userTg = ctx.from_user
    log.info(f"Did handle User{userTg.id} CallbackQuery: {ctx.data}")

    userLanguage = storageFactory.getLanguageForUser(userTg)
    storage = storageFactory.getStorageForLanguage(userLanguage)
    menuFactory = MenuModulesFactory(userLanguage)

    module = menuFactory.generateModuleClass(menu.mainMenu)

    completion: Completion = await module.handleModuleStart(
        ctx = ctx,
        msg = callbackMsg
    )

    menuState = {
        "module": module.name,
        "data": completion.moduleData 
    }

    userInfo = storage.getUserInfo(userTg)
    userInfo["state"] = menuState
    storage.updateUserData(userTg, userInfo)