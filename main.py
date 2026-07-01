import os
import threading
from flask import Flask
import telebot
# এখানে WebAppInfo ইম্পোর্ট করা হয়েছে টেলিগ্রামের ভেতরেই সাইট ওপেন করার জন্য
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# সার্ভার সচল রাখার জন্য Flask ওয়েব সার্ভার
app = Flask('')

@app.route('/')
def home():
    return "বট সফলভাবে লাইভ আছে!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# বটের মূল সেটিংস
BOT_TOKEN = '8876149112:AAEEGXBiFy9LK9m1liE8FMml8qUdkMbR6wI'  # ⚠️ এখানে তোমার আসল বটের টোকেনটি বসিয়ে দাও
CHANNEL_ID = '@Smart_Earning22'
BLOGGER_LINK = 'https://technologybd234.blogspot.com/2026/07/import-urlhttpsfonts.html?m=1'

bot = telebot.TeleBot(BOT_TOKEN)

def is_user_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        return False

def get_blogger_markup():
    markup = InlineKeyboardMarkup()
    # এখানে web_app ব্যবহার করা হয়েছে যেন পপআপ ছাড়া সরাসরি টেলিগ্রামের ভেতরেই সাইট ওপেন হয়
    btn_blog = InlineKeyboardButton("✨ Name Generator 🚀", web_app=WebAppInfo(url=BLOGGER_LINK))
    markup.add(btn_blog)
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    if is_user_joined(user_id):
        bot.send_message(
            message.chat.id, 
            "🎉 **স্বাগতম! আপনি আমাদের চ্যানেলে আছেন।**\n\n👇 আমাদের প্রিমিয়াম টুলসটি ব্যবহার করতে নিচের বাটনে ক্লিক করুন:",
            parse_mode="Markdown",
            reply_markup=get_blogger_markup()
        )
    else:
        markup = InlineKeyboardMarkup()
        channel_url = f"https://t.me/{CHANNEL_ID.replace('@', '')}"
        btn_join = InlineKeyboardButton("📢 চ্যানেলে জয়েন করুন", url=channel_url)
        btn_verify = InlineKeyboardButton("✅ Verify করুন", callback_data="check_verification")
        markup.add(btn_join)
        markup.add(btn_verify)
        bot.send_message(
            message.chat.id, 
            "⚠️ **দুঃখিত!** আমাদের ব্লগার পোস্টটি দেখতে হলে প্রথমে আপনাকে আমাদের টেলিগ্রাম চ্যানেলে জয়েন করতে হবে।\n\nনিচের বাটনে ক্লিক করে জয়েন করুন, তারপর 'Verify' বাটনে চাপ দিন।", 
            parse_mode="Markdown",
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data == "check_verification")
def verify_callback(call):
    user_id = call.from_user.id
    if is_user_joined(user_id):
        bot.answer_callback_query(call.id, "✅ ভেরিফিকেশন সফল হয়েছে!", show_alert=False)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🎉 **অভিনন্দন! আপনার ভেরিফিকেশন সফল হয়েছে।**\n\n👇 নিচের বাটনে ক্লিক করে সাইটে প্রবেশ করুন:",
            parse_mode="Markdown",
            reply_markup=get_blogger_markup()
        )
    else:
        bot.answer_callback_query(call.id, "❌ আপনি এখনো জয়েন করেননি! দয়া করে প্রথমে চ্যানেলে জয়েন করুন, তারপর ভেরিফাই বাটনে ক্লিক করুন।", show_alert=True)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    
    print("বট সফলভাবে চালু হয়েছে...")
    bot.infinity_polling()
