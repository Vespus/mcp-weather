from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import requests, os
from dotenv import load_dotenv

# Hole .env aus dem übergeordneten Verzeichnis
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = FastAPI(title="OpenWeather MCP Tool")

@app.get("/weather")
def get_weather(city: str = Query(...)):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=de"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }
    return {"error": f"{response.status_code}", "details": response.text}

@app.get("/openapi.yaml", include_in_schema=False)
def serve_yaml():
    return FileResponse("openapi.yaml", media_type="text/yaml")

