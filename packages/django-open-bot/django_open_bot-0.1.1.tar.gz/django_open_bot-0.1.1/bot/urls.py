from django.urls import path
from bot import views


urlpatterns = [
    path('webhook/', views.get_webhook, name='webhook'),
    path('webhook/<int:pk>/', views.telegram_webhook, name='telegram_webhook'),
]


