import time
import logging
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

logger = logging.getLogger(__name__)

class PerformanceMetricsMiddleware(MiddlewareMixin):
    
    SLOW_QUERY_THRESHOLD_MS = 200
    
    def process_request(self, request):
        request._start_time = time.perf_counter()
    
    def process_response(self, request, response):
        if request.path in ['/health/', '/ready/']:
            return response
        
        if hasattr(request, '_start_time'):
            duration_sec = time.perf_counter() - request._start_time
            duration_ms = duration_sec * 1000
            
            query_count = 0
            if settings.DEBUG:
                from django.db import connection
                query_count = len(connection.queries)

            if duration_ms > self.SLOW_QUERY_THRESHOLD_MS:
                logger.warning(
                    f"[PERFORMANCE ALERT] Slow query detected on endpoint {request.path}\n"
                    f"  Duration: {duration_ms:.2f}ms\n"
                    f"  Method: {request.method}\n"
                    f"  Status: {response.status_code}\n"
                    f"  DB Queries: {query_count}"
                )
            
            logger.debug(
                f"API Request: {request.method} {request.path} - "
                f"{duration_ms:.2f}ms ({query_count} queries)"
            )
        
        return response