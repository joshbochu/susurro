import os
import requests    # ← new import
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from random import randint

load_dotenv()

app = Flask(__name__)

def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/message', methods=['POST'])
def reply():
    sender = request.form.get('From')
    message = request.form.get('Body')
    media_url = request.form.get('MediaUrl0')
    print(f'{sender} sent {message}')
    if media_url:
        r = requests.get(media_url)
        content_type = r.headers['Content-Type']
        username = sender.split(':')[1]  # remove the whatsapp: prefix from the number
        id = randint(0,999999999)
        print(id)
        if content_type == 'audio/ogg':
            filename = f'uploads/{username}/{id}.ogg'
        if filename:
            if not os.path.exists(f'uploads/{username}'):
                os.mkdir(f'uploads/{username}')
            with open(filename, 'wb') as f:
                f.write(r.content)
            return respond('Thank you! Your voice note was received.')
        else:
            return respond('The file that you submitted is not a supported audio type.')
    else:
        return respond('Please send a voice note!')
