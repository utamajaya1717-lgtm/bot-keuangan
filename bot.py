import os
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print("=" * 50)
print("💰 BOT PENCATAT KEUANGAN")
print("=" * 50)

# Token dari Render
TOKEN = os.environ.get('TOKEN')

if not TOKEN:
    print("❌ ERROR: Token tidak ditemukan")
    exit(1)

print("✅ Bot siap menerima pesan...")

# Simpan transaksi (sementara di memory)
transaksi = []

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
        pengeluaran_keywords = ['makan', 'transport', 'belanja', 'pulsa', 'listrik', 'internet']
        
        if any(k in kategori for k in pemasukan_keywords):
            jenis = "💰 PEMASUKAN"
            emoji = "📥"
        elif any(k in kategori for k in pengeluaran_keywords):
            jenis = "💸 PENGELUARAN"
            emoji = "📤"
        else:
            jenis = "💸 PENGELUARAN"  # default
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
        
        # Format jumlah dengan titik
        jumlah_format = f"{jumlah:,.0f}".replace(",", ".")
        
        # Simpan transaksi
        transaksi.append({
            'waktu': waktu,
            'jenis': jenis,
            'kategori': kategori.title(),
            'jumlah': jumlah,
            'user': user.first_name
        })
        
        # Kirim konfirmasi
        await update.message.reply_text(
            f"{emoji} **TRANSAKSI DICATAT**\n\n"
            f"🕒 {waktu.strftime('%d/%m/%Y %H:%M')}\n"
            f"📊 {jenis}\n"
            f"🏷️ {kategori.title()}\n"
            f"💵 Rp {jumlah_format}\n\n"
            f"📈 Total transaksi: {len(transaksi)}"
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def cek_saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /saldo"""
    if not transaksi:
        await update.message.reply_text("📭 Belum ada transaksi")
        return
    
    total_pemasukan = sum(t['jumlah'] for t in transaksi if 'PEMASUKAN' in t['jenis'])
    total_pengeluaran = sum(t['jumlah'] for t in transaksi if 'PENGELUARAN' in t['jenis'])
    saldo = total_pemasukan - total_pengeluaran
    
    await update.message.reply_text(
        f"💰 **LAPORAN KEUANGAN**\n\n"
        f"📥 Total Pemasukan: Rp {total_pemasukan:,.0f}\n"
        f"📤 Total Pengeluaran: Rp {total_pengeluaran:,.0f}\n"
        f"💎 Saldo Saat Ini: Rp {saldo:,.0f}\n\n"
        f"📊 Total Transaksi: {len(transaksi)}\n"
        f"📅 Periode: {transaksi[0]['waktu'].strftime('%d/%m')} - {transaksi[-1]['waktu'].strftime('%d/%m')}"
    )

async def riwayat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /riwayat"""
    if not transaksi:
        await update.message.reply_text("📭 Belum ada transaksi")
        return
    
    # Ambil 5 transaksi terakhir
    riwayat_text = "📜 **RIWAYAT TRANSAKSI**\n\n"
    
    for i, t in enumerate(reversed(transaksi[-5:]), 1):
        jumlah_format = f"{t['jumlah']:,.0f}".replace(",", ".")
        riwayat_text += (
            f"{i}. {t['waktu'].strftime('%d/%m %H:%M')}\n"
            f"   {t['jenis']} - {t['kategori']}\n"
            f"   Rp {jumlah_format}\n\n"
        )
    
    riwayat_text += f"📊 Total: {len(transaksi)} transaksi"
    
    await update.message.reply_text(riwayat_text)

async def bantuan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /bantuan"""
    await update.message.reply_text(
        "🆘 **BANTUAN**\n\n"
        "📝 **Cara Mencatat:**\n"
        "Kirim: <kategori> <jumlah>\n\n"
        "💰 **Contoh:**\n"
        "• makan 50000\n"
        "• gaji 5000000\n"
        "• transport 25000\n"
        "• belanja 150000\n\n"
        "📊 **Format Jumlah:**\n"
        "• 50000 → Rp 50.000\n"
        "• 1.5jt → Rp 1.500.000\n"
        "• 50k → Rp 50.000\n\n"
        "📋 **Perintah:**\n"
        "/start - Mulai bot\n"
        "/saldo - Cek saldo\n"
        "/riwayat - Lihat riwayat\n"
        "/bantuan - Panduan ini"
    )

# Buat aplikasi bot
app = Application.builder().token(TOKEN).build()

# Tambah handler
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("saldo", cek_saldo))
app.add_handler(CommandHandler("riwayat", riwayat))
app.add_handler(CommandHandler("bantuan", bantuan))
app.add_handler(CommandHandler("help", bantuan))

# Handler untuk pesan teks biasa
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, catat_otomatis))

print("✅ Bot siap! Menunggu pesan...")
print("=" * 50)

# Jalankan bot
app.run_polling()
