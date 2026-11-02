# 🌌 Project Entropy: A Smart AI Gateway

> One interface, many AI providers, and (soon) a built-in brain that decides when your prompt needs live web search.

An open-source, OpenRouter-style gateway written in plain Python. You send one request in the format `provider/model`, and the gateway routes it to the right provider through a small adapter layer.

⚠️ **Status:** early stage and under active development. The core routing layer works; everything under [Roadmap](#-roadmap) is planned.

---

## ✨ The Idea

Most gateways only **route**. Project Entropy is built to also **think before routing**:

> A lightweight AI layer analyses the user's prompt and automatically decides whether it needs **search grounding**, so developers don't have to flip that switch by hand for every request.

- "Who won yesterday's match?" → needs fresh data → search first 🔍
- "Explain recursion" → no search needed → answer directly ⚡

---

## 🧱 How It Works

```
Client request  ->  Router  ->  Registry  ->  Provider adapter  ->  AI provider
 "google/..."     splits       looks up       translates and        Gemini / Mistral /
                  the name     the adapter    calls the API         NVIDIA
```

1. 📨 You pass a model string like `google/gemini-2.5-flash` and a prompt
2. ✂️ The **Router** splits it into `provider` and `model`
3. 📒 The **Registry** maps the provider name to its adapter function
4. 🔌 The **Adapter** builds the provider-specific request and returns the text

Adding a new provider means writing one adapter file and adding one line to the registry. 🎯

---

## 📁 Project Structure

```
project-entropy/
├── router.py            # Router: parses "provider/model" and dispatches the call
├── registory.py         # Registry: provider name -> adapter function
├── google_adaptor.py    # Google Gemini adapter (REST via requests)
├── mistral_adaptor.py   # Mistral adapter (official mistralai SDK)
└── nvidia_adaptor.py    # NVIDIA adapter (OpenAI-compatible SDK)
```

---

## 🔌 Supported Providers

| Provider | Prefix | How it's called |
|----------|--------|-----------------|
| 🔵 Google Gemini | `google/` | REST API with `requests` |
| 🟠 Mistral | `mistral/` | Official `mistralai` SDK |
| 🟢 NVIDIA | `nvidia/` | OpenAI-compatible SDK |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/priyanshuxsci-sudo/project-entropy.git
cd project-entropy
```

### 2. Install dependencies

```bash
pip install requests python-dotenv mistralai openai
```

### 3. Add your API keys

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your-gemini-key
MISTRAL_API_KEY=your-mistral-key
DEEPN_API_KEY=your-nvidia-key
```

🔐 Never commit your `.env` file. Make sure it is listed in `.gitignore`.

### 4. Run it

```python
from router import Router

result = Router("google/gemini-2.5-flash", "What is the capital of France?")
print(result.response)
```

Switching providers only changes the model string:

```python
Router("mistral/mistral-small-latest", "Explain recursion in one line.")
```

---

## ➕ Adding a New Provider

1. Create `yourprovider_adaptor.py` with a function that follows the shared shape:

   ```python
   def yourprovider_ai(provider, model, query):
       ...
       return response_text
   ```

2. Register it in `registory.py`:

   ```python
   ADAPTORS = {
       "google": google_ai,
       "mistral": mistral_ai,
       "nvidia": nvidia_ai,
       "yourprovider": yourprovider_ai,
   }
   ```

3. Call it with `"yourprovider/model-name"`. Done! 🎉

---

## 🗺️ Roadmap

- [x] Router with `provider/model` parsing
- [x] Provider registry
- [x] Google, Mistral, and NVIDIA adapters
- [ ] 🔁 Retry with backoff and 🛟 automatic provider fallback
- [ ] 📋 Standard request format (OpenAI-style `messages`) with `BaseAdapter`
- [ ] 🌐 FastAPI server exposing `/v1/chat/completions`
- [ ] 🌊 Streaming responses (SSE)
- [ ] 🔑 API key authentication, quotas, and rate limiting
- [ ] 📊 Usage and cost logging
- [ ] 🕵️ **Auto-grounding layer:** classifier plus search injection, with `grounding: "auto" | "on" | "off"`
- [ ] 🧪 Evaluation set to measure how accurately the grounding decision is made

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
