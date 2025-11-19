from django.urls import path
from .views import Home, Weather

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('api/weather/', Weather.as_view(), name='weather_api'),
]
