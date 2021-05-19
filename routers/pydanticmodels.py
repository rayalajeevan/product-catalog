from pydantic import BaseModel

class BasePostProduct(BaseModel):
    productName:str
    description:str
    price:float
    quantity:float
    categoryName:str
    category_id:int=None
    created_by:str=None
    
class BaseUpdateProduct(BaseModel):
    productName:str=None
    description:str=None
    price:float=None
    quantity:float=None
    categoryName:str=None
    category_id:int=None
    updated_on:str=None
    updated_by:str=None
    
class BasePostCategory(BaseModel):
    categoryName:str
    description:str
    created_by:str=None
    
class BaseupdateCategory(BaseModel):
    categoryName:str=None
    description:str=None
    updated_on:str=None
    updated_by:str=None
    
class UserLogin(BaseModel):
    email:str
    password:str
    
class RegisterUser(BaseModel):
    first_name:str
    last_name:str
    email:str
    password:str
    role:int
    date_of_birth:str
    