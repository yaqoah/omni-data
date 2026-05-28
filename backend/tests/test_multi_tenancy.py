import pytest
from django.test import Client
from decimal import Decimal
from uuid import uuid4


from merchants.models import Merchant, Transaction


@pytest.fixture()
def merchants():
    merchant_a = Merchant.objects.create(
        name='Merchant A',
        api_key='test_a_key_12345',
        status=Merchant.ACTIVE,
    )
    
    merchant_b = Merchant.objects.create(
        name='Merchant B',
        api_key='test_b_key_67890',
        status=Merchant.ACTIVE,
    )
    
    return {'a': merchant_a, 'b': merchant_b}


@pytest.fixture
def transactions(merchants):
    # Merchant A transactions
    tx_a1 = Transaction.objects.create(
        merchant=merchants['a'],
        amount=Decimal('100.00'),
        currency='USD',
        status=Transaction.COMPLETED,
    )
    
    tx_a2 = Transaction.objects.create(
        merchant=merchants['a'],
        amount=Decimal('200.00'),
        currency='USD',
        status=Transaction.PENDING,
    )
    
    # Merchant B transactions
    tx_b1 = Transaction.objects.create(
        merchant=merchants['b'],
        amount=Decimal('300.00'),
        currency='USD',
        status=Transaction.COMPLETED,
    )
    
    return {
        'a': [tx_a1, tx_a2],
        'b': [tx_b1],
    }


@pytest.mark.django_db
class TestMultiTenancyIsolation:
    
    def test_merchant_cannot_access_other_merchant_transaction(
        self,
        merchants,
        transactions,
    ):
        client = Client()
        
        # Merchant A tries to access Merchant B's transaction
        response = client.get(
            f'/api/merchants/transactions/{transactions["b"][0].id}/',
            HTTP_X_MERCHANT_ID=str(merchants['a'].id),
        )
        
        # MUST return 404, never 403, to prevent enumeration
        assert response.status_code == 404, (
            "Cross-tenant transaction access should return 404, "
            "not 403, to prevent resource enumeration."
        )
    
    def test_merchant_a_sees_only_own_transactions(
        self,
        merchants,
        transactions,
    ):
        client = Client()
        
        response = client.get(
            '/api/merchants/transactions/',
            HTTP_X_MERCHANT_ID=str(merchants['a'].id),
        )
        
        assert response.status_code == 200
        
        data = response.json()
        assert data['count'] == 2, (
            f"Merchant A should see 2 transactions, got {data['count']}"
        )
        
        # Verify all transactions belong to Merchant A
        for result in data['results']:
            assert result['merchant_name'] == 'Merchant A', (
                f"Merchant A leaked data: {result['merchant_name']}"
            )
    
    def test_missing_merchant_header_returns_400(self):
        client = Client()
        
        # Omit X-Merchant-ID header
        response = client.get('/api/merchants/transactions/')
        
        assert response.status_code == 400
        assert 'X-Merchant-ID' in response.json()['error']
    
    def test_invalid_merchant_id_format_rejected(self):
        client = Client()
        
        response = client.get(
            '/api/merchants/transactions/',
            HTTP_X_MERCHANT_ID='not-a-uuid',
        )
        
        assert response.status_code == 400
        assert 'Invalid' in response.json()['error']


@pytest.mark.django_db
class TestAnalyticsDataIsolation:
    
    def test_analytics_summary_shows_only_merchant_data(
        self,
        merchants,
        transactions,
    ):
        client = Client()
        
        # Merchant A's summary
        response_a = client.get(
            '/api/analytics/summary/',
            HTTP_X_MERCHANT_ID=str(merchants['a'].id),
        )
        
        assert response_a.status_code == 200
        assert response_a.json()['total'] == 2
        
        # Merchant B's summary
        response_b = client.get(
            '/api/analytics/summary/',
            HTTP_X_MERCHANT_ID=str(merchants['b'].id),
        )
        
        assert response_b.status_code == 200
        assert response_b.json()['total'] == 1