from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.db.models import QuerySet
from django.db import models
import threading
import logging

logger = logging.getLogger(__name__)

_thread_local = threading.local()


def get_current_merchant_id():
    merchant_id = getattr(_thread_local, 'merchant_id', None)
    if not merchant_id:
        raise RuntimeError(
            "Tenant context not set. "
            "Ensure TenantMiddleware is installed in MIDDLEWARE."
        )
    return merchant_id


def set_current_merchant_id(merchant_id):
    _thread_local.merchant_id = merchant_id


def clear_current_merchant_id():
    if hasattr(_thread_local, 'merchant_id'):
        delattr(_thread_local, 'merchant_id')


class TenantMiddleware(MiddlewareMixin):
    HEADER_NAME = 'HTTP_X_MERCHANT_ID'
    EXCLUDED_PATHS = ['/health/', '/docs/']
    
    def process_request(self, request):
        if any(request.path.startswith(path) for path in self.EXCLUDED_PATHS):
            return None
        
        merchant_id = request.META.get(self.HEADER_NAME)
        
        if not merchant_id:
            logger.warning(
                f"🚨 Missing tenant context for {request.method} {request.path} "
                f"from {request.META.get('REMOTE_ADDR')}"
            )
            return JsonResponse(
                {
                    'error': 'Missing X-Merchant-ID header',
                    'detail': (
                        'All requests must include X-Merchant-ID header '
                        'containing your merchant UUID.'
                    ),
                },
                status=400,
            )
        
        if not self._is_valid_uuid(merchant_id):
            logger.warning(
                f"🚨 Invalid merchant_id format: {merchant_id}"
            )
            return JsonResponse(
                {
                    'error': 'Invalid X-Merchant-ID format',
                    'detail': 'Merchant ID must be a valid UUID.',
                },
                status=400,
            )
        
        set_current_merchant_id(merchant_id)
        
        return None
    
    def process_response(self, request, response):
        clear_current_merchant_id()
        return response
    
    @staticmethod
    def _is_valid_uuid(val):
        import uuid
        try:
            uuid.UUID(str(val))
            return True
        except (ValueError, AttributeError):
            return False


class TenantQuerySet(QuerySet):
    
    def _clone(self):
        clone = super()._clone()
        
        if hasattr(self.model, 'merchant'):
            try:
                merchant_id = get_current_merchant_id()
                clone = clone.filter(merchant_id=merchant_id)
            except RuntimeError:
                pass
        
        return clone

class TenantManager(models.Manager):
    def get_queryset(self):
        return TenantQuerySet(self.model, using=self._db)

from django.shortcuts import get_object_or_404 as django_get_object_or_404

_original_get_object_or_404 = django_get_object_or_404

def get_object_or_404_tenant_safe(klass, *args, **kwargs):
    try:
        return _original_get_object_or_404(klass, *args, **kwargs)
    except Exception:
        from django.http import Http404
        raise Http404()

from django.db import models
import django.db.models as djmodels

original_manager = djmodels.Manager

djmodels.Manager = TenantManager