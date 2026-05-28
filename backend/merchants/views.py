from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .throttles import MerchantRateThrottle
from django.db.models import Q
import logging

from middleware.tenant import get_current_merchant_id
from .models import Transaction, Merchant
from .serializers import TransactionSerializer

logger = logging.getLogger(__name__)


class TransactionPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ListTransactionsView(APIView):
    
    throttle_classes = [MerchantRateThrottle]
    
    def get(self, request):
        try:
            merchant_id = get_current_merchant_id()
            
            merchant = Merchant.objects.get(id=merchant_id)
            
            queryset = Transaction.objects.filter(merchant=merchant)
            
            status_filter = request.query_params.get('status')
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            currency_filter = request.query_params.get('currency')
            if currency_filter:
                queryset = queryset.filter(currency=currency_filter)
        
            paginator = TransactionPagination()
            paginated_queryset = paginator.paginate_queryset(
                queryset,
                request,
            )
            
            serializer = TransactionSerializer(
                paginated_queryset,
                many=True,
            )
            
            return paginator.get_paginated_response(serializer.data)
        
        except Merchant.DoesNotExist:
            logger.warning(
                f"Invalid merchant_id: {merchant_id}"
            )
            return Response(
                {'error': 'Merchant not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"Transaction list failed: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TransactionDetailView(APIView):
    
    throttle_classes = [MerchantRateThrottle]
    
    def get(self, request, tx_id):
        try:
            merchant_id = get_current_merchant_id()
            
            merchant = Merchant.objects.get(id=merchant_id)
            
            transaction = get_object_or_404(
                Transaction,
                id=tx_id,
                merchant=merchant,
            )
            
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        
        except Exception as e:
            # Return 404 for ANY error (prevents enumeration)
            logger.warning(f"Transaction detail access denied: {str(e)}")
            return Response(
                {'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )