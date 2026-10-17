import os

from zoneinfo import ZoneInfo
from telethon import events
from dotenv import load_dotenv
from telethon import TelegramClient
from datetime import datetime, timedelta


load_dotenv()


API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")


PROXY = (
    "socks5",
    "127.0.0.1",
    10808
)


client = TelegramClient(
    "gamenest_user",
    API_ID,
    API_HASH,
    proxy=PROXY
)


def outside(argue):
    return argue.hour < 10 or argue.hour > 20


@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):

    if not event.is_private:
        return

    sender = await event.get_sender()

    if sender.bot:
        print("bot chat")
        return

    iran_tz = ZoneInfo("Asia/Tehran")

    now = datetime.now(iran_tz)


    chat = await event.get_chat()

    # گرفتن دو پیام آخر چت
    messages = await client.get_messages(
        chat,
        limit=2
    )

    # پیام فعلی + پیام قبلی
    if len(messages) >= 2:

        last_message = messages[1]

        last_message_time = last_message.date.astimezone(iran_tz)

        elapsed = now - last_message_time

    else:

        last_message_time = None
        elapsed = None


    # جمعه
    if now.weekday() == 4:
        print("friday")

        # اگر پیام قبلی جمعه بوده، فاصله زمانی را بررسی کن
        if elapsed is not None \
                and last_message_time.weekday() == 4 \
                and elapsed < timedelta(hours=12):

            print("replied before")
            return


        message = (
            "👋 سلام، پیام شما دریافت شد.\n\n"
            "📅 امروز جمعه است و پاسخگویی مجموعه انجام نمی‌شود.\n"
            "⏳ پیام شما در اولین فرصت کاری بررسی و پاسخ داده خواهد شد."
        )


    # خارج از ساعت کاری
    elif outside(now):

        print("out hours")

        # اگر پیام قبلی هم خارج از ساعت کاری بوده
        if last_message_time is not None:

            if outside(last_message_time) and elapsed < timedelta(hours=12):
                print("replied before")
                return

        message = (
            "👋 سلام، پیام شما دریافت شد.\n\n"
            "🕐 ساعت پاسخگویی مجموعه از ساعت ۱۰ الی ۲۱:۰۰ می‌باشد.\n"
            "⏳ پیام شما در اولین زمان کاری بررسی و پاسخ داده خواهد شد."
        )


    # داخل ساعت کاری
    else:

        print("in hours")

        # بررسی زمان آخرین پیام چت
        if elapsed is not None and elapsed < timedelta(hours=8):
            print("replied before")
            return

        message = (
            "👋 سلام، پیام شما دریافت شد.\n\n"
            "📩 اگر مطلب، توضیح یا سؤال دیگری دارید، ارسال کنید؛\n"
            "در غیر این صورت لطفاً تا دریافت پاسخ ادمین، "
            "از ارسال پیام‌های مکرر خودداری فرمایید.\n\n"
            "🙏 ممنون از همراهی شما."
        )


    await event.reply(message)


client.start()


print("🤖 Auto Reply is active...")


client.run_until_disconnected()

