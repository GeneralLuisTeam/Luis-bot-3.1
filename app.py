import os
from flask import Flask, request
from openai import OpenAI
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# OpenAI API Key-i Render-də təhlükəsiz şəkildə əlavə edəcəyik
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

LUIS_PROMPT = "Sən Luis-sən. Zarafatcıl, səmimi və bir az əsəbi asistansan. Dərslərdə kömək edirsən, tənbəlləri danlayırsan."

@app.route("/bot", methods=['POST'])
def bot():
    user_msg = request.values.get('Body', '')

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": LUIS_PROMPT},
            {"role": "user", "content": user_msg}
        ]
    )

    answer = completion.choices[0].message.content
    resp = MessagingResponse()
    resp.message(answer)
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
