from app import app
from fastapi.testclient import TestClient
import random

client = TestClient(app)
token=None
def test_login():
    response = client.post("/user/login/",json={"email":"arvsfsf@gmail.com","password":"arv@12345"})
    assert response.status_code == 401

def test_correct_login():
    response = client.post("/user/login/",json={"email":"arv@gmail.com","password":"arv@12345"})
    assert response.status_code == 200
    assert response.json().get("access_token")!=None
    
def test_getAllproducts():
    response = client.get("/api/product")
    assert response.status_code == 200
    assert isinstance(response.json(),dict)
    
def test_Succesfullregistiraion():
    registered_deatails={"first_name":"xyz","last_name":"Zyx","email":"xyz{int1}@gmail.com".format(int1=random.randint(100000,9000000)),"role":1,"password":"xyz@1234","date_of_birth":"1992-12-12"}
    response = client.post("/user/register/",json=registered_deatails)
    assert response.status_code == 200

def test_UnSuccesfullregistiraion():
    registered_deatails={"first_name":"xyz","last_name":"Zyx","email":"xyz@gmail.com","password":"xyz@1234","date_of_birth":"1992-12-12"}
    response = client.post("/user/register/",json=registered_deatails)
    assert response.status_code==422
    registered_deatails.pop("first_name")
    response = client.post("/user/register/",json=registered_deatails)
    assert response.status_code==422
    registered_deatails.pop("last_name")
    response = client.post("/user/register/",json=registered_deatails)
    assert response.status_code==422
    registered_deatails.pop("email")
    response = client.post("/user/register/",json=registered_deatails)
    assert response.status_code==422

def test_SuccesfullpostAProduct():
    product={"productName": "REddjhMIjhgjkfjgfjh TV{int1}".format(int1=random.randint(100000,100000000)),"description": "This is a  REDMI Mobile TV","price": "42350",
"quantity": "2500","categoryName": "REDMI"}
    response = client.post("/api/product",json=product)
    assert isinstance(response.json(),dict)
    assert response.status_code==200

def test_UnsuccesfullPostProduct():
    product = {"productName": "REMI TV","description": "This is a  REDMI Mobile TV","price": "42350",
    "quantity": "2500"}
    response = client.post("/api/product",json=product)
    assert response.status_code == 422
    
def test_SuccsesfullpostCategory():
    data={"categoryName": "REDMI{int1}".format(int1=random.randint(100000,100000000)),"description": "This is Mobile Play category"}
    response=client.post("/api/category",json=data)
    assert response.status_code==200

def test_UnSuccsesfullpostCategory():
    data={"categoryName": "REDMI{int1}".format(int1=random.randint(100000,100000000))}
    response=client.post("/api/category",json=data)
    assert response.status_code==422

def test_SuccesfullUpdateCategory():
    data={"description": "This is Mobile Play category23445"}
    response=client.put("/api/category/9",json=data)
    assert response.status_code==200

def test_UnSuccesfullUpdateCategory():
    data={"description": "This is Mobile Play category23445"}
    response=client.put("/api/category/900",json=data)
    assert response.status_code==400

def test_UNSuccesfullDeleteCategory():
    response=client.delete("/api/category/122334")
    assert response.status_code==400

def test_SuccesfullExportToPdf():
    response=client.get("/api/products/exporttopdf")
    assert response.status_code==200

def test_SuccesfullExportToExcel():
    response=client.get("/api/products/exporttoexcel")
    assert response.status_code==200

def test_SuccesfullGetTheUser():
    response = client.post("/user/login/",json={"email":"arv@gmail.com","password":"arv@12345"})
    token=response.json().get("access_token")
    response = client.get("/user/get/",headers={"Authorization":"Bearer {token}".format(token=token)})
    assert isinstance(response.json(),dict)
    assert response.status_code==200

def test_SuccesfullAddIntoCart():
    response = client.post("/user/login/",json={"email":"arv@gmail.com","password":"arv@12345"})
    token=response.json().get("access_token")
    response = client.post("/user/cart/add/40",headers={"Authorization":"Bearer {token}".format(token=token)})
    assert isinstance(response.json(),dict)
    assert response.status_code==400
    
def test_UnsuccsfulladIntoCart():
    response = client.post("/user/login/",json={"email":"arv@gmail.com","password":"arv@12345"})
    token=response.json().get("access_token")
    response = client.post("/user/cart/add/40",headers={"Authorization":"Bearer {token}".format(token=token)})
    assert isinstance(response.json(),dict)
    assert response.status_code==400