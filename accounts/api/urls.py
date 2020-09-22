from django.urls import path

from .views import AccountCreation,LoginView

urlpatterns = [
    path('registration/', AccountCreation.as_view()),
    path('login/',LoginView.as_view())
]
