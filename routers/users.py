from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from sqlalchemy.sql.expression import desc
from starlette.responses import Response
from product_database.crud import *
from pydantic import BaseModel
import datetime
from product_database.serializer import *
from product_database.database import SessionLocal
from product_database.crud import *
from utils import *
from .pydanticmodels import *

router = APIRouter()

@router.post('/user/login/')
def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    try:
        UserObj=get_user_object(user.email,user.password)
        if not UserObj:
            raise HTTPException(status_code=401,detail="Bad username or password")
        access_token = Authorize.create_access_token(subject=UserObj.email,expires_time=datetime.timedelta(minutes=60))
        return {Statuses.status_code:Statuses.HTTP_200_OK,Statuses.status:Statuses.success,"access_token": access_token}
    except Exception as exc:
        if str(exc).strip()=="":
            return {Statuses.status_code:Statuses.HTTP_401_UNAUTHORIZED,Statuses.status:Statuses.failed,Statuses.description:"Bad Username or password"}
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}

@router.post("/user/register/") 
async def registerUser(data:RegisterUser):
    try:
        session=SessionLocal()
        user=User(**data.__dict__)
        session.add(user)
        session.flush()
        cart=Cart(user_id=user.user_id)
        session.add(cart)
        session.commit()
        return {Statuses.status_code:Statuses.HTTP_200_OK,Statuses.status:Statuses.success}
    except Exception as exc:
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}

@router.get("/user/search")
async def searchUser(email:str=None,start:int=0,limit:int=10):
    try:
        if email:
            objs=get_all_user_objects(email)
        else:
            objs=get_all_user_objects(email)
        return {Statuses.status_code:Statuses.HTTP_200_OK,Statuses.status:Statuses.success,Statuses.count:objs.count(),Statuses.data: SerilizerMixin.serialize(objs[start:limit:],many=True,unwanted_keys=["password"])}
    except Exception as exc:
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}

@router.get("/user/get/")
async def getUser(Authorize:AuthJWT=Depends()):
    Authorize.jwt_required()
    try:
        user=Authorize.get_jwt_subject()
        obj=get_user_object(username=user)
        if obj:
            return {Statuses.status_code:Statuses.HTTP_200_OK,Statuses.status:Statuses.success,Statuses.data: SerilizerMixin.serialize(obj,unwanted_keys=["password"])}
        return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:f"Authentication Failed"}
    except Exception as exc:
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}

@router.post("/user/cart/add/{product_id}")
async def addtoCart(product_id:int,Authorize:AuthJWT=Depends()):
    Authorize.jwt_required()
    try:
        user=Authorize.get_jwt_subject()
        obj=get_user_object(username=user)
        if obj:
            prodObj=get_product(product_id)
            if prodObj:
                session=SessionLocal()
                cart_id=obj.cart(session).cart_id
                if session.query(CartProduct).filter(CartProduct.cart_id==cart_id,CartProduct.product_id==product_id).count()==0:
                    cartProductObj=CartProduct(cart_id=cart_id,product_id=product_id)
                    session.add(cartProductObj)
                    session.commit()
                    cartProdutsObjs=session.query(CartProduct).filter(CartProduct.cart_id==cart_id)
                    session.close()
                    return {Statuses.status:Statuses.success,Statuses.status_code:Statuses.HTTP_200_OK,Statuses.count:cartProdutsObjs.count(),Statuses.data:SerilizerMixin.serialize(cartProdutsObjs,many=True),Statuses.description:"Product added succesfully to cart"}
                return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:"Product already in cart"}
            return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:f"product not found --> {product_id}"}
        return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:f"Authentication Failed"} 
    except Exception as exc:
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}