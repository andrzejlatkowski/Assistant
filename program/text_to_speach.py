from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import threading


def speak_text(text):
    language = 'en'

    tts = gTTS(text=text, lang=language, slow=False)

    # Create an in-memory file
    speech_file = BytesIO()

    # Write the speech data to the in-memory file
    tts.write_to_fp(speech_file)

    # Reset the file pointer to the beginning of the file
    speech_file.seek(0)

    # Load the speech from the in-memory file using pydub
    speech = AudioSegment.from_file(speech_file)

    # Play the audio
    play(speech)


def play_audio(text):
    play_thread = threading.Thread(target=speak_text, args=(text,))
    play_thread.start()
    play_thread.join()
