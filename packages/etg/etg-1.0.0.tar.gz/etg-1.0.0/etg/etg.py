import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

_bot = None
_dp = None
_callbacks = {}

def setToken(token: str):
    global _bot, _dp
    _bot = Bot(token=token)
    _dp = Dispatcher()

def onCommand(cmd: str, response):
    if _dp is None or _bot is None:
        raise RuntimeError("Сначала вызови setToken() с токеном")

    if isinstance(response, str) and response.startswith("inline:"):
        button_text = response.split("inline:")[1].strip()
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=button_text, callback_data=button_text)]
        ])

        @_dp.message(Command(commands=[cmd.strip('/')]))
        async def handler(message: types.Message):
            await message.answer("Нажми кнопку ниже:", reply_markup=keyboard)

    elif isinstance(response, str):
        @_dp.message(Command(commands=[cmd.strip('/')]))
        async def handler(message: types.Message):
            await message.answer(response)

    elif callable(response):
        @_dp.message(Command(commands=[cmd.strip('/')]))
        async def handler(message: types.Message):
            await response(message)

def onFlyButton(name: str, response):
    if _dp is None:
        raise RuntimeError("Сначала вызови setToken() с токеном")

    _callbacks[name] = response

    @_dp.callback_query(lambda c: c.data == name)
    async def handler(callback: types.CallbackQuery):
        chat_id = callback.message.chat.id
        resp = _callbacks.get(name)

        if callable(resp):
            await resp(callback)
        else:
            await _bot.send_message(chat_id, resp)

        await callback.answer()

def Send(chat_id, text):
    if _bot is None:
        raise RuntimeError("Бот не инициализирован")

    async def send_async():
        await _bot.send_message(chat_id, text)

    asyncio.run(send_async())

def startBot():
    if _dp is None:
        raise RuntimeError("Сначала вызови setToken() с токеном")

    async def main():
        try:
            await _dp.start_polling(_bot)
        finally:
            await _bot.session.close()

    asyncio.run(main())
