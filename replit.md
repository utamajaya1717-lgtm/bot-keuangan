# Bot Keuangan - Telegram Finance Tracker

## Overview
A Telegram bot for tracking personal finances (income and expenses). Users can record transactions by sending messages like "makan 50000" (food expense) or "gaji 5000000" (salary income).

## Project Structure
- `bot.py` - Main bot application using python-telegram-bot library
- `requirements.txt` - Python dependencies

## Features
- `/start` - Start the bot and see instructions
- `/saldo` - Check current balance
- `/riwayat` - View transaction history
- `/bantuan` - Help guide
- Natural text input for transactions (e.g., "makan 50000", "gaji 5jt")

## Environment Variables
- `TOKEN` - Telegram Bot API token (required)

## Running
The bot runs using polling mode. Execute with:
```
python bot.py
```

## Notes
- Transactions are stored in memory (not persistent)
- Indonesian language interface
- Supports amount formats: 50000, 1.5jt (million), 50k, 50rb (thousand)
