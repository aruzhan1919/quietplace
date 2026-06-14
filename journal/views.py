from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Entry
from .forms import EntryForm
from django.views.generic import UpdateView, DeleteView


class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = "journal/entry_list.html"
    context_object_name = "entries"
    paginate_by = 30

    def get_queryset(self):
        qs = Entry.objects.filter(user=self.request.user)
        kind = self.request.GET.get("kind")
        if kind in ["story", "insight", "note"]:
            qs = qs.filter(kind=kind)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["current_kind"] = self.request.GET.get("kind", "")

        # цитаты подмешиваются как инсайты, если фильтр «всё» или «инсайты»
        from books.models import Quote

        if ctx["current_kind"] in ("", "insight"):
            quotes = Quote.objects.filter(book__user=self.request.user).select_related(
                "book"
            )
            ctx["quotes"] = quotes
        else:
            ctx["quotes"] = []

        # объединяем записи и цитаты в один поток, сортируем по дате
        combined = []
        for entry in ctx["entries"]:
            combined.append(("entry", entry, entry.created_at))
        for quote in ctx["quotes"]:
            combined.append(("quote", quote, quote.created_at))
        combined.sort(key=lambda x: x[2], reverse=True)

        ctx["feed"] = combined
        return ctx


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = "journal/entry_detail.html"

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = "journal/entry_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Записано.")
        return reverse_lazy("entry_list")


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = "journal/entry_form.html"

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        messages.success(self.request, "Изменения сохранены.")
        return reverse_lazy("entry_detail", kwargs={"pk": self.object.pk})


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = "journal/entry_confirm_delete.html"
    success_url = reverse_lazy("entry_list")

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.warning(self.request, "Запись удалена.")
        return super().form_valid(form)
