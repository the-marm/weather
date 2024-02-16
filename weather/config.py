"""Module contains configuration for the application."""

import os

from dotenv import load_dotenv

load_dotenv()


OWM_TOKEN = os.getenv("OWM_TOKEN", "")
OWM_URL = (
    "https://api.openweathermap.org/data/2.5/weather?"
    "lat={latitude}&lon={longitude}&"
    "appid=" + OWM_TOKEN + "&lang=us&"
    "units=metric"
)
