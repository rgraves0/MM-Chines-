import logging
import asyncio
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ContextTypes
)

# Config & Token
from src.config import TELEGRAM_TOKEN

# Database စတင်ဖွင့်ရန်
from src.database import init_db

# Handlers
from src.handlers.messages import start, handle_text, handle_voice, user_callback
from src.handlers.admin import admin_panel, admin_callback

# အသစ်ထည့်လိုက်တဲ့ Admin + User Management System
from src.handlers.admin_commands import (
    request_access,
    chat_with_admin,
    approve_user,
    reject_user,
    kick_user,
    ban_user,
    unban_user,
    reply_to_user,
    broadcast_message,
    admin_callback as management_callback  # နာမည်မထပ်အောင်
)

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database စတင်ဖွင့်ရန်
async def startup_tasks(app):
    await init_db()
    logger.info("Database initialized and tables created if not exist.")

if __name__ == '__main__':
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_TOKEN is missing in .env file")
        exit(1)

    print("Bot is starting...")

    # Application တည်ဆောက်ခြင်း
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Startup task (Database ဖန်တီးရန်)
    application.job_queue.run_once(startup_tasks, 0)

    # ====================== BASIC COMMANDS ======================
    application.add_handler(CommandHandler('start', start))

    # ====================== USER FEATURES ======================
    application.add_handler(CommandHandler("request", request_access))      # အသုံးပြုချင်ရင် တောင်းဆိုမယ်
    application.add_handler(CommandHandler("chat", chat_with_admin))        # Admin ကို စာပို့မယ်

    # ====================== ADMIN PANEL ======================
    application.add_handler(CommandHandler('admin', admin_panel))
    application.add_handler(CallbackQueryHandler(admin_callback, pattern="^admin_"))

    # ====================== ADMIN MANAGEMENT COMMANDS ======================
    application.add_handler(CommandHandler("approve", approve_user))     # /approve 123456789 30
    application.add_handler(CommandHandler("reject", reject_user))       # /reject 123456789 အကြောင်းပြချက်
    application.add_handler(CommandHandler("kick", kick_user))           # /kick 123456789
    application.add_handler(CommandHandler("ban", ban_user))             # /ban 123456789 စည်းကမ်းဖောက်ဖျက်
    application.add_handler(CommandHandler("unban", unban_user))         # /unban 123456789
    application.add_handler(CommandHandler("reply", reply_to_user))      # /reply 123456789 မင်္ဂလာပါ
    application.add_handler(CommandHandler("broadcast", broadcast_message))  # /broadcast အားလုံးပါ

    # ====================== MESSAGE HANDLERS ======================
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))

    # ====================== CALLBACK HANDLERS ======================
    # Explain More button
    application.add_handler(CallbackQueryHandler(user_callback, pattern="^explain"))

    # Admin Management Inline Buttons (approve, reject, replyto)
    application.add_handler(CallbackQueryHandler(
        management_callback,
        pattern="^(approve_|reject_|replyto_)"
    ))

    # ====================== START BOT ======================
    print("Bot စတင်လည်ပတ်နေပါပြီ...")
    print("Developed by @MyanmarTecharea")

    # Polling နဲ့ လည်ပတ်မယ် (Zeabur/Railway မှာ webhook သုံးရင် ဒီအစား run_webhook သုံးပါ)
    application.run_polling(
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True
    )
