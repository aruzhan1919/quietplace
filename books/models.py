from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    STATUS_WISHLIST = "wishlist"
    STATUS_READING = "reading"
    STATUS_FINISHED = "finished"

    STATUS_CHOICES = [
        (STATUS_WISHLIST, "Хочу прочитать"),
        (STATUS_READING, "Читаю"),
        (STATUS_FINISHED, "Прочитано"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="books"
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    author = models.CharField(max_length=255, blank=True, verbose_name="Автор")
    cover = models.ImageField(
        upload_to="covers/", blank=True, null=True, verbose_name="Обложка"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_WISHLIST,
        verbose_name="Статус",
    )
    started_at = models.DateField(null=True, blank=True, verbose_name="Начал читать")
    finished_at = models.DateField(
        null=True, blank=True, verbose_name="Закончил читать"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    @property
    def status_label(self):
        return dict(self.STATUS_CHOICES).get(self.status, "")

    @property
    def initials(self):
        if self.author:
            parts = self.author.split()
            if len(parts) >= 2:
                return (parts[0][0] + parts[1][0]).upper()
            return parts[0][:2].upper()
        return self.title[:2].upper() if self.title else "?"

    @property
    def placeholder_color(self):
        palette = ["#4A6E58", "#7390A3", "#B8704A", "#8B7355", "#6E5A8C"]
        return palette[self.id % len(palette)] if self.id else palette[0]


class Review(models.Model):
    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        related_name="review",
        verbose_name="Книга",
    )
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Оценка (1–10)",
        help_text="Можно оставить пустым — оценка опциональна.",
    )
    text = models.TextField(verbose_name="Текст рецензии")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"

    def __str__(self):
        return f"Рецензия на «{self.book.title}»"


class Quote(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="quotes",
        verbose_name="Книга",
    )
    text = models.TextField(verbose_name="Цитата или мысль")
    page = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Страница",
        help_text="Опционально. Можно текстом: «гл. 3» и т.п.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"

    def __str__(self):
        return self.text[:60]
