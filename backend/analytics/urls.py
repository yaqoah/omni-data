from django.urls import path
from .views import (RequestExportView, ExportStatusView, AnalyticsView)

urlpatterns = [
    path('export/', RequestExportView.as_view(), name='request-export'),
    path('export-status/', ExportStatusView.as_view(), name='export-status'),
    path('summary/', AnalyticsView.as_view(), name='analytics-summary'),
]