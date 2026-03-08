from django.urls import path

from accounts.views import ProfileView
from billing.views import InvoiceDetailView

urlpatterns = [
  path("api/profile", ProfileView.as_view()),
  path("api/invoices/<int:invoice_id>", InvoiceDetailView.as_view())
]
