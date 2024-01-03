from django.db import models

from appBase.models import Base
from appAuth.models import User


class Room(Base):
    name = models.CharField(max_length=256, null=True, unique=True)
    participants = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.name}"


class ChatHistory(Base):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE
    )
    message = models.CharField(
        max_length=255
    )
    to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="recipient"
    )

    def __str__(self):
        return f"{self.owner.name} to {self.to.name}"

    class Meta:
        ordering = ['-created_at']
