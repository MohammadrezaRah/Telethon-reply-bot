import os

from telethon import events
from dotenv import load_dotenv
from telethon import TelegramClient
from datetime import datetime, timedelta


last_reply_friday = {}
last_reply_out_business = {}
last_reply_normal = {}



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


@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):

    if not event.is_private:
        return

    user_id = event.sender_id
    now = datetime.now()




    # جمعه
    if now.weekday() == 4:

        # بررسی زمان آخرین پاسخ به این کاربر
        last_reply = last_reply_friday.get(user_id)

        if last_reply:
            if now - last_reply < timedelta(hours=12):
                return

        message = (
            "👋 سلام، پیام شما دریافت شد.\n\n"
            "📅 امروز جمعه است و پاسخگویی مجموعه انجام نمی‌شود.\n"
            "⏳ پیام شما در اولین فرصت کاری بررسی و پاسخ داده خواهد شد."
        )

        # ثبت زمان پاسخ
        last_reply_friday[user_id] = now

    # خارج از ساعت کاری
    elif (
            now.hour < 9
            or (now.hour == 9 and now.minute < 30)
            or now.hour > 20
            or (now.hour == 20 and now.minute >= 30)
    ):

        # بررسی زمان آخرین پاسخ به این کاربر
        last_reply = last_reply_out_business.get(user_id)
        
        if last_reply:
            if now - last_reply < timedelta(hours=12):
                return

        message = (
            "👋 سلام، پیام شما دریافت شد.\n\n"
            "🕐 ساعت پاسخگویی مجموعه از ۱۰ تا ۲۱ می‌باشد.\n"
            "⏳ پیام شما در اولین زمان کاری بررسی و پاسخ داده خواهد شد."
        )
        # ثبت زمان پاسخ
        last_reply_out_business[user_id] = now

    # داخل ساعت کاری
    else:

        # بررسی زمان آخرین پاسخ به این کاربر
        last_reply = last_reply_normal.get(user_id)

        if last_reply:
            if now - last_reply < timedelta(hours=8):
                return

        message = (
            "👋 سلام، پیام شما دریافت شد.\n\n"
            "📩 اگر مطلب، توضیح یا سؤال دیگری دارید، ارسال کنید؛ "
            "در غیر این صورت لطفاً تا دریافت پاسخ ادمین، "
            "از ارسال پیام‌های مکرر خودداری فرمایید.\n\n"
            "🙏 ممنون از همراهی شما."
        )

        # ثبت زمان پاسخ
        last_reply_normal[user_id] = now

    await event.reply(message)





client.start()

print("🤖 Auto Reply is active...")

client.run_until_disconnected()

