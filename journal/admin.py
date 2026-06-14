from django.contrib import admin
from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("preview", "kind", "user", "book", "created_at")
    list_filter = ("kind",)
    search_fields = ("text",)
    readonly_fields = ("created_at", "updated_at")
