from google_adaptor import google_ai
from mistral_adaptor import mistral_ai
from nvidia_adaptor import nvidia_ai

ADAPTORS = {
    "google": google_ai,
    "mistral": mistral_ai,
    "nvidia": nvidia_ai,
}