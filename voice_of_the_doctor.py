# Load environment variables (if you're not using pipenv, uncomment the following)
from dotenv import load_dotenv
load_dotenv()

import os
import subprocess
import platform
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

# Retrieve your ElevenLabs API key from the environment
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def play_audio_file(mp3_filepath):
    """
    Converts the given MP3 file to WAV and plays it using a system command.
    This is necessary because Media.SoundPlayer on Windows only supports WAV files.
    """
    # Create a WAV filename by replacing the extension
    wav_filepath = mp3_filepath.replace(".mp3", ".wav")
    
    try:
        # Convert MP3 to WAV using pydub
        audio = AudioSegment.from_mp3(mp3_filepath)
        audio.export(wav_filepath, format="wav")
    except Exception as e:
        print(f"Error converting MP3 to WAV: {e}")
        return

    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', wav_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', wav_filepath])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

def text_to_speech_with_gtts(input_text, output_filepath):
    """
    Uses gTTS to convert text to speech, saves the result as an MP3,
    and then plays it by converting it to a WAV file.
    """
    language = "en"
    try:
        tts = gTTS(text=input_text, lang=language, slow=False)
        tts.save(output_filepath)
        print(f"gTTS saved audio to {output_filepath}")
    except Exception as e:
        print(f"Error generating speech with gTTS: {e}")
        return
    
    # Play the audio by converting the MP3 to WAV
    play_audio_file(output_filepath)

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """
    Uses ElevenLabs to generate speech from text, saves the MP3 output,
    and then plays it by converting it to a WAV file.
    """
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.generate(
            text=input_text,
            voice="Rachel",  # Change voice if needed
            output_format="mp3_22050_32",
            model="eleven_turbo_v2"
        )
        elevenlabs.save(audio, output_filepath)
        print(f"ElevenLabs saved audio to {output_filepath}")
    except Exception as e:
        print(f"Error generating speech with ElevenLabs: {e}")
        return
    
    # Play the audio by converting the MP3 to WAV
    play_audio_file(output_filepath)

if __name__ == "__main__":
    # Test gTTS implementation
    input_text_gtts = "Hi, this is Mohit Kasat, autoplay testing with gTTS!"
    text_to_speech_with_gtts(input_text=input_text_gtts, output_filepath="gtts_testing_autoplay.mp3")
    
    # Test ElevenLabs implementation
    input_text_eleven = "Hi, this is Mohit Kasat, autoplay testing with ElevenLabs!"
    text_to_speech_with_elevenlabs(input_text=input_text_eleven, output_filepath="elevenlabs_testing_autoplay.mp3")
