from django.db import models
from django.conf import settings


class Board(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    graph = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.user})"

    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"


class Access (models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.board}"

    class Meta:
        verbose_name = "Доступ"
        verbose_name_plural = "Доступы"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "board"],
                name="unique_user_board",
            )
        ]
