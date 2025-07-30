import sys

# Detecta se estamos em ambiente mobile (Android) ou desktop
IS_ANDROID = hasattr(sys, 'getandroidapilevel')

if IS_ANDROID:
    from plyer import tts

    def conigureVoice(*args, **kwargs):
        pass  # Plyer usa a voz padrão do Android, sem opções avançadas

    def falar(prompt: str) -> None:
        tts.speak(prompt)

else:
    import pyttsx3

    def conigureVoice(
        voiceId: int = 0, 
        voiceRate: int = 200, 
        voiceVolume: float = 1.0
    ) -> None:
        global engine
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[voiceId].id)
        engine.setProperty('rate', voiceRate)
        engine.setProperty('volume', voiceVolume)

    def falar(prompt: str) -> None:
        engine.say(prompt)
        engine.runAndWait()

# Teste
if __name__ == "__main__":
    if not IS_ANDROID:
        conigureVoice()
    falar("Olá, sou a Sylphiette!")
