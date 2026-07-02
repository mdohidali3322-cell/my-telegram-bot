import os
import threading
from flask import Flask, request, jsonify
import telebot

app = Flask('')

# ⚠️ সেটিংস (তোমার তথ্যগুলো এখানে বসাও)
BOT_TOKEN = '8876149112:AAEEGXBiFy9LK9m1liE8FMml8qUdkMbR6wI'  # 👈 এখানে তোমার আসল বটের API টোকেন দাও
CHANNEL_ID = '@Smart_Earning22'

bot = telebot.TeleBot(BOT_TOKEN)

# ওয়েবসাইটের সাথে কানেক্ট করার জন্য CORS পলিসি হ্যান্ডেল করা হয়েছে এখানে
@app.route('/')
def home():
    return "API Server is running successfully!", 200, {'Access-Control-Allow-Origin': '*'}

# ভেরিফিকেশন চেক করার মূল পথ (Endpoint)
@app.route('/check-verify')
def check_verify():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "User ID missing"}), 200, {'Access-Control-Allow-Origin': '*'}
    
    try:
        # টেলিগ্রাম চ্যানেলের মেম্বার কি না তা চেক করা হচ্ছে
        member = bot.get_chat_member(CHANNEL_ID, int(user_id))
        if member.status in ['member', 'administrator', 'creator']:
            return jsonify({"status": "verified"}), 200, {'Access-Control-Allow-Origin': '*'}
        else:
            return jsonify({"status": "not_joined"}), 200, {'Access-Control-Allow-Origin': '*'}
    except Exception as e:
        return jsonify({"status": "error", "message": "Invalid User ID or Bot Error"}), 200, {'Access-Control-Allow-Origin': '*'}

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    
    print("API Server & Telegram Bot started...")
    bot.infinity_polling()
