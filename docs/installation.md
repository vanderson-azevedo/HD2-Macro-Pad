# 🚀 Instalação

## Pré-requisitos

- Python 3.8+
- PC com Windows rodando Helldivers 2
- Celular, Tablet ou outro dispositivo na mesma rede local que o PC

## 1. Clone o repositório

```bash
git clone https://github.com/vanderson-azevedo/HD2-Macro-Pad.git
cd HD2-Macro-Pad
```

Ou baixe o ZIP diretamente pela página de Releases e extraia em qualquer pasta.

## 2. Instale as dependências

```bash
pip install -r requirements.txt
```

## 3. Descubra o IP local do PC

No Windows:

```bash
ipconfig
```

Procure o endereço IPv4 da interface de rede ativa, por exemplo:

```text
192.168.1.105
```

## 4. Inicie o servidor

```bash
python server.py
```

O terminal exibirá um endereço semelhante a:

```text
Servidor rodando! Acesse pelo seu dispositivo: http://<SEU_IP_LOCAL>:5000
```

## 5. Acesse pelo celular ou tablet

Abra o navegador do dispositivo (Celular ou Tablet) e acesse:

```text
http://192.168.1.105:5000
```

Substitua o IP pelo endereço exibido pelo servidor.

> [!IMPORTANT]
> O dispositivo (Celular ou Tablet) e o SERVIDOR (PC) precisam estar conectados à mesma rede local.
