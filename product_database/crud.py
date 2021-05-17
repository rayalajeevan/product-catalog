from sqlalchemy.orm import session
from sqlalchemy.sql.functions import user
from .models import *
from .database import SessionLocal

def get_user_object(username=None,password=None,user_id=None):
    session=SessionLocal()
    if username and password==None:
        objs=session.query(User).filter(User.email==username)
    elif user_id:
        objs=session.query(User).filter(User.user_id==user_id)
    else:
        objs=session.query(User).filter(User.email==username,User.password==password)
    return False if objs.count()==0 else objs[0]

def get_all_user_objects(username=None):
    session=SessionLocal()
    if username and username.strip()!="":
        return session.query(User).filter(User.email.like("%"+username+"%"))
    session.close()
    return session.query(User).filter()

def get_category(category_id=None,category_name=None):
    session=SessionLocal()
    if category_id is not None:
        obj=session.query(Category).filter(Category.category_id==category_id)
    elif category_name is not None:
        obj=session.query(Category).filter(Category.categoryName==category_name)
    session.close()
    return False if obj.count()==0 else obj[0]

def create_category(category):
    session=SessionLocal()
    category=Category(**category.__dict__)
    session.add(category)
    session.commit()
    session.close()
    
def update_category(validated_data,category):
    session=SessionLocal()
    updated_validated_data=dict()
    for key,value in validated_data.__dict__.items():
        if value:
            updated_validated_data[key]=value
    updated_validated_data["updated_on"]=datetime.datetime.now()
    session.query(Category).filter(Category.category_id==category.category_id).update(updated_validated_data)
    session.commit()
    session.close()

def delete_category(category_ids):
    session=SessionLocal()
    session.query(Category).filter(Category.category_id.in_(category_ids)).delete()
    session.commit()
    session.close()
    
def get_product(product_id=None,product_name=None):
    session=SessionLocal()
    if product_id is not None:
        obj=session.query(Product).filter(Product.product_id==product_id)
    elif product_name is not None:
        obj=session.query(Product).filter(Product.productName==product_name)
    session.close()
    return False if obj.count()==0 else obj[0]

def create_product(product):
    session=SessionLocal()
    product=Product(**product.__dict__)
    session.add(product)
    session.commit()
    session.close()
    
def update_product(validated_data,product):
    session=SessionLocal()
    updated_validated_data=dict()
    for key,value in validated_data.__dict__.items():
        if value:
            updated_validated_data[key]=value
    updated_validated_data["updated_on"]=datetime.datetime.now()
    session.query(Product).filter(Product.product_id==product.product_id).update(updated_validated_data)
    session.commit()
    session.close()
    
def delete_product(product_ids):
    session=SessionLocal()
    session.query(Product).filter(Product.product_id.in_(product_ids)).delete()
    session.commit()
    session.close()
    
def get_all_products():
    session=SessionLocal()
    return session.query(Product).filter()

def get_all_prodcuts_for_fileUpload():
    objs=get_all_products()
    validatedObjects=list()
    data_list=dict()
    for obj in objs:
            data_list=dict()
            for y in ("product_id","productName","price","category_id","quantity","description","created_by","updated_by","created_on","updated_on"):
                if obj.__dict__[y]!=None:
                    if y in ["created_on","updated_on"]:
                        data_list[y]=obj.__dict__[y].strftime("%d-%m-%Y,%H:%M")
                    else:
                        data_list[y]=obj.__dict__[y]
                else:
                    data_list[y]="   --"
            validatedObjects.append(data_list)
    return validatedObjects
    
    
    
    
    
    
        