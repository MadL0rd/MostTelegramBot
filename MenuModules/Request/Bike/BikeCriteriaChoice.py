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
        # bikeName = getJsonData(....request.json)["bikeName"]
        # pull = [criteria for criteria in pull]............
        # вытаскиваю название байка и делаю фильтрацию
        # TODO: ОБЪЯСНИСЬ БЛЯТЬ!
        pullPrevious = [criteria for criteria in pull if criteria["type"] in data and data[criteria["type"]] == False]
        if len(pullPrevious) > 0:

            prevCriteria = pullPrevious[0]
            prevCriteriaName = prevCriteria["type"]

            if prevCriteria["customTextEnable"] == True or messageText in prevCriteria["values"]:
                storage.logToUserRequest(ctx.from_user, f"bikeCriteriaChoice.{prevCriteriaName}",f"Критерий байка {prevCriteriaName}: {messageText}")
                # Ставим критерию True, т.к. критерий обработан и данные внесены в request.json
                data[prevCriteriaName] = True
            else:
                return self.canNotHandle(data)

        # отфильтровали все критерии и оставили в pull только те, 
        # которые юзер ещё не видел
        pull = [criteria for criteria in pull if criteria["type"] not in data]
        if len(pull) > 0:
            criteria = pull[0]
            criteriaName = criteria["type"]
            keyboardMarkup = utils.replyMarkupFromListOfButtons(criteria["values"])

            await msg.answer(
                ctx = ctx,
                text = criteria["type"],
                keyboardMarkup = keyboardMarkup
            )            
            # ставим False критерию, т.к. он уже отправлен пользователю, 
            # но ответ на него мы ещё не получили
            data[criteriaName] = False
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