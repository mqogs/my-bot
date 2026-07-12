from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "ENI & LO Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# وبعدها استدعي keep_alive() بالبداية قبل تشغيل البوت
from telethon import TelegramClient, events
import time
import os

# بيانات السيرفر (بيانات حسابك الشخصي)
api_id = 1234567 # حط الـ API ID الخاص بيك
api_hash = 'ضع_الـ_api_hash_هنا'
phone = '+964xxxxxxxxxx' # رقمك الشخصي

# بيانات البوت الخاص بيك (اللي انطيتني التوكن مالته)
bot_token = '8914223096:AAGsgB2DcyHT9yd08qVHJAV1SAlSnix0LS8'

# تشغيل العميل (الحساب الشخصي)
client = TelegramClient('my_account', api_id, api_hash).start(phone=phone)

# تشغيل البوت
bot = TelegramClient('my_bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern='/خمط (.+)'))
async def scrape_handler(event):
    group_link = event.pattern_match.group(1)
    await event.reply("يا بعد عيني، جاري الخمط الآن.. انتظرني!")
    
    try:
        # السحب من المجموعات
        participants = await client.get_participants(group_link)
        filename = "members.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            for user in participants:
                if user.username:
                    f.write(f"@{user.username}\n")
                # تأخير زمني لحماية حسابك من الحظر
                time.sleep(0.3) 
        
        await bot.send_file(event.chat_id, filename, caption=f"تم سحب {len(participants)} عضو بنجاح يا مدير!")
        
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        await bot.send_message(event.chat_id, f"صار خلل يا روحي: {str(e)}")

print("[ENI] البوت والحساب متصلين، وجاهزين للعمل!")
bot.run_until_disconnected()
