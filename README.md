# 🎮 HD2 Stratagem Macro Pad

Um painel de macros web que permite utilizar o celular como um controle auxiliar para os **Stratagems de Helldivers 2**, facilitando sua utilização durante as partidas.

A ferramenta foi **criada pensando principalmente em acessibilidade, para pessoas que possuem algum tipo de dificuldade motora, cognitiva ou outra limitação** que torne mais difícil memorizar e executar rapidamente as sequências dos Stratagems.

A proposta não é tornar o jogo mais fácil ou oferecer uma vantagem competitiva, mas disponibilizar uma forma alternativa de interação que permita que mais pessoas possam aproveitar o jogo com maior autonomia.

O celular funciona apenas como um controle auxiliar, permitindo selecionar o Stratagem desejado e executar sua sequência de forma mais acessível.

A ideia é simples: não facilitar o jogo, mas facilitar o acesso ao jogo.

---

## 📋 Índice

- [Como Funciona](#como-funciona)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Interface](#interface)
- [Stratagems Disponíveis](#stratagems-disponíveis)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [API](#api)
- [Detalhes Técnicos](#detalhes-técnicos)
- [Solução de Problemas](#solução-de-problemas)
- [Aviso Legal](#aviso-legal)
- [EULA](#eula)

---

## Como Funciona

```
[Celular na mesma rede Wi-Fi]
        |
        | HTTP POST /stratagem/<nome>
        v
[Flask Server no PC] → pyautogui → [Helldivers 2]
```

O servidor Flask roda no PC e expõe uma interface web acessível por qualquer dispositivo na mesma rede local. Ao tocar em um stratagem no celular, o servidor simula automaticamente a sequência de teclas correspondente no PC como se você tivesse digitado o código manualmente.

---

## Pré-requisitos

- Python 3.8+
- PC com Windows rodando Helldivers 2
- Celular (ou qualquer dispositivo) na **mesma rede Wi-Fi** que o PC

---

## Instalação

**1. Clone o repositório**
```bash
git clone https://github.com/vanderson-azevedo/Auto-Stratagems-HD2.git
cd Auto-Stratagems-HD2
```

Ou baixe o ZIP direto na página de [**Releases**](https://github.com/vanderson-azevedo/Auto-Stratagems-HD2/releases) e extraia em qualquer pasta.

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Descubra o IP local do seu PC**
```bash
ipconfig
```
Procure por `IPv4 Address` na sua interface de rede ativa (ex: `192.168.1.105`).

**4. Inicie o servidor**
```bash
python server.py
```

O terminal exibirá:
```
Servidor rodando! Acesse pelo seu dispositivo: http://<SEU_IP_LOCAL>:5000
```

**5. Acesse no celular**

Abra o navegador do celular e acesse:
```
http://192.168.1.105:5000
```
*(substitua pelo IP do seu PC)*

---

## Como Usar

### Montando seu loadout

Você tem **11 slots** de loadout (7 na linha de cima + 4 na linha de baixo), fixos na parte inferior da tela.

**Opção 1 - Arrastar da lista:**
- Desktop: clique e arraste um card para um slot
- Mobile: pressione e segure (~350ms) um card até ele "soltar", depois arraste para o slot desejado

**Opção 2 - Clicar no slot vazio:**
- Toque em qualquer slot vazio para abrir o modal de busca
- Digite o nome do stratagem para filtrar
- Toque no resultado para atribuir ao slot

### Disparando um stratagem

Toque em qualquer slot **preenchido** o servidor executa a sequência de teclas no PC instantaneamente.

### Removendo do slot

Toque no **✕** que aparece no canto superior direito de cada slot preenchido.

> ⚠️ **Importante:** O jogo precisa estar em foco no PC no momento do disparo. O servidor simula teclas globalmente via `pyautogui`.

---

## Interface

```
┌─────────────────────────────────────┐
│  🔱 HD2 Stratagems                  │  ← Header fixo
├─────────────────────────────────────┤
│                                     │
│  🦅 Eagle                           │
│  [card] [card] [card]               │  ← Lista scrollável
│                                     │     com ícones SVG
│  🛸 Orbital                         │     e categorias
│  [card] [card] [card]               │
│  ...                                │
├─────────────────────────────────────┤
│  [S1][S2][S3][S4][S5][S6][S7]       │  ← Loadout fixo
│      [S8][S9][S10][S11]             │     no rodapé
└─────────────────────────────────────┘
```

**Modal de busca** (abre ao clicar em slot vazio):
```
┌─────────────────────────────────────┐
│  🔍 [buscar stratagem...]    [✕]    │
│─────────────────────────────────────│
│  [card] [card] [card]               │
│  [card] [card] [card]               │
│  ...                                │
└─────────────────────────────────────┘
```

---

## Stratagems Disponíveis

### 🦅 Eagle (8)
| Nome | Código |
|------|--------|
| Eagle Airstrike | `↑ → ↑ ↑` |
| Eagle 500kg Bomb | `↑ → → ↑ →` |
| Eagle Cluster Bomb | `↑ → ↑ ↑ →` |
| Eagle Napalm Airstrike | `↑ → ↓ ↑` |
| Eagle Smoke Strike | `↑ → ↑ →` |
| Eagle 110mm Rocket Pods | `↑ → ↑ ←` |
| Eagle Strafing Run | `↑ → →` |
| Eagle Rearm | `↑ ↑ ← ↑ →` |

### 🛸 Orbital (11)
| Nome | Código |
|------|--------|
| Orbital Precision Strike | `→ → ↑` |
| Orbital Laser | `→ ↓ ↑ → ↓` |
| Orbital Railcannon Strike | `→ ↓ ↑ → ↑` |
| Orbital Gatling Barrage | `→ ↓ ↑ ←` |
| Orbital Airburst Strike | `→ → ↓` |
| Orbital 120mm HE Barrage | `→ ↓ ← → ↓` |
| Orbital 380mm HE Barrage | `→ ↓ ↓ ← ↓ →` |
| Orbital EMS Strike | `→ ↓ ↑ ↓` |
| Orbital Smoke Strike | `→ ↓ ↓ →` |
| Orbital Gas Strike | `→ ↓ ↓ ←` |
| Orbital Napalm Barrage | `→ ↓ ← ← ↓` |
| Orbital Walking Barrage | `→ ↓ → ↓ → ↓` |
| Orbital Illumination Flare | `→ ↓ ↓ ↑` |

### 🗼 Sentinelas (10)
Machine Gun Sentry, Gatling Sentry, Autocannon Sentry, Mortar Sentry, Rocket Sentry, Tesla Tower, EMS Mortar Sentry, Laser Sentry, Flame Sentry, Gas Mortar Sentry

### 🛡️ Defesa & Minas (8)
HMG Emplacement, Anti-Tank Emplacement, Grenadier Battlement, Shield Generator Relay, Anti-Personnel Minefield, Incendiary Mines, Anti-Tank Mines, Gas Mines

### 🔫 Armas de Suporte (30+)
Machine Gun, Expendable Anti-Tank, Stalwart, Laser Cannon, Anti-Materiel Rifle, Recoilless Rifle, Grenade Launcher, Flamethrower, HMG, Autocannon, Arc Thrower, Quasar Cannon, Airburst Launcher, Commando, Spear, Railgun, WASP Launcher, Breaching Hammer, Epoch, Bullet Storm, Speargun, Defoliation Tool, De-Escalator, Expendable Napalm, Sterilizer, Leveller, Belt-Fed Grenade Launcher, C4 Pack, Cremator, Maxigun, One True Flag, Meltagun, Solo Silo

### 🎒 Backpacks (12)
Supply Pack, Jump Pack, Ballistic Shield, Guard Dog, Rover, Shield Generator Pack, Directional Shield, Hot Dog, K-9, Hover Pack, Dog Breath, Warp Pack

### 🤖 Exosuits (5)
Patriot Exosuit, Emancipator Exosuit, Lumberer Exosuit, Breakthrough Exosuit, Bastion MK XVI

### 🚗 Veículos (3)
Fast Recon Vehicle, Incinerator FRV, Supply FRV

### 🎯 Missão (8)
Portable Hellbomb, Cargo Container, Drill, SEAF Artillery, Seismic Probe, Upload Data, Dark Fluid Vessel, Call In Super Destroyer

### ⭐ Essenciais (5)
Reinforce, Resupply, SOS Beacon, Hellbomb, Super Earth Flag

---

## Estrutura do Projeto

```
HD2 - keybinds/
├── server.py           # Servidor Flask + mapeamento de stratagems
├── requirements.txt    # Dependências Python
├── README.md
└── web/
    ├── index.html      # Frontend completo (HTML + CSS + JS)
    └── icons/          # ~100 ícones SVG dos stratagems
        ├── Eagle_Airstrike_Stratagem_Icon_Background.svg
        ├── Orbital_Laser_Stratagem_Icon_Background.svg
        └── ...
```

---

## API

### `GET /`
Serve o frontend (`web/index.html`).

### `GET /icons/<filename>`
Serve os ícones SVG de `web/icons/`.

### `POST /stratagem/<name>`
Executa a sequência de teclas do stratagem especificado.

**Parâmetros:**
- `name` chave do stratagem (ex: `eagle_airstrike`, `orbital_laser`)

**Resposta de sucesso (`200`):**
```json
{ "ok": true, "stratagem": "eagle_airstrike" }
```

**Resposta de erro (`404`):**
```json
{ "error": "Stratagem nao encontrado" }
```

**Exemplo:**
```bash
curl -X POST http://192.168.1.105:5000/stratagem/orbital_laser
```

---

## Detalhes Técnicos

### Execução de teclas

Cada stratagem é executado em uma **thread separada** para não bloquear a resposta HTTP. A sequência segue o padrão:

```
Ctrl (hold) → tecla1 → tecla2 → ... → Ctrl (release)
```

Com `0.1s` de delay entre cada tecla para garantir que o jogo registre corretamente.

```python
pyautogui.FAILSAFE = False  # Evita crash ao mover mouse para canto
pyautogui.PAUSE = 0         # Remove delay padrão do pyautogui
```

### Persistência do loadout

Os slots são salvos automaticamente no `localStorage` do navegador seu loadout persiste entre sessões sem necessidade de servidor ou banco de dados.

### Drag & Drop

| Plataforma | Comportamento |
|------------|---------------|
| Mobile | Long press (350ms) para iniciar drag, arrastar para slot |
| Desktop | Mousedown para iniciar drag, arrastar para slot |

---

## Solução de Problemas

**O servidor fecha sozinho ao mover o mouse para o canto da tela**
→ Certifique-se que `pyautogui.FAILSAFE = False` está no `server.py`. Já está configurado por padrão.

**O celular não consegue acessar o servidor**
→ Verifique se ambos estão na mesma rede Wi-Fi. Confirme o IP com `ipconfig` e tente acessar `http://<IP>:5000` no navegador do celular.

**O stratagem não é executado no jogo**
→ O jogo precisa estar em foco (janela ativa) no PC. Clique na janela do jogo antes de usar o painel.

**Ícone não aparece (404)**
→ Confirme que os arquivos SVG estão em `web/icons/` e que os nomes batem com os mapeados no `index.html`.

**Teclas sendo registradas fora do jogo**
→ O `pyautogui` simula teclas globalmente no sistema. Minimize outras janelas ou use o jogo em tela cheia.

---

> *"For Super Earth!"* 🌍

---

## Aviso Legal

Este projeto é um **fan-made tool** não oficial, sem qualquer afiliação, endosso ou aprovação da **Arrowhead Game Studios** ou da **Sony Interactive Entertainment**.

### Ícones

Os ícones SVG utilizados neste projeto (`web/icons/`) são **propriedade intelectual da Arrowhead Game Studios AB**, criadores de Helldivers 2. Eles foram obtidos da [Helldivers Wiki](https://helldivers.wiki.gg/) uma wiki de conteúdo aberto mantida pela comunidade e são usados aqui **exclusivamente para fins não comerciais e educacionais**, como ferramenta de auxílio a jogadores.

- **Helldivers 2** é marca registrada da Arrowhead Game Studios AB / Sony Interactive Entertainment.
- Este repositório **não distribui, vende ou monetiza** nenhum ativo do jogo.
- Caso a Arrowhead Game Studios ou a Sony Interactive Entertainment solicitem a remoção dos assets, eles serão prontamente retirados.

### Código

O código-fonte deste projeto (Python/Flask + HTML/JS) é de autoria própria e distribuído livremente para uso pessoal.

---

Desenvolvido com 💖 por **Vanderson Azevedo** pela Super Terra!

---

## EULA

**Contrato de Licença de Uso do Usuário Final (EULA)**

Ao baixar, instalar ou utilizar o **HD2 Stratagem Macro Pad**, você concorda com os termos abaixo.

### 1. Concessão de Licença

Este software é disponibilizado gratuitamente para **uso pessoal e não comercial**. É permitido copiar, modificar e redistribuir o código-fonte, desde que mantida a atribuição original ao autor e que nenhuma cobrança seja realizada.

### 2. Restrições

- É **proibido** usar este software para fins comerciais, venda ou monetização de qualquer forma.
- É **proibido** remover ou alterar os avisos de autoria e atribuição presentes no projeto.
- É **proibido** utilizar este software de forma que viole os Termos de Serviço da **Arrowhead Game Studios** ou da **Sony Interactive Entertainment**.

### 3. Assets de Terceiros

Os ícones SVG incluídos em `web/icons/` **não fazem parte desta licença**. Eles são propriedade intelectual da **Arrowhead Game Studios AB** e estão sujeitos aos direitos autorais dos respectivos detentores. O uso desses assets é feito exclusivamente para fins não comerciais, com base no uso justo (*fair use*) como ferramenta de auxílio à comunidade.

### 4. Isenção de Garantias

Este software é fornecido **"como está" (as-is)**, sem garantias de qualquer tipo, expressas ou implícitas. O autor não se responsabiliza por:

- Danos ao sistema, arquivos ou hardware decorrentes do uso do software.
- Banimentos, penalidades ou restrições impostas pela Arrowhead Game Studios ou Sony em decorrência do uso desta ferramenta.
- Mau funcionamento causado por atualizações do jogo ou do sistema operacional.

### 5. Uso por Conta e Risco

O uso deste software é de **inteira responsabilidade do usuário**. Recomenda-se verificar os Termos de Serviço do jogo antes de utilizar qualquer ferramenta de automação de teclas.

### 6. Rescisão

Esta licença é automaticamente rescindida caso qualquer uma das restrições acima seja violada.

### 7. Lei Aplicável

Este acordo é regido pelas leis da **República Federativa do Brasil**.
