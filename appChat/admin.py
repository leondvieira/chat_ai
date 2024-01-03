from django.contrib import admin
from appChat.models import ChatHistory, Room

admin.site.register(Room)
admin.site.register(ChatHistory)
