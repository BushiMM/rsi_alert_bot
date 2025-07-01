from flask import Flask, request
import telegram
import os

# Variabili ambiente
TOKEN = os.getenv("TELEGRAM_TOKEN")  # Inserito su Render
URL = os.getenv("RENDER_EXTERNAL_URL")  # Inserito su Render

# Inizializza il bot
bot = telegram.Bot(token=TOKEN)

# Crea app Flask
app = Flask(__name__)

# Endpoint per ricevere gli aggiornamenti da Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message = update.message.text

    if message == "/start":
        bot.send_message(chat_id=chat_id, text="Bot attivo con Webhook!")
    else:
        bot.send_message(chat_id=chat_id, text=f"Hai scritto: {message}")

    return "OK", 200

# Endpoint di test
@app.route("/", methods=["GET"])
def index():
    return "Bot attivo!", 200

# Imposta il webhook all'avvio dell'app
if __name__ == "__main__":
    if URL:
        webhook_url = f"{URL}/{TOKEN}"
        bot.set_webhook(url=webhook_url)
    else:
        print("⚠️ Manca la variabile RENDER_EXTERNAL_URL")
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
