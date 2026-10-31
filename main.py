import requests
import json
from registory import ADAPTORS

class Router:
    def __init__(self, model_name):
        self.model_name = model_name
        provider, model = model_name.split("/", 1)
        return ADAPTORS[provider](model)