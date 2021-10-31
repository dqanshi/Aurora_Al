print("[AURORA]: Checking System ...")
import re
import random
from os import path
from asyncio import (gather, get_event_loop, sleep)

from aiohttp import ClientSession
from pyrogram import (Client, filters, idle)
from Python_ARQ import ARQ
from os import environ

print("[AURORA]: Initializing Config Vars ...")
bot_token = str(environ.get("TOKEN", None))
B_UNAME = str(environ.get("BOT_USERNAME", None))
CHARA_NAME = str(environ.get("BOT_NAME", None))
ARQ_API_KEY = str(environ.get("ARQ_API_KEY", None))
LANGUAGE = str(environ.get("LANGUAGE", "en"))
bot_id = int(environ.get("BOT_ID", None))
api_id = int(environ.get("API_ID"))
api_hash = str(environ.get("HASH", None))
ARQ_API_BASE_URL = str(environ.get("ARQ_API_BASE_URL", "https://thearq.tech"))

print("[AURORA]: Initializing Bot Client ...")
luna = Client(":memory:",
              bot_token=bot_token,
              api_id=api_id,
              api_hash=api_hash,
)
arq = None

HELP = """
Here is my help menu and command list.

/help - To See This Message
/about - About My Creator

Im a chatbot designed for chatting with you,
Send me any message then i can reply you!
"""

ABOUT = """
😘 My Dev is CoNqUeRoR_mEskEtTeR

Built with ❤ and Pyrogram.
"""

RTEXT = ["I've started...",
         "Hey am here>///<",
         "What are u doin'?",
         "What the hell?",
         "Now what?",
         "How are you?",
         "Why are u here! -_-",
         "Damn! *run away",
         "Be cool lol>///<",
         "Heya am alive?",
         "My darling is @CoNqUeRoR_mEsKeTtEr",
         "Lol am here!!",
         "How can l help you",
         "Are you here for checking me?"
        ]

async def lunaQuery(query: str, user_id: int):
    query = (
        query
        if LANGUAGE == "en"
        else (await arq.translate(query, "en")).result.translatedText
    )
    resp = (await arq.luna(query, user_id)).result
    return (
        resp
        if LANGUAGE == "en"
        else (
            await arq.translate(resp, LANGUAGE)
        ).result.translatedText
    )


async def type_and_send(message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, "typing")
    response, _ = await gather(lunaQuery(query, user_id), sleep(2))
    if "Luna" in response:
        respa = response.replace("Luna", f"{CHARA_NAME}")
    else:
        respa = response
    if "Aco" in respa:
        respb = respa.replace("Aco", f"{CHARA_NAME}")
    else:
        respb = respa
    await message.reply_text(respb)
    await message._client.send_chat_action(chat_id, "cancel")


@luna.on_message(filters.command("repo") & ~filters.edited)
async def repo(_, message):
    await message.reply_text(
        "[GitHub](https://github.com/)",
        
        disable_web_page_preview=True,
    )


@luna.on_message(filters.command(["help", "help@Aurorachat_Robot"]) & ~filters.edited)
async def start(_, message):
    await luna.send_chat_action(message.chat.id, "typing")
    await sleep(2)
    await message.reply_text(HELP)

@luna.on_message(filters.command(["about", f"about@{B_UNAME}"]) & ~filters.edited)
async def start(_, message):
    await luna.send_chat_action(message.chat.id, "typing")
    await sleep(2)
    await message.reply_text(ABOUT)

@luna.on_message(
    ~filters.private
    & filters.text
    & ~filters.command(["start", f"start@{B_UNAME}"])
    & ~filters.edited,
    group=69,
)
async def chat(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return
        from_user_id = message.reply_to_message.from_user.id
        if from_user_id != bot_id:
            return
    else:
        match = re.search(
            f"[.|\n]{0,}{CHARA_NAME}[.|\n]{0,}",
            message.text.strip(),
            flags=re.IGNORECASE,
        )
        if not match:
            return
    await type_and_send(message)


@luna.on_message(
    filters.private
    & ~filters.command(["start", f"start@{B_UNAME}"])
    & ~filters.edited
)
async def chatpm(_, message):
    if not message.text:
        await message.reply_text("Uff... ignoring...")
        return
    await type_and_send(message)


@luna.on_message(filters.command(["start", f"start@{B_UNAME}"]) & ~filters.edited)
async def startt(_, message):
    rand = random.choice(RTEXT)
    await message.reply_text(rand)


async def main():
    global arq
    session = ClientSession()
    print("[AURORA] Initializing Arq Client ...")
    arq = ARQ(ARQ_API_BASE_URL, ARQ_API_KEY, session)

    await luna.start()
    print(
        """
--------------------
| Chatbot Started! |
--------------------
|   CoNqUeRoR_mEsKeTtEr   |
--------------------
"""
    )
    await idle()


loop = get_event_loop()
loop.run_until_complete(main())
