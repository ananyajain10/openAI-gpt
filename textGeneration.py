from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request
from openai import OpenAI
from pathlib import Path


app = Flask(__name__, static_url_path='/static')
import os
API_KEY = os.getenv("api_key")

# Replace "your-api-key" with your actual OpenAI GPT API key
client = OpenAI(api_key=API_KEY)

def conduct_interview(message):
    try:

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Act as an expert philosopher friend to solve the given problem by understanding users tone smartly."},
                {"role": "user", "content": "{}".format(message)},
            ],
        )
        # Return the AI's response
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating speech: {str(e)}"

def text_to_speech(message):
    try:

        speech_file_path = Path(__file__).parent / "static"/ "speech.mp3"
        response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input= message
        )

        response.stream_to_file(speech_file_path)
    except Exception as e:
        return f"Error generating speech: {str(e)}"    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])

def process_input():
    user_input = request.form['user_input']
    bot_response = conduct_interview(user_input)
    audio = text_to_speech(bot_response)
    return render_template('index.html', user_input=user_input, bot_response=bot_response)

if __name__ == '__main__':
    app.run(debug=True)