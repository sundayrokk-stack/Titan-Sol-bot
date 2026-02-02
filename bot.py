import os
import logging
import asyncio
import threading
from flask import Flask
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

load_dotenv()

# --- FLASK SERVER FOR RENDER ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running!", 200

def run_flask():
    # Render uses port 10000 by default
    port = int(os.getenv("PORT", 10000))
    # MUST use host='0.0.0.0' for Render to see the app
    app.run(host='0.0.0.0', port=port)

# --- BOT LOGIC ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "⚠️ *RISK WARNING*\n\n"
        "Trading digital assets involves significant risk\. Prices can be highly volatile\. "
        "Only invest what you can afford to lose\.\n\n"
        "*Introduction*\n"
        "Welcome to the most advanced Solana Trading Suite\. High speed, low latency\."
    )
    # Corrected argument: callback_data
    keyboard = [[InlineKeyboardButton("➡️ Continue", callback_data="intro")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)

async def handle_intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = (
        "🚀 *Welcome to Solana Trade Bot*\n\n"
        "✨ *Fast Swaps:* Instant execution on Raydium & Jupiter\.\n"
        "📈 *Limit Orders:* Set and forget your entries\.\n"
        "👥 *Copy Trading:* Follow whale wallets automatically\."
    )
    keyboard = [[InlineKeyboardButton("🚀 Start Trading", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    wallet_address = "`7xKX...v9PQ7L`"
    
    text = (
        "🏦 *Main Trading Menu*\n\n"
        f"💳 *Your Solana Wallet:*\n{wallet_address}\n\n"
        "Balance: *0\.00 SOL*\n"
        "Select an action below to begin\."
    )
    
    keyboard = [
        [InlineKeyboardButton("🟢 Buy", callback_data="buy"), InlineKeyboardButton("🔴 Sell", callback_data="sell")],
        [InlineKeyboardButton("⏳ Limit Orders", callback_data="limit"), InlineKeyboardButton("📊 DCA", callback_data="dca")],
        [InlineKeyboardButton("📦 Positions", callback_data="pos"), InlineKeyboardButton("👥 Copy Trade", callback_data="copy")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings"), InlineKeyboardButton("🔗 Referrals", callback_data="ref")],
        [InlineKeyboardButton("📤 Withdraw", callback_data="withdraw"), InlineKeyboardButton("🔄 Refresh", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        logging.error("No BOT_TOKEN found!")
        return

    # Start Flask background thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Build Application
    application = Application.builder().token(token).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_intro, pattern="^intro$"))
    application.add_handler(CallbackQueryHandler(main_menu, pattern="^main_menu$"))

    # Start Polling
    application.run_polling()

if __name__ == '__main__':
    main()
