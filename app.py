from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from elevenlabs import ElevenLabs, Voice, save
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
openai_api = os.getenv("OPENAI_API_KEY")
elevenlabs_api = os.getenv("ELEVENLABS_API_KEY")

# Initialize Flask, OpenAI client, and ElevenLabs client
app = Flask(__name__)
openai_client = OpenAI(api_key=openai_api)
eleven_client = ElevenLabs(api_key=elevenlabs_api)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.json['message']
    prompt = f"Recommend some books based on this preference: {user_input}"

    # OpenAI call for recommendations
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    recommendation = response.choices[0].message.content

    # Convert recommendation to speech using ElevenLabs
    audio = eleven_client.text_to_speech(
        text=recommendation,
        voice=Voice(name="Bella")
    )
    save(audio, "static/recommendation.mp3")

    return jsonify({'recommendation': recommendation})

if __name__ == '__main__':
    app.run(debug=True)
