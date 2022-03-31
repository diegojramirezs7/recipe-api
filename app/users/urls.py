from django.urls import path

from .views import CreateAuthTokenView, CreateUserView

app_name = 'users'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateAuthTokenView.as_view(), name='token'),
]
