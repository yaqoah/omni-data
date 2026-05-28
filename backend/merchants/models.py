from django.db import models
from django.utils import timezone
from uuid import uuid4


class Merchant(models.Model):   
    ACTIVE = 'active'
    SUSPENDED = 'suspended'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (SUSPENDED, 'Suspended'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        help_text="Unique identifier using UUID4 to prevent enumeration"
    )
    name = models.CharField(
        max_length=255,
        help_text="Business name of the merchant"
    )
    api_key = models.CharField(
        max_length=255,
        unique=True,
        help_text="Merchant-specific API key for webhooks"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=ACTIVE,
        help_text="Operational status of the merchant account"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Immutable creation timestamp for audit"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Automatically updated on model change"
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['api_key']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.id})"


class Transaction(models.Model):
    
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
        (REFUNDED, 'Refunded'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        help_text="Unique transaction identifier"
    )
    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        related_name='transactions',
        help_text="Parent merchant this transaction belongs to"
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="Transaction amount in smallest currency unit"
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        help_text="ISO 4217 currency code"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
        help_text="Current transaction lifecycle status"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Immutable transaction creation time"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last modification time"
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['merchant', '-created_at']),
            models.Index(fields=['merchant']),
        ]
    
    def __str__(self):
        return f"Transaction {self.id}: {self.amount} {self.currency} ({self.status})"
    