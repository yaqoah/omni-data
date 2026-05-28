import pytest
from django.test import Client
from rest_framework.status import HTTP_200_OK, HTTP_429_TOO_MANY_REQUESTS

from merchants.models import Merchant, Transaction


@pytest.fixture
def rate_limited_merchant():
    return Merchant.objects.create(
        name='Rate Test Merchant',
        api_key='test_rate_key',
    )


@pytest.mark.django_db
class TestRateLimiting:
    
    def test_rate_limit_enforced_at_60_requests_per_minute(
        self,
        rate_limited_merchant,
    ):
        client = Client()
        merchant_id = str(rate_limited_merchant.id)
        
        # Fire 60 successful requests
        for i in range(60):
            response = client.get(
                '/api/merchants/transactions/',
                HTTP_X_MERCHANT_ID=merchant_id,
            )
            
            assert response.status_code == HTTP_200_OK, (
                f"Request {i+1} should succeed, got {response.status_code}"
            )
        
        # 61st request should be throttled
        response = client.get(
            '/api/merchants/transactions/',
            HTTP_X_MERCHANT_ID=merchant_id,
        )
        
        assert response.status_code == HTTP_429_TOO_MANY_REQUESTS, (
            "Request 61 should be throttled (429), "
            f"got {response.status_code}"
        )
        
        assert 'available in' in response.json().get('detail', '').lower()