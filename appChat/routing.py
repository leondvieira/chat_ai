from django.urls import path
from appChat import consumers


websocket_urlpatterns = [
    path("ws/<str:room_name>/", consumers.SocketConsumer.as_asgi())
]
