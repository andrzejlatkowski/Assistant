import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")

        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio_data)

        return text.lower()
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you said"
    except sr.RequestError as e:
        return "Error: {}".format(e)


# testing
# recognized_text = recognize_speech()
# print("You said:", recognized_text)
