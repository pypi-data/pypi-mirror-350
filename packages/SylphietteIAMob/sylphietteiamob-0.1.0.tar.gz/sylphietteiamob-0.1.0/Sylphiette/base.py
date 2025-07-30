from Sylphiette import Gemini
from Sylphiette import Voices
from Sylphiette import Acessos
from Sylphiette import Terminal


class AI:
    def __init__(
        self, name : str,
        personalidade : str,
        api_key : str, fala = True,
        model='gemini-1.5-flash',
        debug = False
        ) -> None:
        
        Voices.conigureVoice()
        self.name = name
        self.personalidade = personalidade + f"Agora fale como {self.name} em tom de conversação curta sem *, minha fala: "
        self.model = model
        self.fala = fala
        self.debug = debug
        self.api = api_key
        Gemini.gerarModelo(model, api_key)
        self.terminal = Terminal.Terminal(self)
            
    def resposta(self, prompt : str) -> str:
        prompt_completo = self.personalidade + prompt
        if "codigo" in prompt.lower():
            codigos = Acessos.Code()
            prompt_completo += (
                "\n\nAqui estão os códigos que quero que você comente linha por linha, explicando de forma clara e amigável o que cada parte faz:\n"
                + codigos
            )
        if self.debug:
            print(prompt_completo)
        respost = Gemini.Gresponde(prompt_completo)
        print(f"\033[1;33m{self.name}: \033[0m" + respost)
        if self.fala:
            Voices.falar(respost)
        return respost
    
    def run(self) -> None:
        print(f"""
              \033[1;33mModelo: {self.name}\033[0m

              """)
        while True:
            pgt = input("\033[1;32mUsuario: \033[0m")
            if pgt == "SAIR CHAT":
                break
            print("")
            self.resposta(pgt)
            
    def getName(self) -> str:
        return self.name
            
    def runTerminal(self) -> str:
        self.terminal.run()


    