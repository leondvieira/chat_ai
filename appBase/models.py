from django.db import models


class Base(models.Model):
    is_active = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    class Meta:
        abstract = True
