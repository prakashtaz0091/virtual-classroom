from django.db import models
import uuid

PAYMENT_STATUS = (
    ('initiated', 'Initiated'),
    ('success', 'Success'),
    ('failed', 'Failed'),
)


class EsewaTransaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notes = models.ForeignKey('main.Note', on_delete=models.CASCADE, null=True, blank=True, related_name='esewa_transactions')
    initiater = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='esewa_transactions')
    receiver = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='received_esewa_transactions')
    status = models.CharField(max_length=50, choices=PAYMENT_STATUS, default='initiated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.transaction_id}"