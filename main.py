import os
from pyrogram import Client, filters
from pyrogram.types import *

Bot = Client(
    "Calculator Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_TEXT = """Hᴇʟʟᴏ {},\n
I ᴀᴍ ᴀ sɪᴍᴘʟᴇ ᴄᴀʟᴄᴜʟᴀᴛᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛ\n\nSᴇɴᴅ ᴍᴇ /calculator

Mᴀᴅᴇ ʙʏ <a href="https://t.me/VAMPIRE_KING_NO_1">Tᴇʀʀᴏʀ Mɪᴄᴋᴇʏ</a>
"""
START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url='https://t.me/STMbOTsUPPORTgROUP'),
        ]
    ]
)
CALCULATE_TEXT = "Mᴀᴅᴇ Bʏ @VAMPIRE_KING_NO_1"
CALCULATE_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Dᴇʟ", callback_data="DEL"),
            InlineKeyboardButton("Aᴄ", callback_data="AC"),
            InlineKeyboardButton("(", callback_data="("),
            InlineKeyboardButton(")", callback_data=")")
        ],
        [
            InlineKeyboardButton("⑦", callback_data="7"),
            InlineKeyboardButton("⑧", callback_data="8"),
            InlineKeyboardButton("⑨", callback_data="9"),
            InlineKeyboardButton("÷", callback_data="/")
        ],
        [
            InlineKeyboardButton("④", callback_data="4"),
            InlineKeyboardButton("⑤", callback_data="5"),
            InlineKeyboardButton("⑥", callback_data="6"),
            InlineKeyboardButton("×", callback_data="*")
        ],
        [
            InlineKeyboardButton("①", callback_data="1"),
            InlineKeyboardButton("②", callback_data="2"),
            InlineKeyboardButton("③", callback_data="3"),
            InlineKeyboardButton("-", callback_data="-"),
        ],
        [
            InlineKeyboardButton(".", callback_data="."),
            InlineKeyboardButton("⓪", callback_data="0"),
            InlineKeyboardButton("=", callback_data="="),
            InlineKeyboardButton("+", callback_data="+"),
        ]
    ]
)


@Bot.on_message(filters.command(["start", "mickey",]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.mention)
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )


@Bot.on_message(filters.private & filters.command(["calc", "calculate", "calculator", "king"]))
async def calculate(bot, update):
    await update.reply_text(
        text=CALCULATE_TEXT,
        reply_markup=CALCULATE_BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_callback_query()
async def cb_data(bot, update):
        data = update.data
        try:
            message_text = update.message.text.split("\n")[0].strip().split("=")[0].strip()
            message_text = '' if CALCULATE_TEXT in message_text else message_text
            if data == "=":
                text = float(eval(message_text))
            elif data == "DEL":
                text = message_text[:-1]
            elif data == "AC":
                text = ""
            else:
                text = message_text + data
            await update.message.edit_text(
                text=f"{text}\n\n{CALCULATE_TEXT}",
                disable_web_page_preview=True,
                reply_markup=CALCULATE_BUTTONS
            )
        except Exception as error:
            print(error)


@Bot.on_inline_query()
async def inline(bot, update):
    if len(update.data) == 0:
        try:
            answers = [
                InlineQueryResultArticle(
                    title="Calculator",
                    description=f"New calculator",
                    input_message_content=InputTextMessageContent(
                        text=CALCULATE_TEXT,
                        disable_web_page_preview=True
                    ),
                    reply_markup=CALCULATE_BUTTONS
                )
            ]
        except Exception as error:
            print(error)
    else:
        try:
            message_text = update.message.text.split("\n")[0].strip().split("=")[0].strip()
            data = message_text.replace("×", "*").replace("÷", "/")
            text = float(eval(data))
            answers = [
                InlineQueryResultArticle(
                    title="Answer",
                    description=f"Results of your input",
                    input_message_content=InputTextMessageContent(
                        text=f"{data} = {text}",
                        disable_web_page_preview=True
                    )
                )
            ]
        except:
            pass
    await update.answer(answers)


Bot.run()
