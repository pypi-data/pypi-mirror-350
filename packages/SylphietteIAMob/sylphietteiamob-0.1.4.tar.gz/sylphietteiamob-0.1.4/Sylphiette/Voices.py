from plyer import tts

def conigureVoice(*args, **kwargs):
    # O Android usa a voz padrão do sistema. Não há opções personalizáveis com plyer.
    pass

def falar(prompt: str) -> None:
    tts.speak(prompt)

# Teste
if __name__ == "__main__":
    conigureVoice()
    falar("Olá, sou a Sylphiette!")
