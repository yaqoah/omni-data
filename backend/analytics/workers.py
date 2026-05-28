import threading
import queue
import csv
import io
from datetime import datetime
from decimal import Decimal
from typing import Optional
import logging

from django.db import close_old_connections

logger = logging.getLogger(__name__)

_task_queue = queue.Queue()
_task_status = {} 


class TransactionExportTask:    
    def __init__(self, merchant_id: str, format: str = 'csv', 
                 date_range: Optional[tuple] = None):
        self.merchant_id = merchant_id
        self.format = format
        self.date_range = date_range
        self.created_at = datetime.utcnow()
        self.file_content = None
        self.error = None

    def execute(self):
        close_old_connections()

        try:
            logger.info(
                "Starting export task for merchant %s",
                self.merchant_id
            )

            _task_status[self.merchant_id] = {
                'status': 'processing',
                'rows': 0,
                'started_at': datetime.utcnow().isoformat(),
            }

            from merchants.models import Transaction
            from middleware.tenant import set_current_merchant_id

            set_current_merchant_id(self.merchant_id)

            transactions = Transaction.objects.all()
            
            if self.date_range:
                start_date, end_date = self.date_range
                transactions = transactions.filter(
                    created_at__gte=start_date,
                    created_at__lte=end_date,
                )
            
            transactions = transactions.select_related('merchant')
            
            csv_buffer = io.StringIO()
            writer = csv.DictWriter(
                csv_buffer,
                fieldnames=[
                    'id',
                    'amount',
                    'currency',
                    'status',
                    'created_at',
                    'merchant_name',
                ],
            )
            
            writer.writeheader()
            row_count = 0
            
            for tx in transactions.iterator(chunk_size=1000):
                writer.writerow({
                    'id': str(tx.id),
                    'amount': str(tx.amount),
                    'currency': tx.currency,
                    'status': tx.status,
                    'created_at': tx.created_at.isoformat(),
                    'merchant_name': tx.merchant.name,
                })
                row_count += 1
            
            self.file_content = csv_buffer.getvalue()

            _task_status[self.merchant_id] = {
                'status': 'complete',
                'rows': row_count,
                'file_size_kb': len(self.file_content) / 1024,
                'completed_at': datetime.utcnow().isoformat(),
            }
            
            logger.info(
            "Export complete: %s rows for %s",
            row_count,
            self.merchant_id
        )
        
        except Exception as e:
            logger.error(
                "Export failed for %s: %s",
                self.merchant_id,
                str(e),
                exc_info=True,
            )

        finally:
            close_old_connections()

def submit_export_task(merchant_id: str) -> TransactionExportTask:
    task = TransactionExportTask(merchant_id=merchant_id)
    
    worker_thread = threading.Thread(
        target=task.execute,
        daemon=False,
        name=f"export-{merchant_id[:8]}",
    )
    
    worker_thread.start()
    
    return task


def get_export_status(merchant_id: str) -> dict:
    return _task_status.get(merchant_id)