from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_db
from sqlalchemy import text

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.customer import Customer
from app.models.order import Order
from app.models.payment import Payment
router = APIRouter()


@router.get("/earnings/mumbai_last_month")
async def mumbai_last_month_earnings(db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT r.restaurant_name, SUM(p.amount) AS total_earnings
        FROM orders o
        JOIN payments p ON o.transaction_id = p.transaction_id
        JOIN restaurants r ON o.restaurant_id = r.restaurant_id
        WHERE p.status = 'pass_status'
          AND r.area = 'Mumbai'
          AND o.created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
        GROUP BY r.restaurant_name;
    """)
    result = await db.execute(query)
    return [dict(row) for row in result.mappings().all()]


@router.get("/veg_earnings/bangalore")
async def veg_earnings_bangalore(db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT SUM(p.amount) AS total_earnings
        FROM orders o
        JOIN payments p ON o.transaction_id = p.transaction_id
        join restaurants r ON o.restaurant_id = r.restaurant_id
        WHERE p.status = 'pass_status'
        AND r.area = 'Bangalore'
		AND o.food_item IN ('veg_manchurian', 'veg_fried_rice');
    """)
    result = await db.execute(query)
    return [dict(row) for row in result.mappings().all()]

@router.get("/top-customers")
async def top_customers(db: AsyncSession = Depends(get_db)):
    """
    Get the top 3 customers with the most successful orders placed.
    Returns: [{ "customer_name": str, "order_count": int }]
    """

    # Join Customer -> Order -> Payment to count only successful payments
    stmt = (
        select(
            Customer.name.label("customer_name"),
            func.count(Order.order_id).label("order_count")
        )
        .join(Order, Customer.id == Order.customer_id)
        .join(Payment, Payment.transaction_id == Order.transaction_id)
        .where(Payment.status == "pass")
        .group_by(Customer.id)
        .order_by(desc(func.count(Order.order_id)))
        .limit(3)
    )

    result = await db.execute(stmt)   # ✅ Don't wrap in text()
    top_customers = result.mappings().all()

    return [{"customer_name": row["customer_name"], "order_count": row["order_count"]} for row in top_customers]

@router.get("/daily_revenue")
async def daily_revenue_past_week(db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT 
            DATE(o.created_at) AS order_date,
            r.area AS city,
            SUM(p.amount) AS total_revenue
        FROM orders o
        JOIN payments p ON o.transaction_id = p.transaction_id
        JOIN restaurants r ON o.restaurant_id = r.restaurant_id
        WHERE p.status = 'pass_status'
          AND o.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
        GROUP BY DATE(o.created_at), r.area
        ORDER BY order_date DESC, r.area;
    """)
    result = await db.execute(query)
    return [dict(row) for row in result.mappings().all()]

@router.get("/restaurant_summary/{restaurant_id}")
async def restaurant_order_summary(restaurant_id: str, db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT 
            o.food_item AS item_name,
            COUNT(o.order_id) AS total_orders
        FROM orders o
        JOIN payments p ON o.transaction_id = p.transaction_id
        WHERE o.restaurant_id = :restaurant_id
          AND p.status = 'pass_status'
        GROUP BY o.food_item
        ORDER BY total_orders DESC;
    """)
    result = await db.execute(query, {"restaurant_id": restaurant_id})
    return [dict(row) for row in result.mappings().all()]
