import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from huggingface_hub import InferenceClient

app = Flask(__name__)

# --- The GeneralLuis Team: Yaddaş Sistemi ---
# Hər istifadəçinin söhbət tarixçəsini yadda saxlayır
user_history = {}

# --- Hugging Face AI Beyni ---
# Diqqət: HF_TOKEN-i 'Environment Variables' hissəsindən götürürük (Təhlükəsizlik üçün)
HF_TOKEN = os.environ.get("HF_TOKEN")
client = InferenceClient(model="google/flan-t5-large", token=HF_TOKEN)

@app.route("/", methods=['GET'])
def home():
    return "Luis 3.2 (Memory Version) is Online! 🚀 | The GeneralLuis Team"

@app.route("/webhook", methods=['POST'])
def webhook():
    # Gələn mesajı və göndərən nömrəni müəyyən edirik
    user_id = request.values.get('From', '')
    incoming_msg = request.values.get('Body', '').lower()
    
    # Yeni istifadəçi üçün tarixçə yarat
    if user_id not in user_history:
        user_history[user_id] = []
    
    # İstifadəçinin mesajını yaddaşa əlavə et
    user_history[user_id].append(f"User: {incoming_msg}")
    
    # AI-nın konteksti anlaması üçün son 4 mesajı birləşdiririk
    context = "\n".join(user_history[user_id][-4:])
    
    resp = MessagingResponse()
    msg = resp.message()

    try:
        # AI Cavab Generatoru
        ai_response = client.text_generation(
            context, 
            max_new_tokens=150,
            temperature=0.7 # Cavabların daha təbii olması üçün
        )
        
        # AI-nın cavabını yaddaşa əlavə edirik (Növbəti suallar üçün)
        user_history[user_id].append(f"Luis: {ai_response}")
        
        msg.body(ai_response)
    except Exception as e:
        print(f"Error: {e}")
        msg.body("Texniki bir xəta baş verdi, amma GeneralLuis bunu həll edəcək! 🛠️")

    return str(resp)

if __name__ == "__main__":
    # Hugging Face Spaces üçün port ayarı
    app.run(host='0.0.0.0', port=7860)
