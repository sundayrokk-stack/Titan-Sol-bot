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
    port = int(os.getenv("PORT", 8080))
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
    keyboard = [[InlineKeyboardButton("➡️ Continue", callback_query_data="intro")]]
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
    keyboard = [[InlineKeyboardButton("🚀 Start Trading", callback_query_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Placeholder Wallet
    wallet_address = "`7xKX...v9PQ7L`"
    
    text = (
        "🏦 *Main Trading Menu*\n\n"
        f"💳 *Your Solana Wallet:*\n{wallet_address}\n\n"
        "Balance: *0\.00 SOL*\n"
        "Select an action below to begin\."
    )
    
    keyboard = [
        [InlineKeyboardButton("🟢 Buy", callback_query_data="buy"), InlineKeyboardButton("🔴 Sell", callback_query_data="sell")],
        [InlineKeyboardButton("⏳ Limit Orders", callback_query_data="limit"), InlineKeyboardButton("📊 DCA", callback_query_data="dca")],
        [InlineKeyboardButton("📦 Positions", callback_query_data="pos"), InlineKeyboardButton("👥 Copy Trade", callback_query_data="copy")],
        [InlineKeyboardButton("⚙️ Settings", callback_query_data="settings"), InlineKeyboardButton("🔗 Referrals", callback_query_data="ref")],
        [InlineKeyboardButton("📤 Withdraw", callback_query_data="withdraw"), InlineKeyboardButton("🔄 Refresh", callback_query_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Error: BOT_TOKEN not found in environment.")
        return

    # Start Flask in a background thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Build the Telegram Application
    application = Application.builder().token(token).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_intro, pattern="^intro$"))
    application.add_handler(CallbackQueryHandler(main_menu, pattern="^main_menu$"))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
