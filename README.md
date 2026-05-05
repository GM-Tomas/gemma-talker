# Gemma Talker

Chat de IA en la terminal. Escribis, responde en streaming. Sin interfaz web, sin
cuentas, sin conexion permanente — el modelo corre localmente en tu maquina.

## Instalacion

---

### Paso 1 — Instalar Python

Necesitas Python 3.10 o superior. Verificá si ya lo tenes:

```bash
python --version
```

Si no tenes Python, descargalo de [python.org](https://www.python.org/downloads/) y
durante la instalacion **tilda la opcion "Add Python to PATH"**.

---

### Paso 2 — Instalar pipx

`pipx` instala herramientas de Python de forma aislada y las deja disponibles en
cualquier terminal, sin activar entornos manualmente.

**Windows:**
```powershell
pip install pipx
python -m pipx ensurepath
```

**macOS / Linux:**
```bash
pip install pipx
pipx ensurepath
```

Despues de correr `ensurepath`, **reinicia la terminal**.

---

### Paso 3 — Bajar el proyecto

**Con git:**
```bash
git clone https://github.com/TomasGM/gemma-talker.git
cd gemma-talker
```

**Sin git (ZIP):**
Descarga el ZIP desde GitHub, extraelo en la carpeta que quieras y abrí una terminal
en esa carpeta.

> La carpeta no se puede mover ni borrar despues de instalar — `gemma` va a seguir
> apuntando a ella.

---

### Paso 4 — Instalar

**Windows:**
```powershell
.\install.ps1
```

**macOS / Linux:**
```bash
bash install.sh
```

El script descarga las dependencias precompiladas (sin necesidad de compiladores ni
Visual Studio) e instala `gemma` como comando global.

---

### Primer uso

```bash
gemma
```

La primera vez descarga el modelo automaticamente (~3.5 GB). Las siguientes arrancan
directo.

---

### GPU NVIDIA (opcional)

Si tenes una GPU NVIDIA y queres que el modelo corra mas rapido, primero fijate tu
version de CUDA con `nvidia-smi` (esquina superior derecha) y despues:

**Windows:**
```powershell
# CUDA 12.1
.\install.ps1 -Backend cu121

# CUDA 12.2
.\install.ps1 -Backend cu122

# CUDA 11.8
.\install.ps1 -Backend cu118
```

**macOS / Linux:**
```bash
bash install.sh cu121
```

**macOS con Apple Silicon:**
```bash
bash install.sh metal
```

---

## Uso

```bash
gemma
```

```bash
gemma-talker
```

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
| `GEMMA_TALKER_REPO_ID` | `bartowski/google_gemma-4-E2B-it-GGUF` |
| `GEMMA_TALKER_MODEL_FILE` | `google_gemma-4-E2B-it-Q4_K_M.gguf` |
| `GEMMA_TALKER_HISTORY` | `~/.gemma_chat_history` |
| `GEMMA_TALKER_GPU_LAYERS` | `-1` |
| `GEMMA_TALKER_CTX` | `32768` |
| `GEMMA_TALKER_TEMPERATURE` | `0.7` |
| `GEMMA_TALKER_MAX_TOKENS` | `2048` |

Ejemplo:

```powershell
$env:GEMMA_TALKER_CTX = "8192"
gemma
```

## OpenCode

Podés usar Gemma 4 E2B como backend de [OpenCode](https://opencode.ai) (el agente de
codigo de terminal) a traves del servidor OpenAI-compatible incluido en este proyecto.

### Paso 1 — Instalar con soporte servidor

**Windows:**
```powershell
.\install.ps1 -Server
```

**macOS / Linux:**
```bash
bash install.sh --server
```

### Paso 2 — Levantar el servidor

```bash
gemma-serve
```

Al iniciar imprime el snippet exacto para `opencode.json`. El servidor queda escuchando
en `http://127.0.0.1:8000/v1`.

### Paso 3 — Configurar OpenCode

Pega esto en `opencode.json` en la raiz de tu proyecto (o en
`~/.config/opencode/config.json` para que aplique globalmente):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "gemma-local": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Gemma Local",
      "options": {
        "baseURL": "http://127.0.0.1:8000/v1"
      },
      "models": {
        "google_gemma-4-E2B-it-Q4_K_M.gguf": {
          "name": "Gemma 4 E2B",
          "limit": {
            "context": 32768,
            "output": 2048
          }
        }
      }
    }
  }
}
```

Despues abrí OpenCode con `opencode` y seleccioná **Gemma Local / Gemma 4 E2B** en el
selector de modelos (`/models`).

> Si cambiaste el modelo con `GEMMA_TALKER_MODEL_FILE`, ajusta la clave del modelo en
> el JSON para que coincida con el nombre del archivo `.gguf` que estas usando.

---

## Desarrollo

Para contribuir o modificar el proyecto:

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -e ".[dev]"
```

Ejecutar tests:

```bash
pytest
```

## Arquitectura

```text
gemma_talker/
  domain/              Mensajes y conversacion pura
  application/         Casos de uso, comandos y puertos
  infrastructure/      Adaptadores: llama.cpp, terminal y Markdown
  cli.py               Punto de entrada del chat (gemma / gemma-talker)
  serve.py             Servidor OpenAI-compatible para OpenCode (gemma-serve)
tests/                 Tests unitarios
```

- `domain` no conoce Rich, Hugging Face, llama.cpp ni archivos.
- `application` coordina la conversacion a traves de puertos.
- `infrastructure` contiene los detalles externos reemplazables.
- `cli.py` conecta todo para correrlo como herramienta de terminal.

