from flask import Flask, request, jsonify
import requests
from twilio.twiml.messaging_response import MessagingResponse
import os
from twilio.rest import Client


account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

app = Flask(__name__)



@app.route('/')
def home():
    print('hot')
    print(account_sid, auth_token)
    src='https://api.twilio.com/2010-04-01/accounts/aca066a52abc10a525037cbfc138cec0a1/messages/mmc1578e79f26daae9e1945a780f484bb8/media/me1f548e3ed3cd6359f8d6b9dd485100eb'
    audio = requests.get(src, auth=(account_sid, auth_token))
    print(audio)
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'


@app.route('/transcribe', methods=['POST'])
def transcribe():
    audio_src = request.values.get('MediaUrl0', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    return str(msg)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        audio_src = request.values.get('MediaUrl0', '').lower()
        src='https://api.twilio.com/2010-04-01/accounts/aca066a52abc10a525037cbfc138cec0a1/messages/mmc1578e79f26daae9e1945a780f484bb8/media/me1f548e3ed3cd6359f8d6b9dd485100eb'
        audio = requests.get(audio_src, auth=(account_sid, auth_token))
        print(audio_src)
        print(audio)
        msg.body('I only know about famous quotes and cats, sorry!')
    return str(resp)


if __name__ == '__main__':
    app.run(port=4000)
