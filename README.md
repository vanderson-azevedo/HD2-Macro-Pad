![ ](https://systemartins.com.br/items_v2/assets/Gemini_Generated_Image_novy9hnovy9hnovy.jpg)
# 🎮 HD2 Macro Pad

Um painel web que permite utilizar o celular como um controle auxiliar para os **Stratagems de Helldivers 2**.

A ferramenta foi criada pensando principalmente em **acessibilidade**, para pessoas que possuem algum tipo de dificuldade motora, cognitiva ou outra limitação que torne mais difícil memorizar e executar rapidamente as sequências dos Stratagems.

> A ideia não é facilitar o jogo, mas facilitar o acesso ao jogo.

## ✨ Recursos

- Controle de Stratagems pelo celular ou tablet
- Loadout com 11 slots
- Busca de Stratagems
- Drag & Drop no desktop e mobile
- Execução das sequências de teclas pelo PC
- Persistência do loadout no navegador
- Interface web acessível pela rede local

## ⚙️ Como funciona

O servidor Flask roda no PC e disponibiliza uma interface web na rede local. O dispositivo (Celular ou Tablet) acessa essa interface e, ao selecionar um Stratagem, o servidor simula a sequência de teclas no PC utilizando `pyautogui`.

## 🚀 Instalação rápida

```bash
git clone https://github.com/vanderson-azevedo/HD2-Macro-Pad.git
cd HD2-Macro-Pad
pip install -r requirements.txt
python server.py
```

Depois, abra no dispositivo (Celular ou Tablet) o endereço informado pelo servidor, por exemplo:

```text
http://192.168.1.105:5000
```

> [!IMPORTANT]
> O dispositivo (Celular ou Tablet) e o SERVIDOR (PC) precisam estar conectados à mesma rede local.

![ ](https://i.ibb.co/RGDPDrts/Sem-T-tulo-1.png)

## 📖 Documentação

- [Instalação](docs/installation.md)
- [Como usar](docs/usage.md)
- [Interface](docs/interface.md)
- [Stratagems disponíveis](docs/stratagems.md)
- [API](docs/api.md)
- [Detalhes técnicos](docs/technical.md)
- [Solução de problemas](docs/troubleshooting.md)

## ⚖️ Licença e termos

- [EULA](EULA.md)
- [Aviso Legal](DISCLAIMER.md)
- [Avisos de terceiros](THIRD-PARTY-NOTICES.md)
- [Licença do código](LICENSE)

## ⚠️ Aviso

Este é um projeto **fan-made e não oficial**, sem afiliação, endosso ou aprovação da Arrowhead Game Studios ou Sony Interactive Entertainment.

Veja o [Aviso Legal](DISCLAIMER.md) e os [Avisos de terceiros](THIRD-PARTY-NOTICES.md) para mais informações.

---

> Desenvolvido com 💖 por **Vanderson Azevedo** pela Super Terra!
