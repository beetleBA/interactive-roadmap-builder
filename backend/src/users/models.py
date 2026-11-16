from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(blank=True)


class Stack(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Технология"
        verbose_name_plural = "Технологии"


class UserStack(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    stack = models.ForeignKey(Stack, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.stack}"

    class Meta:
        verbose_name = "Стек пользователя"
        verbose_name_plural = "Стек пользователей"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "stack"],
                name="unique_user_stack",
            )
        ]
