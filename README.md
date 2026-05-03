# Gemma Talker

Chat minimalista de terminal con Gemma 2 2B, `llama.cpp` y descarga automatica del
modelo desde Hugging Face.

La idea es que se sienta como una herramienta tipo Claude Code desde la terminal:
abrir, escribir, recibir respuesta en streaming, limpiar contexto, cambiar system
prompt y guardar la conversacion cuando haga falta.

## Instalacion

Requisitos:

- Python 3.10 o superior.
- Acceso a internet la primera vez, para descargar el modelo.
- Dependencias de compilacion si tu sistema no consigue una rueda precompilada de
  `llama-cpp-python`.

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

En macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Uso

```bash
gemma-talker
```

Tambien queda disponible el alias corto:

```bash
gemma
```

Si preferis no instalar el comando:

```bash
python -m gemma_talker
```

La primera ejecucion descarga `gemma-2-2b-it-Q4_K_M.gguf` y despues usa el cache
local de Hugging Face.

## Comandos del chat

| Comando | Accion |
| --- | --- |
| `/help` | Muestra la ayuda |
| `/clear` | Limpia el historial de la conversacion |
| `/system <texto>` | Define el system prompt |
| `/system` | Muestra el system prompt actual |
| `/save` | Guarda la conversacion en un archivo Markdown |
| `/salir` | Sale del chat |

Tambien podes salir con `Ctrl+C` o `Ctrl+D`.

## Configuracion

Se puede ajustar el modelo y algunos parametros con variables de entorno:

| Variable | Valor por defecto |
| --- | --- |
| `GEMMA_TALKER_REPO_ID` | `bartowski/gemma-2-2b-it-GGUF` |
| `GEMMA_TALKER_MODEL_FILE` | `gemma-2-2b-it-Q4_K_M.gguf` |
| `GEMMA_TALKER_HISTORY` | `~/.gemma_chat_history` |
| `GEMMA_TALKER_GPU_LAYERS` | `-1` |
| `GEMMA_TALKER_CTX` | `4096` |
| `GEMMA_TALKER_TEMPERATURE` | `0.7` |
| `GEMMA_TALKER_MAX_TOKENS` | `2048` |

Ejemplo:

```powershell
$env:GEMMA_TALKER_CTX = "8192"
gemma-talker
```

## Arquitectura

El proyecto usa una arquitectura hexagonal liviana:

```text
gemma_talker/
  domain/              Mensajes y conversacion pura
  application/         Casos de uso, comandos y puertos
  infrastructure/      Adaptadores: llama.cpp, terminal y Markdown
  cli.py               Punto de entrada y armado de dependencias
chat_gemma.py          Wrapper compatible con el script anterior
tests/                 Tests unitarios
```

Las reglas principales quedan asi:

- `domain` no conoce Rich, Hugging Face, llama.cpp ni archivos.
- `application` coordina la conversacion a traves de puertos.
- `infrastructure` contiene los detalles externos reemplazables.
- `cli.py` conecta todo para correrlo como herramienta de terminal.

## Desarrollo

Instalar dependencias de desarrollo:

```bash
python -m pip install -e ".[dev]"
```

Ejecutar tests:

```bash
pytest
```

El archivo `chat_gemma.py` sigue funcionando como compatibilidad:

```bash
python chat_gemma.py
```
