from fastapi import FastAPI
from app.database import Base, engine
from app.routers import product_router
from app.routers import sale_router
from app.routers import user_router
from app.routers import customer_router
from app.routers import category_router
from app.routers import supplier_router
from app.routers import sale_item_router
from app.routers import payment_router
from app.routers import receipt_router
from app.models.category_model import Category
from app.models.supplier_model import Supplier
from app.models.product_model import Product
from app.models.customer_model import Customer
from app.models.user_model import User
from app.models.sale_model import Sale
from app.models.sale_item_model import SaleItem
from app.models.payment_model import Payment
from app.models.receipt_model import Receipt

Base.metadata.create_all(bind=engine)



app = FastAPI(title ="Pos API",version="1")
app.include_router(sale_router.router) 
app.include_router(product_router.router) 
app.include_router(user_router.router)
app.include_router(customer_router.router)
app.include_router(category_router.router)
app.include_router(supplier_router.router)
app.include_router(sale_item_router.router)
app.include_router(payment_router.router)
app.include_router(receipt_router.router)


@app.get("/")
def root():
    return {"message": "Welcome to the POS API!"}   