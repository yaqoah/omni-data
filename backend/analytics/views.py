
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import logging

from middleware.tenant import get_current_merchant_id
from merchants.models import Transaction, Merchant
from .workers import submit_export_task, get_export_status

logger = logging.getLogger(__name__)


class RequestExportView(APIView):
    def post(self, request):
        try:
            merchant_id = get_current_merchant_id()
            export_format = request.data.get('format', 'csv')
            date_range = request.data.get('date_range')
            
            if export_format not in ['csv', 'json']:
                return Response(
                    {'error': 'Invalid format. Must be "csv" or "json".'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            task = submit_export_task(merchant_id)
            
            logger.info(
                "Export task submitted for merchant %s",
                merchant_id
            )
            
            return Response(
                {
                    'message': 'Export processing started',
                    'merchant_id': str(merchant_id),
                    'task_id': str(task.created_at.timestamp()),
                    'status_url': '/api/analytics/export-status/',
                    'estimated_wait_seconds': 5,
                    'format': export_format,
                },
                status=status.HTTP_202_ACCEPTED,
            )
        
        except Exception as e:
            logger.error(f"Export request failed: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ExportStatusView(APIView):
    
    def get(self, request):
        try:
            merchant_id = get_current_merchant_id()
            task_status = get_export_status(merchant_id)
            
            if not task_status:
                return Response(
                    {
                        'status': 'not_found',
                        'message': 'No active export task for this merchant',
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            
            return Response(task_status)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AnalyticsView(APIView):
    
    def get(self, request):
        try:
            merchant_id = get_current_merchant_id()
            merchant = Merchant.objects.get(id=merchant_id)
            all_txs = Transaction.objects.filter(merchant=merchant)
            
            total_volume = sum(
                tx.amount for tx in all_txs
            ) or 0
            
            statuses = {
                'total': all_txs.count(),
                'completed': all_txs.filter(status=Transaction.COMPLETED).count(),
                'pending': all_txs.filter(status=Transaction.PENDING).count(),
                'failed': all_txs.filter(status=Transaction.FAILED).count(),
                'refunded': all_txs.filter(status=Transaction.REFUNDED).count(),
            }
            
            average_tx = (
                total_volume / statuses['total'] 
                if statuses['total'] > 0 
                else 0
            )
            
            return Response({
                'merchant_id': str(merchant_id),
                'merchant_name': merchant.name,
                **statuses,
                'total_volume': str(total_volume),
                'average_transaction': f"{average_tx:.2f}",
                'currency': 'USD',
            })
        
        except Exception as e:
            logger.error(f"Analytics request failed: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )