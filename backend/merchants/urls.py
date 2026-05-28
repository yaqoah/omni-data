from django.urls import path
from .views import ListTransactionsView, TransactionDetailView

urlpatterns = [
    path('transactions/', ListTransactionsView.as_view(), 
         name='list-transactions'),
    path('transactions/<uuid:tx_id>/', TransactionDetailView.as_view(),
         name='transaction-detail'),
]