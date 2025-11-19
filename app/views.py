import os
import requests
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from django.core.cache import cache
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

class Home(View):
    def get(self, request):
        return render(request=requests, template_name='home.html')
    


class Weather(View):
    def get(self, request):
       city = request.GET.get("city", "Tashkent").strip()

       if not city:
           return JsonResponse({"error": "City required"}, status = 400)
       cache_key = f"weather:{city.lower()}"

       cached = cache.get(cache_key)
       if cached:
            return JsonResponse({"source": "cache", "data": cached})

       if not OPENWEATHER_KEY:
            return JsonResponse({"error": "API key missing"}, status=500)
       
       try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": OPENWEATHER_KEY, "units": "metric"}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
       except requests.RequestException as e:
            return JsonResponse({"error": "Failed to get weather", "details": str(e)}, status=500)
       
       json_data = response.json()
       data = {
            "city": json_data.get("name"),
            "weather": json_data["weather"][0]["description"],
            "icon": json_data["weather"][0]["icon"],
            "temp": json_data["main"]["temp"],
            "feels_like": json_data["main"]["feels_like"],
            "humidity": json_data["main"]["humidity"],
            "pressure": json_data["main"]["pressure"],
            "wind_speed": json_data["wind"]["speed"]
        }

       cache.set(cache_key, data, timeout=60)
       return JsonResponse({"source": "api", "data": data})


    


