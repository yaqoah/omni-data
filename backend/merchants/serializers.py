from rest_framework import serializers
from .models import Merchant, Transaction

class MerchantSerializer(serializers.ModelSerializer):
    
    transaction_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Merchant
        fields = ['id', 'name', 'api_key', 'status', 'transaction_count', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_transaction_count(self, obj):
        return obj.transactions.count()


class TransactionSerializer(serializers.ModelSerializer):
    
    merchant_name = serializers.CharField(
        source='merchant.name',
        read_only=True,
    )
    
    class Meta:
        model = Transaction
        fields = ['id', 'merchant_name', 'amount', 'currency', 'status',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero."
            )
        return value