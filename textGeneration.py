from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request
from openai import OpenAI


app = Flask(__name__, static_url_path='/static')
import os
API_KEY = os.getenv("api_key")

# Replace "your-api-key" with your actual OpenAI GPT API key
client = OpenAI(api_key=API_KEY)

def conduct_interview(message):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Act as an expert philosopher to solve the given problem smartly."},
            {"role": "user", "content": "{}".format(message)},
        ],
    )
    # Return the AI's response
    return completion.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])

def process_input():
    user_input = request.form['user_input']
    bot_response = conduct_interview(user_input)
    return render_template('index.html', user_input=user_input, bot_response=bot_response)

if __name__ == '__main__':
    app.run(debug=True)