import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

print("🤖 BOT KEUANGAN TELEGRAM")
print("=" * 40)

TOKEN = os.environ.get('8191849660:AAE8OqUnXJ8NFt3lkwfhrSb_xY5OZr63kqM')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Halo! Saya bot pencatat keuangan.\n\n"
        "Kirim: 'makan 50000' atau 'gaji 5000000'"
    )

async def catat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"✅ Dicatat: {text}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("catat", catat))

print("Bot sedang berjalan...")
app.run_polling()
