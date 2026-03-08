class Invoice:
  def __init__(self, invoice_id, owner_id, amount):
    self.id = invoice_id
    self.owner_id = owner_id
    self.amount = amount


class InvoiceManager:
  @staticmethod
  def get(id):
    return Invoice(id, owner_id=42, amount=199)


Invoice.objects = InvoiceManager()
