from fastapi import APIRouter
from app.api.routes import customer, order,  analytics, payments, restaurant


router = APIRouter()


router.include_router(customer.router, prefix="/customers", tags=["Customers"])
router.include_router(payments.router, prefix="/payments", tags=["Payments"])
router.include_router(order.router, prefix="/orders", tags=["Orders"])
router.include_router(restaurant.router, prefix="/restaurants", tags=["Restaurants"])
router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])