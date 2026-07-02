import os
import threading
from flask import Flask, request, jsonify
import telebot
from telebot import types

app = Flask('')

# ⚠️ '  

CHANNEL_ID = '' 
BLOGGER_URL = 'https://technologybd234.blogspot.com/2026/07/import-urlhttpsfonts.html?m=1'

bot = telebot.TeleBot(BOT_TOKEN)

@app.route('/')
def home():
    return "API Server is running successfully!", 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/check-verify')
def check_verify():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "User ID missing"}), 200, {'Access-Control-Allow-Origin': '*'}
    
    try:
        member = bot.get_chat_member(CHANNEL_ID, int(user_id))
        if member.status in ['member', 'administrator', 'creator']:
            return jsonify({"status": "verified"}), 200, {'Access-Control-Allow-Origin': '*'}
        else:
            return jsonify({"status": "not_joined"}), 200, {'Access-Control-Allow-Origin': '*'}
    except Exception as e:
        return jsonify({"status": "error", "message": "Bot Error"}), 200, {'Access-Control-Allow-Origin': '*'}

# 🚀 এই কমান্ডটি ইউজারকে আইডি সহ সরাসরি ক্রোম ব্রাউজারে পাঠাবে
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # ইউজার আইডিটি লিংকের সাথে নিখুঁতভাবে জুড়ে দেওয়ার লজিক
    if "?" in BLOGGER_URL:
        chrome_link = f"{BLOGGER_URL}&user_id={user_id}"
    else:
        chrome_link = f"{BLOGGER_URL}?user_id={user_id}"
    
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="✨ Name Generator 🚀", url=chrome_link)
    markup.add(btn)
    
    bot.send_message(
        message.chat.id, 
        "👋 আমাদের প্রিমিয়াম নাম জেনারেটর টুলসটি ব্যবহার করতে নিচের বাটনে ক্লিক করুন (এটি সরাসরি ক্রোম ব্রাউজারে ওপেন হবে):", 
        reply_markup=markup
    )

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    bot.infinity_polling()
