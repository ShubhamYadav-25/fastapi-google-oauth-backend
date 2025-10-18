### **README.md**
```markdown
# FastAPI Food Ordering Backend Prototype


## Overview
This is a **FastAPI-based backend** for a food ordering platform supporting Google OAuth login, async MySQL database, order flow, and analytical queries.


### Features
- Async SQLAlchemy models with Alembic migrations
- CRUD endpoints for Customers, Payments, Orders, Restaurants
- Google OAuth2 login + JWT authentication
- Order placement only if payment is successful
- Analytics endpoints using raw SQL
- Pagination and rate-limiting
- Seed data script to populate sample data
- Pytest tests covering OAuth login and analytics


---


## Setup


### 1. Clone Repository
```bash
git clone <repo_url>
cd fastapi_backend
```


### 2. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows
pip install -r requirements.txt
```


### 3. Configure Environment Variables
Copy `.env.example` to `.env` and set your MySQL credentials and Google OAuth info.


### 4. Run Alembic Migrations
```bash
alembic upgrade head
```


### 5. Seed Sample Data
```bash
python scripts/seed_data.py
```


### 6. Run the Backend
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`


---


## API Endpoints
- **Health Check:** `GET /healthz`
- **Customer Login (Google OAuth):** `POST /api/v1/customers/login`
- **Place Order:** `POST /api/v1/orders/place`
- **Analytics:**
- `GET /api/v1/analytics/earnings/mumbai_last_month`
- `GET /api/v1/analytics/veg_earnings/bangalore`
- **CRUD:** standard routes under `/api/v1/customers`, `/payments`, `/orders`, `/restaurants` (with pagination support)


---


## Testing
```bash
pytest tests/
```
This runs tests for OAuth login and analytics endpoints.


---


## Notes
- Google OAuth requires `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
- Use JWT tokens for authenticated endpoints
- Pagination params: `?skip=0&limit=10`
- Rate-limiting: simple IP-based in-memory limiter
```