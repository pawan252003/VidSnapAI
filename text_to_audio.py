from gtts import gTTS
import os

def text_to_speech_file(text, folder):
    output_path = os.path.join("user_uploads", folder, "audio.mp3")

    text = text.strip()
    
    if os.path.exists(output_path):
        return 

    tts = gTTS(text=text, lang="en")
    tts.save(output_path)