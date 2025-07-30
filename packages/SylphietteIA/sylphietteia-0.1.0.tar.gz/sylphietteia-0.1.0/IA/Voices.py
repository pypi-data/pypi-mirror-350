import pyttsx3

def falar(prompt : str) -> None:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 240)
    engine.setProperty('volume', 1.0)
    engine.say(prompt)
    engine.runAndWait()
    if __name__ == "__main__":
        for i, voz in enumerate(voices):
            print(f"{i}: {voz.name} - {voz.id}")
            
if __name__ == "__main__":
    falar("Audio funcionando")