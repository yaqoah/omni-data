from django.core.management.base import BaseCommand
from django.utils import timezone
from merchants.models import Merchant, Transaction
from decimal import Decimal
import random
from datetime import timedelta


class Command(BaseCommand):
    help = "Seed the database with test merchants and transactions"
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("📩 Starting database seed..."))

        # ============ MERCHANT A ============
        merchant_a, created_a = Merchant.objects.get_or_create(
            api_key='test_sk_merchant_a_12345',
            defaults={
                'name': 'Acme Corporation',
                'status': Merchant.ACTIVE,
            }
        )
        
        if created_a:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Created Merchant A: {merchant_a.name}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"⚡ Merchant A already exists: {merchant_a.name}")
            )
        
        # ============ MERCHANT B ============
        merchant_b, created_b = Merchant.objects.get_or_create(
            api_key='test_sk_merchant_b_67890',
            defaults={
                'name': 'Beta Industries',
                'status': Merchant.ACTIVE,
            }
        )
        
        if created_b:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Created Merchant B: {merchant_b.name}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"⏭️  Merchant B already exists: {merchant_b.name}")
            )
        
        # ============ SEED TRANSACTIONS ============
        self.seed_transactions_for_merchant(merchant_a)
        self.seed_transactions_for_merchant(merchant_b)
        
        self.stdout.write(
            self.style.SUCCESS("✅ Database seeding complete!")
        )
    
    def seed_transactions_for_merchant(self, merchant):
        
        statuses = [
            Transaction.COMPLETED,
            Transaction.COMPLETED,
            Transaction.COMPLETED,
            Transaction.PENDING,
            Transaction.FAILED,
        ]
        
        for i, status in enumerate(statuses):
            tx_exists = Transaction.objects.filter(
                merchant=merchant,
                amount=Decimal(f"{100 + i * 50}.00"),
            ).exists()
            
            if not tx_exists:
                created_at = timezone.now() - timedelta(hours=i*2)
                
                Transaction.objects.create(
                    merchant=merchant,
                    amount=Decimal(f"{100 + i * 50}.00"),
                    currency='USD',
                    status=status,
                    created_at=created_at,
                )
                
                self.stdout.write(
                    f"  → Created {status} transaction for {merchant.name}"
                )
        