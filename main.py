import requests
import json
from registory import ADAPTORS

class Router:
    def __init__(self, model_name, query):
        self.query = query
        self.model_name = model_name
        provider, model = model_name.split("/", 1)
        response, token = ADAPTORS[provider](model, query)
        return response, token