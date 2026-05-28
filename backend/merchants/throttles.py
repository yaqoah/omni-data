from rest_framework.throttling import UserRateThrottle
from middleware.tenant import get_current_merchant_id

class MerchantRateThrottle(UserRateThrottle):
    scope = 'merchant'
    rate = '60/minute'
    
    def get_cache_key(self, request, view):
        try:
            merchant_id = get_current_merchant_id()
            return f"throttle_{self.scope}_{merchant_id}"
        except:
            return None