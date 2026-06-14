from django.urls import path
from . import views

urlpatterns = [
    path("", views.BookListView.as_view(), name="book_list"),
    path("add/", views.BookCreateView.as_view(), name="book_add"),
    path("<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("<int:pk>/edit/", views.BookUpdateView.as_view(), name="book_edit"),
    path("<int:pk>/delete/", views.BookDeleteView.as_view(), name="book_delete"),
    # рецензии
    path("<int:book_pk>/review/add/", views.review_add, name="review_add"),
    path("<int:book_pk>/review/edit/", views.review_edit, name="review_edit"),
    path("<int:book_pk>/review/delete/", views.review_delete, name="review_delete"),
    # цитаты
    path("<int:book_pk>/quote/add/", views.quote_add, name="quote_add"),
    path("quote/<int:pk>/delete/", views.quote_delete, name="quote_delete"),
]
