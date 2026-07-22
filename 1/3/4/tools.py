import math
import datetime
import requests
from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression and return the result.
    Supports basic arithmetic (+, -, *, /), powers (**), and math functions (sqrt, sin, cos, etc.)."""
    try:
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"


@tool
def word_counter(text: str) -> str:
    """Count the number of words, characters, and sentences in the given text."""
    words = len(text.split())
    characters = len(text)
    characters_no_spaces = len(text.replace(" ", ""))
    sentences = text.count(".") + text.count("!") + text.count("?")
    return (
        f"Words: {words}\n"
        f"Characters (with spaces): {characters}\n"
        f"Characters (without spaces): {characters_no_spaces}\n"
        f"Sentences: {sentences}"
    )


@tool
def get_current_time(timezone: str = "UTC") -> str:
    """Get the current date and time. Optionally specify a timezone name (e.g., 'UTC', 'US/Eastern')."""
    try:
        now = datetime.datetime.now(datetime.timezone.utc)
        return f"Current UTC time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except Exception as e:
        return f"Error getting time: {e}"


@tool
def fetch_webpage_content(url: str) -> str:
    """Fetch and return the plain-text content of a webpage given its URL."""
    try:
        import re
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        text = response.text
        clean = re.sub(r"<[^>]+>", " ", text)
        clean = re.sub(r"\s+", " ", clean).strip()
        return clean[:3000] + ("..." if len(clean) > 3000 else "")
    except Exception as e:
        return f"Error fetching webpage: {e}"


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city using the Open-Meteo free API (no key required).
    Provide the city name (e.g., 'London', 'New York', 'Mumbai')."""
    try:
        from urllib.parse import quote
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={quote(city)}&count=1"
        geo_resp = requests.get(geo_url, timeout=10).json()
        if not geo_resp.get("results"):
            return f"Could not find location for city: {city}"

        location = geo_resp["results"][0]
        lat, lon = location["latitude"], location["longitude"]
        name = location.get("name", city)
        country = location.get("country", "")

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current_weather=true"
        )
        weather_resp = requests.get(weather_url, timeout=10).json()
        cw = weather_resp.get("current_weather", {})

        temp = cw.get("temperature", "N/A")
        wind = cw.get("windspeed", "N/A")
        code = cw.get("weathercode", -1)

        wmo_codes = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Icy fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
            80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
            95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Heavy thunderstorm with hail",
        }
        condition = wmo_codes.get(code, f"Weather code {code}")

        return (
            f"Weather in {name}, {country}:\n"
            f"  Condition  : {condition}\n"
            f"  Temperature: {temp}C\n"
            f"  Wind Speed : {wind} km/h"
        )
    except Exception as e:
        return f"Error fetching weather: {e}"
