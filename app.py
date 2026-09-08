# -*- coding: utf-8 -*-
import os
import logging
import threading
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 6013396411  # آیدی عددی خودت رو بذار

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        "👋 به **TP VPN** خوش اومدی!\n\n"
        "✅ فروش کانفیگ‌های پرسرعت و پایدار\n"
        "✅ پشتیبانی ۲۴/۷\n"
        "✅ قیمت‌های مناسب\n\n"
        "یکی از گزینه‌های زیر رو انتخاب کن:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ========== تابع مدیریت پیام‌ها ==========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # ----- منوی اصلی -----
    if text == "🛒 خرید کانفیگ":
        keyboard = [
            ["🌟 تک لوکیشن ویژه"],
            ["🌍 مولتی لوکیشن"],
            ["🔙 بازگشت"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🗂 **دسته‌بندی محصولات:**\n\n"
            "🌟 تک لوکیشن ویژه: فقط یک لوکیشن خاص (مثلاً آمریکا)\n"
            "🌍 مولتی لوکیشن: دسترسی به چندین لوکیشن\n\n"
            "لطفاً یکی رو انتخاب کن:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        context.user_data["step"] = "main_category"

    # ===== انتخاب نوع سرویس =====
    elif context.user_data.get("step") == "main_category" and text == "🌟 تک لوکیشن ویژه":
        keyboard = [
            ["🇺🇸 آمریکا ویژه"],
            ["🇩🇪 آلمان ویژه"],
            ["🇳🇱 هلند ویژه"],
            ["🔙 بازگشت"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🌟 **تک لوکیشن ویژه:**\n\n"
            "لطفاً لوکیشن مورد نظرت رو انتخاب کن:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        context.user_data["step"] = "single_location"

    elif context.user_data.get("step") == "main_category" and text == "🌍 مولتی لوکیشن":
        keyboard = [
            ["📊 مولتی حجمی"],
            ["♾️ مولتی نامحدود"],
            ["🔙 بازگشت"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🌍 **مولتی لوکیشن:**\n\n"
            "📊 مولتی حجمی: حجم مشخص (۱۵، ۲۰، ۳۰، ... گیگ)\n"
            "♾️ مولتی نامحدود: بدون محدودیت حجم\n\n"
            "لطفاً یکی رو انتخاب کن:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        context.user_data["step"] = "multi_type"

    # ===== تک لوکیشن ویژه (نمایش قیمت) =====
    elif context.user_data.get("step") == "single_location" and text != "🔙 بازگشت":
        location = text
        # قیمت‌های ویژه برای تک لوکیشن (با ۱۵۰,۰۰۰ اضافه)
        await update.message.reply_text(
            f"✅ **سفارش تک لوکیشن ویژه:**\n\n"
            f"🌍 لوکیشن: {location}\n"
            f"💰 قیمت: ۳۵۰,۰۰۰ تومان\n"
            f"📦 حجم: ۵۰ گیگ\n"
            f"⏰ مدت: ۳۰ روز\n\n"
            f"💳 برای پرداخت، به ادمین پیام بده:\n"
            f"📩 @YourSupportID",
            parse_mode="Markdown"
        )
        context.user_data.clear()

    # ===== مولتی حجمی =====
    elif context.user_data.get("step") == "multi_type" and text == "📊 مولتی حجمی":
        keyboard = [
            ["۱۵ گیگ - ۵۲۵,۰۰۰"],
            ["۲۰ گیگ - ۶۵۰,۰۰۰"],
            ["۳۰ گیگ - ۹۰۰,۰۰۰"],
            ["۴۰ گیگ - ۱,۱۵۰,۰۰۰"],
            ["۵۰ گیگ - ۱,۴۰۰,۰۰۰"],
            ["🔙 بازگشت"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "📊 **مولتی حجمی:**\n\n"
            "لطفاً حجم مورد نظرت رو انتخاب کن:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        context.user_data["step"] = "multi_volume"

    # ===== مولتی نامحدود =====
    elif context.user_data.get("step") == "multi_type" and text == "♾️ مولتی نامحدود":
        keyboard = [
            ["♾️ ۱ ماهه - ۵۰۰,۰۰۰"],
            ["♾️ ۳ ماهه - ۱,۲۰۰,۰۰۰"],
            ["♾️ ۶ ماهه - ۲,۰۰۰,۰۰۰"],
            ["🔙 بازگشت"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "♾️ **مولتی نامحدود:**\n\n"
            "بدون محدودیت حجم\n"
            "دسترسی به همه لوکیشن‌ها\n\n"
            "لطفاً مدت مورد نظرت رو انتخاب کن:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        context.user_data["step"] = "multi_unlimited"

    # ===== نمایش قیمت نهایی (مولتی حجمی) =====
    elif context.user_data.get("step") == "multi_volume" and text != "🔙 بازگشت":
        await update.message.reply_text(
            f"✅ **سفارش مولتی حجمی:**\n\n"
            f"📦 حجم: {text}\n"
            f"🌍 لوکیشن‌ها: همه لوکیشن‌ها\n"
            f"⏰ مدت: ۳۰ روز\n\n"
            f"💳 برای پرداخت، به ادمین پیام بده:\n"
            f"📩 @YourSupportID",
            parse_mode="Markdown"
        )
        context.user_data.clear()

    # ===== نمایش قیمت نهایی (مولتی نامحدود) =====
    elif context.user_data.get("step") == "multi_unlimited" and text != "🔙 بازگشت":
        await update.message.reply_text(
            f"✅ **سفارش مولتی نامحدود:**\n\n"
            f"♾️ مدت: {text}\n"
            f"🌍 لوکیشن‌ها: همه لوکیشن‌ها\n"
            f"📦 حجم: نامحدود\n\n"
            f"💳 برای پرداخت، به ادمین پیام بده:\n"
            f"📩 @YourSupportID",
            parse_mode="Markdown"
        )
        context.user_data.clear()

    # ===== قیمت‌ها =====
    elif text == "💰 قیمت‌ها":
        await update.message.reply_text(
            "📊 **لیست قیمت‌ها:**\n\n"
            "🌟 **تک لوکیشن ویژه:**\n"
            "• ۵۰ گیگ / ۳۰ روز: ۳۵۰,۰۰۰ تومان\n\n"
            "🌍 **مولتی حجمی:**\n"
            "• ۱۵ گیگ: ۵۲۵,۰۰۰ تومان\n"
            "• ۲۰ گیگ: ۶۵۰,۰۰۰ تومان\n"
            "• ۳۰ گیگ: ۹۰۰,۰۰۰ تومان\n"
            "• ۴۰ گیگ: ۱,۱۵۰,۰۰۰ تومان\n"
            "• ۵۰ گیگ: ۱,۴۰۰,۰۰۰ تومان\n\n"
            "♾️ **مولتی نامحدود:**\n"
            "• ۱ ماهه: ۵۰۰,۰۰۰ تومان\n"
            "• ۳ ماهه: ۱,۲۰۰,۰۰۰ تومان\n"
            "• ۶ ماهه: ۲,۰۰۰,۰۰۰ تومان",
            parse_mode="Markdown"
        )

    # ===== پشتیبانی =====
    elif text == "📞 پشتیبانی":
        await update.message.reply_text(
            "📞 **ارتباط با پشتیبانی:**\n\n"
            "🆔 آیدی تلگرام: @YourSupportID\n"
            "⏰ پاسخگویی: ۹ صبح تا ۱۲ شب\n\n"
            "📌 برای پیگیری سفارش، لطفاً شماره سفارش خود را ارسال کن.",
            parse_mode="Markdown"
        )

    # ===== راهنما =====
    elif text == "ℹ️ راهنما":
        await update.message.reply_text(
            "📖 **راهنمای استفاده:**\n\n"
            "1️⃣ روی دکمه 🛒 خرید کانفیگ کلیک کن.\n"
            "2️⃣ نوع سرویس رو انتخاب کن:\n"
            "   • 🌟 تک لوکیشن ویژه\n"
            "   • 🌍 مولتی لوکیشن (حجمی یا نامحدود)\n"
            "3️⃣ مشخصات رو انتخاب کن.\n"
            "4️⃣ قیمت نهایی بهت نمایش داده میشه.\n"
            "5️⃣ برای پرداخت، به ادمین پیام بده.\n\n"
            "✅ بعد از تایید پرداخت، کانفیگ برات ارسال میشه.",
            parse_mode="Markdown"
        )

    # ===== بازگشت به منوی اصلی =====
    elif text == "🔙 بازگشت":
        context.user_data.clear()
        reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
        await update.message.reply_text(
            "🔙 به منوی اصلی برگشتی.",
            reply_markup=reply_markup
        )

    # ===== پیام ناشناخته =====
    else:
        await update.message.reply_text(
            "❌ گزینه نامعتبر!\n"
            "لطفاً از دکمه‌ها استفاده کن یا /start رو بزن."
        )

# ========== وب سرور برای Render ==========
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "🤖 ربات TP VPN فعال است!"

@flask_app.route('/health')
def health():
    return "OK", 200

# ========== اجرای ربات ==========
def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("🤖 ربات TP VPN روشن شد!")
    app.run_polling(drop_pending_updates=True)

# ========== اجرای همزمان ==========
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)
