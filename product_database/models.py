from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime,Float
from .database import Base
import datetime

class Role(Base):
    __tablename__ = "role"
    role_id = Column("role_id",Integer, primary_key=True, index=True)
    role_name = Column("role_name",String(50))

class User(Base):
    __tablename__ = "USER"
    user_id=Column("user_id",Integer, primary_key=True, index=True)
    first_name=Column("first_name",String(250))
    last_name=Column("last_name",String(250))
    email=Column("email",String(250))
    password=Column("password",String(30))
    role=Column("role_id",Integer, ForeignKey('role.role_id'))
    created_by=Column(String(30))
    created_on=Column(DateTime(), default=datetime.datetime.now())
    updated_by=Column(String(30))
    updated_on=Column(DateTime())
    
    def cart(self,session):
        return session.query(Cart).filter(Cart.user_id==self.user_id)[0]
    
class Cart(Base):
    __tablename__="cart"
    cart_id=Column("cart_id",Integer, primary_key=True, index=True)
    user_id=Column("user_id",Integer, ForeignKey('USER.user_id'))
    created_by=Column(String(30))
    created_on=Column(DateTime(), default=datetime.datetime.now())
    updated_by=Column(String(30))
    updated_on=Column(DateTime())

class Category(Base):
    __tablename__= "category"
    category_id=Column(Integer, primary_key=True, index=True)
    categoryName=Column("category_name",String(30))
    description=Column(String(500))
    created_by=Column(String(30))
    created_on=Column(DateTime(), default=datetime.datetime.now())
    updated_by=Column(String(30))
    updated_on=Column(DateTime())
    
class Product(Base):
    __tablename__= "product"
    product_id=Column(Integer, primary_key=True, index=True)
    productName=Column("product_name",String(30))
    description=Column("description",String(500))
    price=Column("price",Float)
    quantity=Column("quantity",Integer)
    category_id=Column(Integer, ForeignKey('category.category_id'))
    created_by=Column(String(30))
    created_on=Column(DateTime(), default=datetime.datetime.now())
    updated_by=Column(String(30))
    updated_on=Column(DateTime())

class Order(Base):
    __tablename__="ORDER"
    order_id=Column(Integer, primary_key=True, index=True)
    address=Column(String(30))
    status=Column(String(30))
    user_id=Column(Integer, ForeignKey('User.user_id'))
    total_amount=Column(Float)
    created_by=Column(String(30))
    created_on=Column(DateTime(), default=datetime.datetime.now())
    updated_by=Column(String(30))
    updated_on=Column(DateTime())
    
class CartProduct(Base):
    __tablename__= "cart_product"
    id=Column(Integer, primary_key=True, index=True)
    cart_id=Column(Integer, ForeignKey('cart.cart_id'))
    product_id=Column(Integer, ForeignKey('product.product_id'))

class OrderProduct(Base):
    __tablename__= "order_product"
    id=Column(Integer, primary_key=True, index=True)
    order_id=Column(Integer, ForeignKey('ORDER.order_id'))
    product_id=Column(Integer, ForeignKey('product.product_id'))

class UserHistory(Base):
    __tablename__= "user_history"
    id=Column(Integer, primary_key=True, index=True)
    description=Column(String(30))
    user_id=Column(Integer, ForeignKey('User.user_id'))
    created_by=Column(String(30))
    created_on=Column(DateTime(), default=datetime.datetime.now())