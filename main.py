from fastapi import FastAPI, Query
import yt_dlp
import whisper
from googletrans import Translator
from gtts import gTTS
import os

app = FastAPI()
translator = Translator()

@app.get("/")
def home():
    return {"message": "DubFlow AI Backend is Running!"}

@app.get("/dub")
async def generate_dub(video_url: str = Query(..., description="YouTube Video URL")):
    try:
        audio_file = "original_audio.mp3"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'original_audio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        model = whisper.load_model("base")
        result = model.transcribe(audio_file)
        english_text = result['text']

        translated = translator.translate(english_text, dest='ur')
        urdu_text = translated.text

        tts = gTTS(text=urdu_text, lang='ur')
        output_audio = "urdu_dubbed.mp3"
        tts.save(output_audio)

        return {
            "status": "success",
            "original_text": english_text,
            "translated_text": urdu_text,
            "audio_url": "Backend_URL/urdu_dubbed.mp3"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
      
