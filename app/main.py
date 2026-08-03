from fastapi import FastAPI
import models
from database import Base,engine
from routers import product_router
from routers import sale_router
from routers import user_router
from routers import customer_router
from routers import category_router
from routers import supplier_router
from routers import sale_item_router
from routers import payment_router
from routers import receipt_router
from models.category_model import Category
from models.supplier_model import Supplier
from models.product_model import Product
from models.customer_model import Customer
from models.user_model import User
from models.sale_model import Sale
from models.sale_item_model import SaleItem
from models.payment_model import Payment
from models.receipt_model import Receipt

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