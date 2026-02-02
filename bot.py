import os
import logging
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

# --- FLASK SERVER ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "Active", 200

def run_flask():
    port = int(os.getenv("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- BOT LOGIC ---
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "⚠️ *RISK WARNING*\n\n"
        "Trading digital assets involves significant risk\. Prices can be highly volatile\. "
        "Only invest what you can afford to lose\.\n\n"
        "🙋‍♂️ *Support:* Only contact @ads2defi\n\n"
        "*Introduction*\n"
        "Welcome to the most advanced Solana Trading Suite\. High speed, low latency\."
    )
    keyboard = [[InlineKeyboardButton("➡️ Continue", callback_data="intro")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send message and pin it
    msg = await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
    try:
        await context.bot.pin_chat_message(chat_id=update.effective_chat.id, message_id=msg.message_id)
    except Exception as e:
        logging.warning(f"Could not pin message: {e}")

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
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN_V2)

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    wallet = "`7xKX...v9PQ7L`"
    text = (
        "🏦 *Main Trading Menu*\n\n"
        f"💳 *Your Solana Wallet:*\n{wallet}\n\n"
        "Balance: *0\.00 SOL*\n"
        "Select an action below to begin\."
    )
    
    keyboard = [
        [InlineKeyboardButton("🟢 Buy", callback_data="buy"), InlineKeyboardButton("🔴 Sell", callback_data="sell")],
        [InlineKeyboardButton("⏳ Limit Orders", callback_data="limit"), InlineKeyboardButton("📊 DCA", callback_data="dca")],
        [InlineKeyboardButton("🎯 Sniper", callback_data="sniper"), InlineKeyboardButton("🌊 Trenches", callback_data="trenches")],
        [InlineKeyboardButton("📦 Positions", callback_data="pos"), InlineKeyboardButton("👥 Copy Trade", callback_data="copy")],
        [InlineKeyboardButton("🎁 Rewards", callback_data="rewards"), InlineKeyboardButton("👀 Watchlist", callback_data="watchlist")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings"), InlineKeyboardButton("🔗 Referrals", callback_data="ref")],
        [InlineKeyboardButton("📤 Withdraw", callback_data="withdraw"), InlineKeyboardButton("🔄 Refresh", callback_data="main_menu")],
        [InlineKeyboardButton("❓ Help", callback_data="help")]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN_V2)

# Generic handler for functioning buttons
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer(text=f"Opening {data.capitalize()}...", show_alert=False)
    
    # You can add specific logic for each button here later
    if data == "help":
        await query.message.reply_text("📚 *Help Center*\nNeed assistance? Contact @ads2defi", parse_mode=ParseMode.MARKDOWN_V2)

def main():
    token = os.getenv("BOT_TOKEN")
    threading.Thread(target=run_flask, daemon=True).start()
    
    app_bot = Application.builder().token(token).build()
    
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CallbackQueryHandler(handle_intro, pattern="^intro$"))
    app_bot.add_handler(CallbackQueryHandler(main_menu, pattern="^main_menu$"))
    # Catches all other button clicks to ensure they "work"
    app_bot.add_handler(CallbackQueryHandler(button_callback))

    app_bot.run_polling()

if __name__ == '__main__':
    main()
