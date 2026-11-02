import requests
import json
from registory import ADAPTORS
import uuid
import time

class Router:
    def __init__(self, model_name, query, fallbacks=None):
        candidates = [model_name] + (fallbacks or [])
        self.query = query
        self.model_name = model_name

        print(f"\nRouter initialized with model: {model_name}\n")
        for name in candidates:
            try:
                provider, model = name.split("/", 1)
                start_time = time.perf_counter()
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
                        "grounding": "off"
                    }
                }
                return
            except Exception as error:
                last_error = error

        raise last_error