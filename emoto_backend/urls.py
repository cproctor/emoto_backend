"""emoto_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from emoto_backend import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/users/new/?$', views.signup, name="signup"),
    url(r'^api/v1/users/(?P<username>\w+)/status/?$', views.status, name="status"),
    url(r'^api/v1/users/(?P<username>\w+)/messages/?$', views.messages, name="messages"),
    url(r'^api/v1/users/(?P<username>\w+)/messages/new/?$', views.new_message, name="new_message"),
    url(r'^api/v1/users/(?P<username>\w+)/location', views.set_location, name="set_location"),
    url(r'^api/v1/users/(?P<username>\w+)/emoto', views.set_current_emoto, name="set_current_emoto"),
    url(r'^api/v1/users/(?P<username>\w+)/present', views.set_present, name="set_present"),
    url(r'^api/v1/users/(?P<username>\w+)/absent', views.set_absent, name="set_absent"),
    url(r'^api/v1/users/(?P<username>\w+)/pair/(?P<pair_code>\w+)/?$', views.pair, name="pair"),
    url(r'^api/v1/users/(?P<username>\w+)/unpair/?$', views.unpair, name="unpair"),
    url(r'^api/v1/emotos/new/?', views.new_emoto, name="new_emoto"),
    url(r'^api/v1/emotos/?', views.emotos, name="emotos")
]
