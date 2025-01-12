from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
