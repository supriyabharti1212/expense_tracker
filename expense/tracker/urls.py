from django.urls import path
from .views import TransactionAPIView

urlpatterns = [
    path('transactions/', TransactionAPIView.as_view(), name='transaction-api'),
]
