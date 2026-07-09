import json
import random
import string
import threading
import requests
import telebot
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# 1. إعدادات بوت التليجرام الخاصة بك
BOT_TOKEN = "8693064555:AAHiITywz89GxWblHg2oDiGSyLetX8sM1cI"
CHAT_ID = "1899767509"

bot = telebot.TeleBot(BOT_TOKEN)

# 2. توليد User-Agent عشوائي للحماية من الحظر
def generate_user_agent():
    chrome_version = f"{random.randint(110, 130)}.0.{random.randint(1000, 6000)}.{random.randint(10, 150)}"
    return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36"

# 3. دالة إرسال الإيميلات المستخرجة إلى حسابك
def Ahmed(email_address):
    print(f"[+] Extracted Email: {email_address}")
    try:
        bot.send_message(CHAT_ID, f"📩 تم استخراج إيميل جديد:\n`{email_address}`", parse_mode="Markdown")
    except Exception as e:
        print(f"[-] Telegram Send Error: {e}")

# 4. دالة سحب اليوزرات من إنستغرام
def get_username():
    while True:
        try:
            LsD = ''.join(random.choices(string.ascii_letters + string.digits, k=32))            
            bol = json.dumps({"id": str(random.randrange(10000, 53186034340)), "render_surface": "PROFILE"})         
            
            headers = {
                "X-FB-LSD": LsD, 
                'User-Agent': generate_user_agent(),
            }
            data = {
                "lsd": LsD, 
                "variables": bol, 
                "doc_id": "25618261841150840"
            }
            
            response = requests.post("https://instagram.com", headers=headers, data=data, timeout=10)
            username = response.json()['data']['user']['username']     
            
            email = username + "@gmail.com"    
            Ahmed(email)            
        except:
            pass

# 5. التفاعل مع أمر /start في البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 أهلاً بك! الأداة تعمل الآن على خوادم Railway وتقوم بالفحص والإرسال تلقائياً.")

# 6. دالة تشغيل فحص الإنستغرام في مسار منفصل
def start_extraction():
    threads = []
    for i in range(10): 
        t = threading.Thread(target=get_username)
        threads.append(t)
        t.start()

# 7. خادم ويب وهمي مخصص لمنصة Railway لمنع توقف الأداة
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is alive and running!")

def run_health_server():
    # Railway يوفر تلقائياً متغير PORT، وفي حال عدم وجوده نستخدم 8080 كافتراضي
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"[*] Health check server started on port {port}")
    server.serve_forever()

if name == "__main__":
    print("[*] Starting Telegram Bot & Instagram Tool for Railway...")
    
    # أ. تشغيل خادم الويب الخاص بـ Railway في Thread منفصل
    server_thread = threading.Thread(target=run_health_server)
    server_thread.daemon = True
    server_thread.start()
    
    # ب. تشغيل سحب اليوزرات في Thread منفصل
    extraction_thread = threading.Thread(target=start_extraction)
    extraction_thread.daemon = True
    extraction_thread.start()
    
    # ج. تشغيل البوت الأساسي ليبقى مستيقظاً ويستقبل أوامرك فوراً
    bot.infinity_polling()
