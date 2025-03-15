from django.urls import path
from .views import PaymentTransactionCreateView, PaymentTransactionListView

urlpatterns = [
    path('transactions/', PaymentTransactionCreateView.as_view(), name='create-transaction'),
    path('transactions/history/', PaymentTransactionListView.as_view(), name='transaction-history'),
]
