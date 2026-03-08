from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Invoice


class InvoiceDetailView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    return Response({
      "id": invoice.id,
      "owner_id": invoice.owner_id,
      "amount": invoice.amount
    })
