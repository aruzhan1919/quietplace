from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib import messages
from .models import Book
from .forms import BookForm


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"
    paginate_by = 30

    def get_queryset(self):
        qs = Book.objects.filter(user=self.request.user)
        status = self.request.GET.get("status")
        if status in ["wishlist", "reading", "finished"]:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["current_status"] = self.request.GET.get("status", "")
        return ctx


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "books/book_detail.html"

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        new_status = request.GET.get("set_status")
        if new_status in ["wishlist", "reading", "finished"]:
            self.object.status = new_status
            self.object.save(update_fields=["status", "updated_at"])
            from django.shortcuts import redirect

            return redirect("book_detail", pk=self.object.pk)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Книга добавлена.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("book_detail", kwargs={"pk": self.object.pk})


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("book_detail", kwargs={"pk": self.object.pk})


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = "books/book_confirm_delete.html"
    success_url = reverse_lazy("book_list")

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.warning(self.request, "Книга удалена.")
        return super().form_valid(form)


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Review, Quote
from .forms import ReviewForm, QuoteForm


def _get_user_book(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    if book.user != request.user:
        raise Http404
    return book


@login_required
def review_add(request, book_pk):
    book = _get_user_book(request, book_pk)

    if book.status != Book.STATUS_FINISHED:
        messages.warning(request, "Рецензию можно написать только после прочтения.")
        return redirect("book_detail", pk=book.pk)

    if hasattr(book, "review"):
        return redirect("review_edit", book_pk=book.pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()
            messages.success(request, "Рецензия сохранена.")
            return redirect("book_detail", pk=book.pk)
    else:
        form = ReviewForm()

    return render(
        request,
        "books/review_form.html",
        {
            "form": form,
            "book": book,
            "is_new": True,
        },
    )


@login_required
def review_edit(request, book_pk):
    book = _get_user_book(request, book_pk)
    review = get_object_or_404(Review, book=book)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Рецензия обновлена.")
            return redirect("book_detail", pk=book.pk)
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "books/review_form.html",
        {
            "form": form,
            "book": book,
            "is_new": False,
        },
    )


@login_required
def review_delete(request, book_pk):
    book = _get_user_book(request, book_pk)
    review = get_object_or_404(Review, book=book)

    if request.method == "POST":
        review.delete()
        messages.warning(request, "Рецензия удалена.")
        return redirect("book_detail", pk=book.pk)

    return render(
        request,
        "books/review_confirm_delete.html",
        {
            "book": book,
            "review": review,
        },
    )


@login_required
def quote_add(request, book_pk):
    book = _get_user_book(request, book_pk)

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.book = book
            quote.save()
            messages.success(request, "Цитата сохранена.")
            return redirect("book_detail", pk=book.pk)
    else:
        form = QuoteForm()

    return render(
        request,
        "books/quote_form.html",
        {
            "form": form,
            "book": book,
        },
    )


@login_required
def quote_delete(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    if quote.book.user != request.user:
        raise Http404

    book_pk = quote.book.pk
    if request.method == "POST":
        quote.delete()
        messages.warning(request, "Цитата удалена.")
        return redirect("book_detail", pk=book_pk)

    return render(
        request,
        "books/quote_confirm_delete.html",
        {
            "quote": quote,
        },
    )
