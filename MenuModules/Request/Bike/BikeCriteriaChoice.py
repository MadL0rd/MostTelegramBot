from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant
import Core.Utils.Utils as utils

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class BikeCriteriaChoice(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.bikeCriteriaChoice

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleBikeCriteriaChoice, "")   
        
        return await self.handleUserMessage(ctx, msg, {})

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        
        messageText = ctx.text
        pull = storage.getJsonData(storage.PathConfig.botContentBikeCriteria)

        pullPrevious = [line for line in pull if line["type"] in data and data[line["type"]] == False]
        if len(pullPrevious) > 0:

            prevCriteria = pullPrevious[0]
            prevCriteriaName = prevCriteria["type"]

            if messageText in prevCriteria["values"]:
                storage.logToUserRequest(ctx.from_user, f"Критерий байка {prevCriteriaName}: {messageText}")
                data[prevCriteriaName] = True
            else:
                return self.canNotHandle(data)

        pull = [line for line in pull if line["type"] not in data]
        if len(pull) > 0:
            criteria = pull[0]
            criteriaName = criteria["type"]
            keyboardMarkup = utils.replyMarkupFromListOfButtons(criteria["values"])

            await msg.answer(
                ctx = ctx,
                text = criteria["type"],
                keyboardMarkup = keyboardMarkup
            )            

            data[f"{criteriaName}"] = False
            log.debug(data)

            return Completion(
                inProgress=True,
                didHandledUserInteraction=True,
                moduleData=data
            )

        return self.complete(nextModuleName = MenuModuleName.bikeHelmet.get)
        

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================

    @property
    def menuDict(self) -> dict:
        return {
            
        }