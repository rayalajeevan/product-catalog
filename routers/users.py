from fastapi import APIRouter, Depends,HTTPException,Response, status
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
def login(response:Response,user: UserLogin, Authorize: AuthJWT = Depends()):
    try:
        session=SessionLocal()
        UserObj=get_user_object(user.email)
        if UserObj:
            if ProjectUtils.authenticate_user(UserObj,user.password):
                access_token = Authorize.create_access_token(subject=UserObj.email,expires_time=datetime.timedelta(days=365),user_claims={"roles":[UserObj.role_name(session).role_name]})
                session.close()
                response.status_code=status.HTTP_200_OK
                return {Statuses.status_code:Statuses.HTTP_200_OK,Statuses.status:Statuses.success,"access_token": access_token,Statuses.type:Statuses.bearer}
            else:
                raise HTTPException(status_code=401,detail="Bad username or password")
        raise HTTPException(status_code=401,detail="Bad username or password")
    except Exception as exc:
        if str(exc).strip()=="":
            raise HTTPException(status_code=401,detail="Bad username or password")
        ProjectUtils.print_log_msg(exc,ProjectUtils.EXCEPTION)
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}

@router.post("/user/register/")
async def registerUser(data:RegisterUser,response:Response):
    try:
        if not get_user_object(username=data.email):
            session=SessionLocal()
            data.password=ProjectUtils.get_password_hash(data.password)
            user=User(**data.__dict__)
            session.add(user)
            session.flush()
            cart=Cart(user_id=user.user_id)
            session.add(cart)
            session.commit()
            return {Statuses.status_code:Statuses.HTTP_200_OK,Statuses.status:Statuses.success}
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:"Email already Exists"}
    except Exception as exc:
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ProjectUtils.print_log_msg(exc,ProjectUtils.EXCEPTION)
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}

@router.get("/user/search")
async def searchUser(response:Response,email:str=None,start:int=0,limit:int=10,Authorize:AuthJWT=Depends()):
    Authorize.jwt_required()
    try:
        if str(email)==str(None):
            objs=get_all_user_objects(email)
        else:
            objs=get_all_user_objects(email)
        return {Statuses.status_code:Statuses.HTTP_200_OK,Statuses.status:Statuses.success,Statuses.count:objs.count(),Statuses.data: SerilizerMixin.serialize(objs[start:limit:],many=True,unwanted_keys=["password"],function_keys={"date_of_birth":SerilizerMixin.parseDOb})}
    except Exception as exc:
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ProjectUtils.print_log_msg(exc,ProjectUtils.EXCEPTION)
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}

@router.get("/user/get/")
async def getUser(response:Response,Authorize:AuthJWT=Depends()):
    Authorize.jwt_required()
    try:
        user=Authorize.get_jwt_subject()
        obj=get_user_object(username=user)
        if obj:
            return {Statuses.status_code:Statuses.HTTP_200_OK,Statuses.status:Statuses.success,Statuses.data: SerilizerMixin.serialize(obj,unwanted_keys=["password"],function_keys={"date_of_birth":SerilizerMixin.parseDOb})}
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:f"Authentication Failed"}
    except Exception as exc:
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ProjectUtils.print_log_msg(exc,ProjectUtils.EXCEPTION)
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}

@router.post("/user/cart/add/{product_id}")
async def addtoCart(product_id:int,response:Response,Authorize:AuthJWT=Depends()):
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
                response.status_code=status.HTTP_400_BAD_REQUEST
                return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:"Product already in cart"}
            response.status_code=status.HTTP_400_BAD_REQUEST
            return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:f"product not found --> {product_id}"}
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:f"Authentication Failed"} 
    except Exception as exc:
        ProjectUtils.print_log_msg(exc,ProjectUtils.EXCEPTION)
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}