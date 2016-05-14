from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
import json
from datetime import datetime
from .helpers import get_weather, generate_pair_code
from django.contrib import admin
import logging
from django.core.exceptions import ValidationError

log = logging.getLogger('django')

# class EmotoSet(models.Model):
    # pass

class Emoto(models.Model):
    name = models.TextField(max_length=200)
    image = models.ImageField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def json(self):
        return {
            "url": self.image.url,
            "name": self.name
        }

    class Meta:
        ordering = ['name']

class Profile(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    username = models.TextField(max_length=100, unique=True)
    partner = models.OneToOneField("Profile", null=True, related_name="recip_partner")
    pair_code = models.TextField(max_length=6, null=True)
    avatar = models.ImageField(null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    city_cached = models.TextField(max_length=100)
    weather_cached = models.TextField(max_length=100)
    time_zone_cached = models.TextField(max_length=100)
    temperature_cached = models.IntegerField()
    weather_icon_url_cached = models.URLField(max_length=2000)
    cache_timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):
        "Make sure to set some props before saving the first time"
        if not self.pk:
            self.pair_code = generate_pair_code()
            self.reload_cache()
        log.info(self.status_json())
        log.info(self.__dict__)
        super().save(*args, **kwargs)    

    def clean(self):
        if -180 > self.latitude or self.latitude > 180:
            raise ValidationError("Latitude must be between -180 and 180")
        if -180 > self.longitude or self.longitude > 180:
            raise ValidationError("Longitude must be between -180 and 180")
        if self.username == "":
            raise ValidationError("Username must not be blank")
        if self.partner and self.partner == self:
            raise ValidationError("User cannot pair with self")

    @property
    def city(self):
        if self.cache_expired():
            self.reload_cache()
        return self.city_cached
        
    @property
    def weather(self):
        if self.cache_expired():
            self.reload_cache()
        return self.weather_cached

    @property
    def time_zone(self):
        if self.cache_expired():
            self.reload_cache()
        return self.time_zone_cached

    @property
    def temperature(self):
        if self.cache_expired():
            self.reload_cache()
        return self.temperature_cached

    @property
    def weather_icon_url(self):
        if self.cache_expired():
            self.reload_cache()
        return self.weather_icon_url_cached
        
    def cache_expired(self):
        return (datetime.now() - self.cache_timestamp).total_seconds() > settings.WEATHER_EXPIRATION_SECONDS
    
    def reload_cache(self):
        weather_info = get_weather(self.latitude, self.longitude)
        if weather_info:
            self.city_cached = weather_info['city']
            self.weather_cached = weather_info['weather']
            self.time_zone_cached = weather_info['time_zone']
            self.temperature_cached = weather_info['temperature']
            self.weather_icon_url_cached = weather_info['weather_icon_url']
            self.cache_timestamp = datetime.now()
        else: 
            log.warn("WEATHER LOOKUP FAILED")

    def status_json(self):
        return {
            "username": self.username,
            "avatar_url": self.avatar.url if self.avatar else None,
            "city": self.city,
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "weather": self.weather,
            "temperature": self.temperature,
            "weather_icon_url": self.weather_icon_url,
            "pair_code": self.pair_code
        }
            
class Message(models.Model):
    text = models.TextField(max_length=400)
    emoto = models.ForeignKey(Emoto, null=True)
    author = models.ForeignKey(Profile, to_field="username")
    created_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        "Make sure to set some props before saving the first time"
        if not self.pk:
            now = datetime.utcnow()
            now.replace(microsecond=0)
            self.created_time = now
        super().save(*args, **kwargs)    
    
    def __str__(self):
        return "{}: {} with {}, ({})".format(self.author, self.text, self.emoto, 
                self.created_time.isoformat())

    def json(self):
        return {
            "id": self.id,
            "text": self.text, 
            "emoto": {
                "name": self.emoto.name,
                "url": self.emoto.image.url
            } if self.emoto else None,
            "author": self.author.username,
            "created_time": self.created_time.isoformat()            
        }

    class Meta:
        ordering = ["created_time"]

admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Emoto)
