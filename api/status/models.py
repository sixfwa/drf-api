from django.db import models
from django.conf import settings


class Status(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="user"
    )

    content = models.TextField(verbose_name="content")

    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="Date Published"
    )
