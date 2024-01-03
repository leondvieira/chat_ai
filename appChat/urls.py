from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.views.generic import TemplateView

from appChat.views import ChatHistoryViewSet, RoomViewSet


router = DefaultRouter()

router.register("chathistory", ChatHistoryViewSet, basename="chathistory")
router.register("room", RoomViewSet, basename="room")

urlpatterns = (
    path("", include(router.urls)),
    # DEBUG CHAT WEBSOCKET
    path("debug1/", TemplateView.as_view(template_name='appChat/chat_1.html')),
    path("debug2/", TemplateView.as_view(template_name='appChat/chat_2.html'))
)
