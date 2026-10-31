import requests
import json
from registory import ADAPTORS

class Router:
    def __init__(self, model_name, query, token=None):
        self.token = token
        self.query = query
        self.model_name = model_name
        provider, model = model_name.split("/", 1)
        self.response, self.token = ADAPTORS[provider](model, query)