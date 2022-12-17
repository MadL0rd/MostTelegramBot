from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.MessageSender import MessageSender
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
        self.storage.logToUserHistory(ctx.from_user, event.startModuleBikeCriteriaChoice, "")   
        
        return await self.handleUserMessage(ctx, msg, {})

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        
        messageText = ctx.text
        pull = self.storage.getJsonData(self.storage.path.botContentBikeCriteria)
        request = self.storage.getUserRequest(ctx.from_user)
        if textConstant.orderStepKeyBikeScooterCategory.value in request:
            bikeName = request[textConstant.orderStepKeyBikeScooterCategory.value]["value"]
            pull = [criteria for criteria in pull if self.getText(textConstant.orderStepValueAll) in criteria["bikes"] or bikeName in criteria["bikes"]]

        pullPrevious = [criteria for criteria in pull if criteria["id"] in data and data[criteria["id"]] == False]
        if len(pullPrevious) > 0:

            prevCriteria = pullPrevious[0]
            prevCriteriaId = prevCriteria["id"]
            prevCriteriaTitle = prevCriteria["title"]

            if prevCriteria["customTextEnable"] == True or messageText in prevCriteria["values"]:
                self.storage.logToUserRequestCustom(
                    user = ctx.from_user,
                    codingKey = f"{textConstant.bikeCriteriaChoice.value}.{prevCriteriaId}",
                    title = prevCriteriaTitle,
                    value = messageText
                )
                    
                # Ставим критерию True, т.к. критерий обработан и данные внесены в request.json
                data[prevCriteriaId] = True
            else:
                return self.canNotHandle(data)

        # отфильтровали все критерии и оставили в pull только те, 
        # которые юзер ещё не видел
        pull = [criteria for criteria in pull if criteria["id"] not in data]
        if len(pull) > 0:
            criteria = pull[0]
            criteriaId = criteria["id"]
            keyboardMarkup = utils.replyMarkupFromListOfButtons(criteria["values"])

            await msg.answer(
                ctx = ctx,
                text = criteria["question"],
                keyboardMarkup = keyboardMarkup
            )            
            # ставим False критерию, т.к. он уже отправлен пользователю, 
            # но ответ на него мы ещё не получили
            data[criteriaId] = False
            log.debug(data)

            return Completion(
                inProgress=True,
                didHandledUserInteraction=True,
                moduleData=data
            )

        await msg.answer(
                ctx = ctx,
                text = self.getText(textConstant.bikeButtonCriteriaFinal),
                keyboardMarkup = ReplyKeyboardMarkup()
            ) 
        return self.complete(nextModuleName = MenuModuleName.bikeHelmet.get)
        
    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================