from django import forms
from .models import Book
from .models import Review, Quote


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "cover", "status", "started_at", "finished_at"]
        widgets = {
            "started_at": forms.DateInput(attrs={"type": "date"}),
            "finished_at": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "title": "Название",
            "author": "Автор",
            "cover": "Обложка",
            "status": "Статус",
            "started_at": "Начал читать",
            "finished_at": "Закончил читать",
        }

    def clean(self):
        cleaned = super().clean()
        started = cleaned.get("started_at")
        finished = cleaned.get("finished_at")
        if started and finished and finished < started:
            raise forms.ValidationError(
                "Дата окончания не может быть раньше даты начала."
            )
        return cleaned


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text"]
        widgets = {
            "rating": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 10,
                    "placeholder": "опционально",
                }
            ),
            "text": forms.Textarea(
                attrs={
                    "rows": 12,
                    "placeholder": "что осталось после книги…",
                    "class": "entry-textarea",
                }
            ),
        }
        labels = {
            "rating": "Оценка (1–10)",
            "text": "",
        }


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "page"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "цитата или мысль по ходу чтения…",
                }
            ),
            "page": forms.TextInput(
                attrs={
                    "placeholder": "стр. (опц.)",
                }
            ),
        }
        labels = {
            "text": "",
            "page": "",
        }
