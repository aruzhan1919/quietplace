from django.db import models
from django.conf import settings
from django.urls import reverse


class Entry(models.Model):
    KIND_NOTE = "note"
    KIND_STORY = "story"
    KIND_INSIGHT = "insight"

    KIND_CHOICES = [
        (KIND_NOTE, "Запись"),
        (KIND_STORY, "История"),
        (KIND_INSIGHT, "Инсайт"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="entries"
    )
    kind = models.CharField(
        max_length=10, choices=KIND_CHOICES, default=KIND_NOTE, verbose_name="Тип"
    )
    text = models.TextField(verbose_name="Текст")
    book = models.ForeignKey(
        "books.Book",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entries",
        verbose_name="Книга",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return self.preview

    @property
    def preview(self):
        text = self.text.strip()
        if len(text) <= 60:
            return text
        return text[:60].rsplit(" ", 1)[0] + "…"

    @property
    def first_line(self):
        for line in self.text.split("\n"):
            line = line.strip()
            if line:
                return line
        return ""

    @property
    def kind_label(self):
        return dict(self.KIND_CHOICES).get(self.kind, "")

    def get_absolute_url(self):
        return reverse("entry_detail", kwargs={"pk": self.pk})
