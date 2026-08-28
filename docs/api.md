# 🔌 API

O servidor Flask disponibiliza uma API HTTP local.

## `GET /`

Serve o frontend localizado em:

```text
web/index.html
```

## `GET /icons/<filename>`

Serve um ícone SVG localizado em:

```text
web/icons/
```

## `POST /stratagem/<name>`

Executa a sequência de teclas do Stratagem especificado.

### Parâmetros

`name` é a chave interna do Stratagem.

Exemplo:

```text
eagle_airstrike
```

ou:

```text
orbital_laser
```

### Resposta de sucesso

HTTP `200`:

```json
{
  "ok": true,
  "stratagem": "eagle_airstrike"
}
```

### Resposta de erro

HTTP `404`:

```json
{
  "error": "Stratagem nao encontrado"
}
```

### Exemplo

```bash
curl -X POST http://192.168.1.105:5000/stratagem/orbital_laser
```
