import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

print("🤖 BOT KEUANGAN TELEGRAM")

# Token dari Render nanti
TOKEN = os.environ.get('TOKEN')

if not TOKEN:
    print("❌ ERROR: Token tidak ditemukan")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Halo! Kirim: makan 50000")

async def catat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"✅ Dicatat: {text}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("catat", catat))

print("✅ Bot berjalan...")
app.run_polling()
