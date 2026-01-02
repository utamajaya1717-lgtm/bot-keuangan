import os
import datetime
import json
import base64
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print("=" * 50)
print("💰 BOT PENCATAT KEUANGAN + GOOGLE SHEETS")
print("=" * 50)

# Load environment variables
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') or os.environ.get('TOKEN')
SHEET_ID = os.environ.get('GOOGLE_SHEET_ID')
CREDS_BASE64 = os.environ.get('GOOGLE_CREDENTIALS_BASE64')

if not TOKEN:
    print("❌ ERROR: Token tidak ditemukan")
    exit(1)

# Setup Google Sheets
sheet = None
if SHEET_ID and CREDS_BASE64:
    try:
        creds_json = json.loads(base64.b64decode(CREDS_BASE64).decode('utf-8'))
        creds = Credentials.from_service_account_info(
            creds_json, 
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).get_worksheet(0)
        print("✅ Terhubung ke Google Sheets")
    except Exception as e:
        print(f"⚠️ Gagal terhubung ke Google Sheets: {e}")

print("✅ Bot siap menerima pesan...")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /start"""
    await update.message.reply_text(
        "👋 Halo! Saya bot pencatat keuangan.\n\n"
        "💰 **CARA PAKAI:**\n"
        "• `makan 50000` - Catat pengeluaran makan Rp 50.000\n"
        "• `gaji 5000000` - Catat pemasukan gaji Rp 5.000.000\n"
        "• `/saldo` - Lihat saldo saat ini\n"
        "• `/riwayat` - Lihat riwayat transaksi\n\n"
        "Contoh lain:\n"
        "• transport 25000\n"
        "• belanja 150000\n"
        "• bonus 1000000"
    )

async def catat_otomatis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk catat transaksi otomatis"""
    try:
        pesan = update.message.text.lower()
        user = update.message.from_user
        waktu = datetime.datetime.now()
        
        # Pisahkan kata-kata
        kata = pesan.split()
        
        if len(kata) < 2:
            await update.message.reply_text("Format: <kategori> <jumlah>\nContoh: makan 50000")
            return
        
        kategori = kata[0]
        jumlah_text = kata[1]
        
        # Deteksi jenis transaksi
        pemasukan_keywords = ['gaji', 'bonus', 'jual', 'penjualan', 'investasi']
        
        if any(k in kategori for k in pemasukan_keywords):
            jenis = "💰 PEMASUKAN"
            emoji = "📥"
        else:
            jenis = "💸 PENGELUARAN"
            emoji = "📤"
        
        # Konversi jumlah
        try:
            if 'jt' in jumlah_text:
                jumlah = float(jumlah_text.replace('jt', '')) * 1000000
            elif 'k' in jumlah_text:
                jumlah = float(jumlah_text.replace('k', '')) * 1000
            elif 'rb' in jumlah_text:
                jumlah = float(jumlah_text.replace('rb', '')) * 1000
            else:
                jumlah = float(jumlah_text.replace(',', '.'))
        except:
            await update.message.reply_text("Format jumlah salah!\nContoh: 50000, 1.5jt, 50k")
            return
        
        # Simpan ke Google Sheets jika tersedia
        status_sheet = ""
        if sheet:
            try:
                sheet.append_row([
                    waktu.strftime('%d/%m/%Y %H:%M'),
                    user.first_name,
                    jenis,
                    kategori.title(),
                    jumlah
                ])
                status_sheet = "\n✅ Tersimpan di Google Sheets"
            except Exception as e:
                status_sheet = f"\n⚠️ Gagal simpan ke Sheets: {e}"

        # Format jumlah dengan titik
        jumlah_format = f"{jumlah:,.0f}".replace(",", ".")
        
        # Kirim konfirmasi
        await update.message.reply_text(
            f"{emoji} **TRANSAKSI DICATAT**\n\n"
            f"🕒 {waktu.strftime('%d/%m/%Y %H:%M')}\n"
            f"📊 {jenis}\n"
            f"🏷️ {kategori.title()}\n"
            f"💵 Rp {jumlah_format}{status_sheet}"
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def bantuan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /bantuan"""
    await update.message.reply_text(
        "🆘 **BANTUAN**\n\n"
        "📝 **Cara Mencatat:**\n"
        "Kirim: <kategori> <jumlah>\n\n"
        "💰 **Contoh:**\n"
        "• makan 50000\n"
        "• gaji 5000000\n\n"
        "📋 **Perintah:**\n"
        "/start - Mulai bot\n"
        "/bantuan - Panduan ini"
    )

# Buat aplikasi bot
app = Application.builder().token(TOKEN).build()

# Tambah handler
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("bantuan", bantuan))
app.add_handler(CommandHandler("help", bantuan))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, catat_otomatis))

print("✅ Bot siap! Menunggu pesan...")
print("=" * 50)

# Jalankan bot
app.run_polling()
