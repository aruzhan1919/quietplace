# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Добро пожаловать.")
            return redirect("today")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def today_view(request):
    from books.models import Book
    from journal.models import Entry
    from datetime import datetime

    reading_books = Book.objects.filter(
        user=request.user,
        status=Book.STATUS_READING,
    )[:3]

    recent_entries = Entry.objects.filter(user=request.user)[:2]

    hour = datetime.now().hour
    if hour < 6:
        time_of_day = "тихая ночь"
    elif hour < 12:
        time_of_day = "утро"
    elif hour < 18:
        time_of_day = "день"
    elif hour < 23:
        time_of_day = "вечер"
    else:
        time_of_day = "поздний вечер"

    return render(
        request,
        "accounts/today.html",
        {
            "reading_books": reading_books,
            "recent_entries": recent_entries,
            "time_of_day": time_of_day,
        },
    )
