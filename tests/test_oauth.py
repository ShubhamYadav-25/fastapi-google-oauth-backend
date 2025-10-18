import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_google_login(monkeypatch):
    async def mock_get_google_user_info(token):
        print(f"Mock get_google_user_info called with token: {token}")
        return {'sub': 'mockuser123', 'name': 'Test User', 'email': 'test@example.com'}

    async def mock_get_customer(db, google_id):
        print(f"Mock get_customer called with google_id: {google_id}")
        class User:
            id = 'user123'
            name = 'Test User'
            google_id = 'mockuser123'
            age = None
        return User()

    def mock_create_access_token(subject, expires_delta=None):
        print(f"Mock create_access_token called with subject: {subject}")
        return 'mock_access_token'

    def mock_create_refresh_token(subject):
        print(f"Mock create_refresh_token called with subject: {subject}")
        return 'mock_refresh_token'

    # We need to mock the functions in the locations where they're imported
    monkeypatch.setattr('app.auth.google_oauth.get_google_user_info', mock_get_google_user_info)
    monkeypatch.setattr('app.api.routes.customer.get_google_user_info', mock_get_google_user_info)  # Used directly in the route
    monkeypatch.setattr('app.schemas.customer_crud.get_customer_by_google_id', mock_get_customer)
    monkeypatch.setattr('app.auth.jwt_handler.create_access_token', mock_create_access_token)
    monkeypatch.setattr('app.auth.jwt_handler.create_refresh_token', mock_create_refresh_token)
    
    
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post('/api/v1/customers/login', json={'token': 'fake-token'})
        assert response.status_code == 200
        data = response.json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['token_type'] == 'bearer'