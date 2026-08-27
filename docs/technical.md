# 🧩 Detalhes técnicos

## Arquitetura

O projeto utiliza:

- Python
- Flask
- PyAutoGUI
- HTML
- CSS
- JavaScript
- SVG

O servidor Flask disponibiliza a interface web e recebe as requisições dos Stratagems.

## Execução das teclas

Cada Stratagem é executado em uma thread separada para não bloquear a resposta HTTP.

A sequência segue o padrão:

```text
Ctrl (hold) → tecla1 → tecla2 → ... → Ctrl (release)
```

Existe um delay de `0.1s` entre as teclas para garantir que o jogo registre corretamente os comandos.

Configurações utilizadas pelo PyAutoGUI:

```python
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
```

## Persistência do loadout

Os slots são salvos no `localStorage` do navegador.

Não é necessário banco de dados para armazenar o loadout.

## Drag & Drop

| Plataforma | Comportamento |
|---|---|
| Mobile | Long press de aproximadamente 350 ms para iniciar o drag |
| Desktop | Mousedown para iniciar o drag |

## Estrutura

```text
HD2 - keybinds/
├── server.py
├── requirements.txt
├── README.md
└── web/
    ├── index.html
    └── icons/
        ├── Eagle_Airstrike_Stratagem_Icon_Background.svg
        ├── Orbital_Laser_Stratagem_Icon_Background.svg
        └── ...
```
