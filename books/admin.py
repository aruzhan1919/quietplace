from django.contrib import admin
from .models import Book, Review, Quote


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "user", "updated_at")
    list_filter = ("status",)
    search_fields = ("title", "author")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "rating", "updated_at")
    search_fields = ("book__title", "text")


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("book", "short_text", "page", "created_at")
    search_fields = ("text", "book__title")

    def short_text(self, obj):
        return obj.text[:60] + ("…" if len(obj.text) > 60 else "")

    short_text.short_description = "Текст"
