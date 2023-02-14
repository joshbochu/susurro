import os
import requests    # ← new import
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from random import randint
import whisper
from tempfile import NamedTemporaryFile

load_dotenv()

# Load the Whisper model:
model = whisper.load_model('base')

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
        # remove the whatsapp: prefix from the number
        username = sender.split(':')[1]
        id = randint(0, 999999999)
        print(id)

        audio_bytes = r.content
        audio_id = f'{username}-{id}'

        if content_type.startswith('audio/'):
            audio_bytes = r.content
            audio_id = f'{username}-{id}'
            audio_file = f'{audio_id}.ogg'
            audio_path = os.path.join(os.getcwd(), audio_file)

            with open(audio_path, 'wb') as f:
                f.write(audio_bytes)

            try:
                transcript = model.transcribe(audio_path, fp16=False)
                os.remove(audio_path)
                return respond(transcript.text)
            except Exception as e:
                print(e)
                os.remove(audio_path)
                return respond('There was an error processing your request.')

    #     else:
    #         return respond('The file that you submitted is not a supported audio type.')

    #    with NamedTemporaryFile(delete=False) as temp_audio_file:
    #         temp_audio_file.write(audio_bytes)
    #         audio_path = temp_audio_file.name
    #     try:
    #         print(audio_path)
    #         transcript = model.transcribe(audio_path, fp16=False)
    #         return respond(transcript)
    #     except Exception as e:
    #         print(e)
    #         return respond('There was an error processing your request.')

        # save block
        # if content_type == 'audio/ogg':
        #     filename = f'uploads/{username}/{id}.ogg'
        # if filename:
        #     if not os.path.exists(f'uploads/{username}'):
        #         os.mkdir(f'uploads/{username}')
        #     with open(filename, 'wb') as f:
        #         content_bytes = r.content
        #         f.write(r.content)
        #     return respond('Thank you! Your voice note was received.')
        # else:
        #     return respond('The file that you submitted is not a supported audio type.')
    else:
        return respond('Please send a voice note!')
