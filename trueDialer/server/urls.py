from django.urls import path

from .views import DetailView, LoginView, MarkSpamView, RegisterView, SearchView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("mark-spam/", MarkSpamView.as_view(), name="mark_spam"),
    path("search/<str:search_query>/", SearchView.as_view(), name="search"),
    path("detail/<int:id>/", DetailView.as_view(), name="detail"),
    path("login/", LoginView.as_view(), name="login"),
]
