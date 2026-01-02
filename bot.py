import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

print("🤖 TELEGRAM FINANCE BOT")
print("=" * 40)

# Token dari environment variable (akan diisi di Render)
TOKEN = os.environ.get('8191849660:AAE8OqUnXJ8NFt3lkwfhrSb_xY5OZr63kqM')

if not TOKEN:
    print("❌ ERROR: TOKEN tidak ditemukan!")
    print("💡 Tambah TOKEN di Render dashboard → Environment")
    exit(1)

print(f"✅ Token loaded: {8191849660:AAE8OqUnXJ8NFt3lkwfhrSb_xY5OZr63kqM[:10]}...")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Halo! Saya bot pencatat keuangan.\n\n"
        "Kirim: 'makan 50000' atau 'gaji 5000000'\n\n"
        "Bot siap digunakan!"
    )

async def catat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"✅ Dicatat: {text}")

# Buat aplikasi bot
app = Application.builder().token(TOKEN).build()

# Tambah handler
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("catat", catat))

print("✅ Bot application created")
print("📡 Starting polling...")
print("=" * 40)

# Jalankan bot
app.run_polling()
