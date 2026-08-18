from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def text_to_speech_file(text, folder):
    audio = elevenlabs.text_to_speech.convert(
       voice_id="pNInz6obpgDQGcFmaJgB", # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5", # use the turbo model for low latency
        # Optional voice settings that allow you to customize the output
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )

#play(audio)

    save_file_path = os.path.join(f"user_uploads/{folder}", "audio.mp3")

    with open(save_file_path,"wb") as f:
        for chunk in audio:
            if chunk:
                f.write(chunk)


    return save_file_path
