from flask import Flask, request
import telegram
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")  # Il token lo inserirai come variabile ambiente su Render
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

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

@app.route("/", methods=["GET"])
def index():
    return "Bot attivo!", 200

if __name__ == "__main__":
    app.run(debug=True)
