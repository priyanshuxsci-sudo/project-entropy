# 🌌 Project Entropy: A Smart AI Gateway

> One interface, many AI providers, and a built-in brain that decides when your prompt needs live web search.

An open-source, OpenRouter-style gateway written in plain Python. You send one request in the format `provider/model`, and the gateway routes it to the right provider through a small adapter layer. It retries on temporary failures, falls back to other models, and returns one standard JSON response no matter which provider answered.

⚠️ **Status:** early stage and under active development. The routing, fallback, JSON output, and grounding features work; everything under [Roadmap](#-roadmap) is still planned.

---

## ✨ The Idea

Most gateways only **route**. Project Entropy also **thinks before routing**:

> A lightweight AI layer analyses the user's prompt and automatically decides whether it needs **search grounding**, so developers don't have to flip that switch by hand for every request.

- "Who won yesterday's match?" → needs fresh data → search first 🔍
- "Explain recursion" → no search needed → answer directly ⚡

---

## 🧱 How It Works

```
Client request  ->  Grounding  ->  Router  ->  Registry  ->  Adapter  ->  AI provider
 payload (JSON)     off / on /     splits      looks up      calls the     Gemini / Mistral /
                    auto           the name    the adapter   API (retry)   NVIDIA / Meta
```

1. 📨 You pass a model string like `google/gemini-3.7-flash-lite`, a prompt, a grounding mode, and optional fallbacks
2. 🔍 **Grounding** (if enabled) fetches fresh web results and adds them to the prompt
3. ✂️ The **Router** splits the model string into `provider` and `model`
4. 📒 The **Registry** maps the provider name to its adapter function
5. 🔌 The **Adapter** calls the provider, retrying temporary errors up to 3 times
6. 🛟 If a model still fails, the Router **falls back** to the next model in your list
7. 📦 You get one standard JSON response, whichever model answered

---

## 🕵️ Grounding Modes

Search grounding means giving a model fresh web results so its answer rests on facts instead of memory.

| Mode | What happens |
|------|--------------|
| `"off"` | No search. The prompt goes straight to the model |
| `"on"` | Always search, then add the results to the prompt |
| `"auto"` | A small classifier model decides whether this prompt needs search |

The response tells you **what you asked for** and **what actually happened**:

```json
"grounding": {"mode": "auto", "searched": true}
```

---

## 📦 Request and Response Format

**Request**

```json
{
  "model": "google/gemini-3.7-flash-lite",
  "messages": [{"role": "user", "content": "What are the latest AI developments?"}],
  "fallbacks": ["mistral/ministral-3b-2512"],
  "grounding": "auto"
}
```

**Response**

```json
{
  "id": "en-3f9a1c7b2d4e",
  "model": "google/gemini-3.7-flash-lite",
  "used_model": "mistral/ministral-3b-2512",
  "choices": [
    {
      "message": {"role": "assistant", "content": "..."},
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 240,
    "total_tokens": 252
  },
  "entropy": {
    "fallback_used": true,
    "latency_ms": 1840,
    "grounding": {"mode": "auto", "searched": true}
  }
}
```

- 🔌 The top part follows the familiar OpenAI-style shape
- 🌌 The `entropy` block is Project Entropy's own: whether a fallback was used, how long the request took, and what grounding did

---

## 📁 Project Structure

```
project-entropy/
├── router.py             # Router: grounding, fallback loop, and the JSON output
├── registory.py          # Registry: provider name -> adapter function
├── google_adaptor.py     # Google Gemini adapter (REST via requests)
├── mistral_adaptor.py    # Mistral adapter (official mistralai SDK)
├── nvidia_adaptor.py     # NVIDIA adapter (OpenAI-compatible SDK)
├── meta_adaptor.py       # Meta models adapter (OpenAI-compatible SDK)
├── caller.py             # Classifier call used by grounding "auto"
├── tavily_grounding.py   # Web search via Tavily
└── demo.py               # Example request and response
```

---

## 🔌 Supported Providers

| Provider | Prefix | How it's called |
|----------|--------|-----------------|
| 🔵 Google Gemini | `google/` | REST API with `requests` |
| 🟠 Mistral | `mistral/` | Official `mistralai` SDK |
| 🟢 NVIDIA | `nvidia/` | OpenAI-compatible SDK |
| 🟣 Meta | `meta/` | OpenAI-compatible SDK (through NVIDIA's endpoint) |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/priyanshuxsci-sudo/project-entropy.git
cd project-entropy
```

### 2. Install dependencies

```bash
pip install requests python-dotenv mistralai openai tavily-python
```

### 3. Add your API keys

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your-gemini-key
MISTRAL_API_KEY=your-mistral-key
NVIDIA_API_KEY=your-nvidia-key
META_API_KEY=your-meta-key
TAVILY_API_KEY=your-tavily-key
```

🔐 Never commit your `.env` file. Make sure it is listed in `.gitignore`.

### 4. Run it

```python
import json
from router import Router

payload = {
    "model": "google/gemini-3.7-flash-lite",
    "messages": [{"role": "user", "content": "What are the latest AI developments?"}],
    "fallbacks": ["mistral/ministral-3b-2512"],
    "grounding": "auto",
}

result = Router(
    payload["model"],
    payload["messages"][0]["content"],
    payload["grounding"],
    payload["fallbacks"],
)

print(json.dumps(result.output, indent=2))
```

🏷️ Model names are examples. Use any model your provider currently offers.

---

## 🛟 Retry and Fallback

- 🔁 **Retry:** each adapter tries a request up to 3 times, retrying only temporary problems such as timeouts, rate limits (`429`), and server errors (`5xx`)
- 🛟 **Fallback:** if a model still fails, the Router moves to the next model in your `fallbacks` list
- 🏷️ The response shows which model answered (`used_model`) and whether a fallback was used (`fallback_used`)

Tip: put fallbacks on a **different provider**, since an overloaded provider is often overloaded for all of its models.

---

## ➕ Adding a New Provider

1. Create `yourprovider_adaptor.py` with a function that follows the shared shape:

   ```python
   def yourprovider_ai(provider, model, query):
       ...
       return response_text, usage
   ```

2. Register it in `registory.py`:

   ```python
   ADAPTORS = {
       "google": google_ai,
       "mistral": mistral_ai,
       "nvidia": nvidia_ai,
       "meta": meta_ai,
       "yourprovider": yourprovider_ai,
   }
   ```

3. Call it with `"yourprovider/model-name"`. Done! 🎉

---

## 🗺️ Roadmap

- [x] Router with `provider/model` parsing
- [x] Provider registry
- [x] Google, Mistral, NVIDIA, and Meta adapters
- [x] 🔁 Retry on temporary errors and 🛟 fallback across models
- [x] 📦 Standard JSON request and response format
- [x] 🕵️ Auto-grounding: `grounding: "off" | "on" | "auto"`
- [ ] 🧪 Evaluation set to measure how accurately the grounding decision is made
- [ ] ⚡ Run grounding once before the fallback loop
- [ ] 📎 Return the sources used for grounding in the response
- [ ] 💬 Full `messages` support (conversation history and system prompts)
- [ ] 🌐 FastAPI server exposing `/v1/chat/completions`
- [ ] 🌊 Streaming responses (SSE)
- [ ] 🔑 API key authentication, quotas, and rate limiting
- [ ] 📊 Usage and cost logging

---

## 🤝 Contributing

Contributions, ideas, and issues are welcome! This is a learning-in-public project, so beginner-friendly PRs (new adapters, tests, docs) are especially appreciated. 💙

1. Fork the repo
2. Create a branch: `git checkout -b feature/my-feature`
3. Commit your changes and open a pull request

---

## 📄 License

Not yet chosen. A permissive license such as MIT is planned.

---

Built with 🐍 Python and curiosity by [@priyanshuxsci-sudo](https://github.com/priyanshuxsci-sudo)
