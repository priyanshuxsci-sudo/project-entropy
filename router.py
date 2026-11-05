import requests
import json
from registory import ADAPTORS
import uuid
import time
from tavily_grounding import tavily_search
from caller import auto_caller

class Router:
    def __init__(self, model_name, query, grounding, fallbacks=None):
        candidates = [model_name] + (fallbacks or [])
        self.query = query
        self.model_name = model_name
        self.grounding = grounding
        self.searched = False

        print(f"\nRouter initialized with model: {model_name}\n")

        start_time = time.perf_counter()
        if self.grounding == "on":
            context = tavily_search(query)
            query = f" Here's the Context:\n{context or ''}\n\nUser Query:\n{query}"
            self.searched = True
        if self.grounding == "auto":
            auto_response = auto_caller(query).strip()
            if auto_response.startswith("```"):
                lines = auto_response.splitlines()
                if lines[0].strip().lower() in ("```json", "```"):
                    lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                auto_response = "\n".join(lines)

                print(f"\nAuto-caller response:\n{auto_response}\n")
                search_query = query
                try:
                    start = auto_response.index("{")
                    end = auto_response.rindex("}") + 1
                    decision = json.loads(auto_response[start:end])
                    self.searched = decision.get("search_grounding") is True
                    search_query = decision.get("query", query)
                except (ValueError, TypeError):
                    self.searched = False
        
                if self.searched:
                    context = tavily_search(search_query)
                    query = f"Here's the context :\n{context or ''}\n\nUser Query:\n{query}"

        for name in candidates:
            try:       
                provider, model = name.split("/", 1)
                self.a_response, self.usage = ADAPTORS[provider](provider, model, query)
                self.used_model = name
                self.output = {
                    "id": f"en-{uuid.uuid4().hex[:12]}",
                    "model": self.model_name,
                    "used_model": self.used_model,
                    "choices": [
                        {
                            "message": {
                                "role": "assistant",
                                "content": self.a_response
                            },
                            "finish_reason": "stop"
                        }
                    ],
                    "usage": self.usage,
                    "entropy": {
                        "fallback_used": True if self.used_model != self.model_name else False,
                        "latency_ms": round((time.perf_counter() - start_time) * 1000),
                        "grounding": {
                            "mode" : self.grounding,
                            "searched": self.searched
                        },
                }
                }
                return
            except Exception as error:
                last_error = error

        raise last_error