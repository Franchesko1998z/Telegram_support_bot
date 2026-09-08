# -*- coding: utf-8 -*-
import os
import logging
import threading
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 6013396411  # آیدی عددی خودت

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== لینک Worker در Cloudflare ==========
YOUR_WORKER_URL = "https://tg-bridge.franchesko1998z.workers.dev"  # <-- لینک Worker خودت

# ========== دکمه‌های منوی اصلی ==========
MAIN_KEYBOARD = [
    ["🛒 خرید کانفیگ"],
    ["💰 قیمت‌ها", "📞 پشتیبانی"],
    ["ℹ️ راهنما"]
]

# ========== تابع شروع ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        "👋 به ربات فروش کانفیگ خوش اومدی!",
        reply_markup=reply_markup
    )

# ========== تابع مدیریت پیام‌ها ==========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🛒 خرید کانفیگ":
        await update.message.reply_text("📌 لطفاً نوع کانفیگ مورد نظر خود را انتخاب کنید.")
    elif text == "💰 قیمت‌ها":
        await update.message.reply_text("📊 لیست قیمت‌ها:\n\n🌟 تک لوکیشن ویژه: ۳۵۰,۰۰۰ تومان")
    elif text == "📞 پشتیبانی":
        await update.message.reply_text("📞 پشتیبانی: @YourSupportID")
    elif text == "ℹ️ راهنما":
        await update.message.reply_text("📖 راهنمای استفاده:\n1. خرید کانفیگ\n2. پرداخت\n3. دریافت کانفیگ")
    else:
        await update.message.reply_text("❌ گزینه نامعتبر! لطفاً از دکمه‌ها استفاده کن.")

# ========== اجرای ربات با Cloudflare Worker ==========
def run_bot():
    app = Application.builder().token(TOKEN).base_url(YOUR_WORKER_URL).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("🤖 ربات از طریق Cloudflare Worker روشن شد!")
    app.run_polling(drop_pending_updates=True)

# ========== وب سرور برای Render ==========
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "🤖 ربات فعال است!"

@flask_app.route('/health')
def health():
    return "OK", 200

# ========== اجرای همزمان ==========
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)
