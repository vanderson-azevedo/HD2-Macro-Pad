# 🛠️ Solução de problemas

## O servidor fecha sozinho ao mover o mouse para o canto da tela

Certifique-se de que:

```python
pyautogui.FAILSAFE = False
```

está configurado no `server.py`.

Essa configuração já está prevista no projeto.

## O dispositivo (Celular ou Tablet) não consegue acessar o servidor

Verifique:

1. Se o PC e o Celular ou Tablet estão na mesma rede Wi-Fi.
2. O endereço IPv4 do PC com `ipconfig`.
3. Se o endereço acessado no Celular ou Tablet contém a porta `5000`.

Exemplo:

```text
http://192.168.1.105:5000
```

## O Stratagem não é executado no jogo

O jogo precisa estar em foco, ou seja, ser a janela ativa no PC.

Clique na janela do jogo antes de utilizar o painel.

## O ícone não aparece

Se houver erro `404`, confirme que:

- O arquivo SVG existe em `web/icons/`.
- O nome do arquivo corresponde ao mapeamento utilizado pelo `index.html`.

## Teclas sendo registradas fora do jogo

O `pyautogui` simula teclas globalmente no sistema.

Minimize outras janelas ou utilize o jogo em tela cheia para reduzir a possibilidade de os comandos serem recebidos por outro aplicativo.
