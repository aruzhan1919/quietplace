from django import forms
from .models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["text", "kind", "book"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 12,
                    "placeholder": "пиши о чём думаешь…",
                    "class": "entry-textarea",
                }
            ),
        }
        labels = {
            "text": "",
            "kind": "Тип",
            "book": "Связать с книгой",
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            from books.models import Book

            self.fields["book"].queryset = Book.objects.filter(user=user)
            self.fields["book"].required = False
            self.fields["book"].empty_label = "— не привязывать —"
