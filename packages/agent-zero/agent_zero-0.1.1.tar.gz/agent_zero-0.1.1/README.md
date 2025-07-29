# Agent Zero

**Agent Zero** is a flexible voice agent framework designed for automated outbound calling, real-time inference, and multi-agent orchestration.  
It supports OpenAI, Gemini, Groq, Fireworks, and other LLMs, with full telephony support via Twilio and Pipecat.

---

## 📦 Installation

Install the latest stable release from PyPI:

```bash
pip install agent-zero
```

Or, if you want to install with development and documentation dependencies:

```bash
pip install "agent-zero[dev,docs]"
```

---

## 🚀 Quick Start

You can import and use the core setup functions as follows:

```python
from agent_zero import init_config
from agent_zero import register_custom_tools
from agent_zero import register_routes, register_custom_handlers
```

---

## 🧩 Example Usage

```python
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agent_zero import init_config
from agent_zero import register_custom_tools
from agent_zero import register_routes, register_custom_handlers

PROJECT_ROOT = Path(__file__).parent
CONFIG_PATH = PROJECT_ROOT / "config.yaml"
HANDLERS_PATH = str(PROJECT_ROOT / "custom/handlers")
TOOLS_CONFIG_PATH = str(PROJECT_ROOT / "custom/tools/config.yaml")
TOOLS_FUNCTIONS_PATH = str(PROJECT_ROOT / "custom/tools/functions")

init_config(str(CONFIG_PATH))
register_custom_handlers(HANDLERS_PATH)
register_custom_tools(TOOLS_FUNCTIONS_PATH, TOOLS_CONFIG_PATH)

app = FastAPI()
register_routes(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔧 Configuration

Each project must provide a `config.yaml` file with the following structure:

```yaml
vad_params:
  confidence: 0.5
  min_volume: 0.6
  start_secs: 0.2
  stop_secs: 0.8

llm:
  main:
    vendor: "openai"
    model: "gpt-4.1-mini-2025-04-14"
  utils:
    vendor: "openai"
    model: "gpt-4.1-mini-2025-04-14"

vector_db:
  type: "Weaviate"

embedding:
  type: "OpenAI/text-embedding-3-small"

agent_inputs:
  project_name: agent_zero
  language_code: en
  language: English
  translate_prompt: false
  agent_name: Emma
  agent_company_name: SpaceStep

tools: ["greet_user"]
agent_id:
  agent_zero_dev

routes:
  routers:
    - prefix: /agent_zero
      routes:
        - path: /
          methods: [POST]
          handler: agent_inference
        ...
  websockets:
    - prefix: /agent_zero
      routes:
        - path: /outbound/ws
          handler: outbound_websocket_endpoint
```

---

## 🛠️ Tool Configuration

Each tool must be declared in the `tools` section of `config.yaml` and implemented inside `functions/`.

Example `tools/config.yaml`:

```yaml
greet_user:
  description: "Say hello to a user by name."
  parameters:
    type: object
    properties:
      name:
        type: string
        description: "User's first name."
    required: ["name"]
```

---

## 🌐 Environment Variables

Define your API keys and runtime secrets in `.env`:

```env
OPENAI_API_KEY=
GROQ_API_KEY=
FIREWORKS_API_KEY=
GOOGLE_CREDENTIALS_JSON=

# Tooling
TOOL_CHECK_SLOT_AVAILABILITY_WEBHOOK_URL=
TOOL_BOOKING_WEBHOOK_URL=

# Audio + Voice
DEEPGRAM_API_KEY=
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=

# Twilio
TWILIO_ACCOUNT_ID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
SERVER_ADDRESS=
CALL_STATUS_URL=

# Inference service
INFERENCE_URL=
CONNEXITY_API_KEY=
```

---

## 🧱 Directory Structure

```
src/agent_zero/
├── core/                 # Runtime core: agents, tools, config, models
│   ├── tools/            # Built-in tools and tool manager
│   ├── llm/              # LLM model implementations (OpenAI, Gemini, etc.)
│   ├── pipecat_w_twillio # Pipecat + Twilio integration
│   ├── config.py         # YAML config parser
│   ├── prompts.py        # Prompt loading utilities
│   └── agent.py          # Main agent logic
├── api/                  # FastAPI routes and custom handlers
│   ├── handlers.py       # Handler implementations
│   └── router.py         # Route registration from config
├── data/                 # Schemas, cache, and validators
├── helpers/              # Runtime utilities
├── assets/               # Background audio / SFX
```

---

## 📄 License

MIT License. See `LICENSE`.