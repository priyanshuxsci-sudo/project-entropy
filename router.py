import requests
import json
from registory import ADAPTORS

class Router:
    def __init__(self, model_name, query, fallbacks=None):
        candidates = [model_name] + (fallbacks or [])
        self.query = query
        self.model_name = model_name

        print(f"Router initialized with model: {model_name}")
        for name in candidates:
            try:
                provider, model = name.split("/", 1)
                self.response = ADAPTORS[provider](provider, model, query)
                self.used_model = name
                return
            except Exception as error:
                last_error = error

        raise last_error