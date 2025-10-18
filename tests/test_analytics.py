import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_mumbai_last_month_earnings(monkeypatch: pytest.MonkeyPatch):
    async def mock_execute(self, query):
        class MockRow:
            def __init__(self):
                self._data = {'restaurant_name': 'Spice Heaven', 'total_earnings': 250.0}
            
            def __getitem__(self, key):
                return self._data[key]
            
            def keys(self):
                return self._data.keys()

        class Result:
            def fetchall(self):
                return [MockRow()]
                
            def mappings(self):
                return self
                
            def all(self):
                return self.fetchall()
                
        return Result()
    
    monkeypatch.setattr('sqlalchemy.ext.asyncio.AsyncSession.execute', mock_execute)    
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get('/api/v1/analytics/earnings/mumbai_last_month')
        assert response.status_code == 200
        data = response.json()
        assert data[0]['restaurant_name'] == 'Spice Heaven'
        assert data[0]['total_earnings'] == 250.0
    

@pytest.mark.asyncio
async def test_veg_earnings_bangalore(monkeypatch: pytest.MonkeyPatch):
    async def mock_execute(self, query):
        class MockRow:
            def __init__(self):
                self._data = {'total_earnings': 150.0}
            
            def __getitem__(self, key):
                return self._data[key]
            
            def keys(self):
                return self._data.keys()

        class Result:
            def fetchall(self):
                return [MockRow()]
                
            def mappings(self):
                return self
                
            def all(self):
                return self.fetchall()
                
        return Result()
    
    
    monkeypatch.setattr('sqlalchemy.ext.asyncio.AsyncSession.execute', mock_execute)

    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get('/api/v1/analytics/veg_earnings/bangalore')
        assert response.status_code == 200
        data = response.json()
        assert data[0]['total_earnings'] == 150.0