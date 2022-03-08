"""
ASGI config for django_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import django
from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

django.setup()
from chat.schema import MyGraphqlWsConsumer


application = ProtocolTypeRouter({
    "http": get_asgi_application(), 
    "websocket": URLRouter([
        path("graphql/", MyGraphqlWsConsumer.as_asgi()),
    ])
})