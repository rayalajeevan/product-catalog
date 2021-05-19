from app import app
from fastapi.testclient import TestClient
import random

client = TestClient(app)
headers={"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhcnZAZ21haWwuY29tIiwiaWF0IjoxNjIxNDE4ODIwLCJuYmYiOjE2MjE0MTg4MjAsImp0aSI6IjllODc2MjRlLTUxZTUtNGY3Yi1hNTkzLTA2YWYxOTIyNDhlYSIsImV4cCI6MTY1NzQxODgyMCwidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZSwicm9sZXMiOlsiQURNSU4iXX0.AGiL_9mW_O4dQDmmSmjoGWpJBU4WRJMHZ_fRZFOrwmo"}
def test_Incorrectlogin():
    response = client.post("/user/login/",json={"email":"arvsfsf@gmail.com","password":"arv@12345"})
    assert response.status_code == 401

def test_IncorrectloginSeondTestCase():
    response = client.post("/user/login/",json={"email":"arv@gmail.com","password":"arv@123456"})
    assert response.status_code == 401

def test_correct_login():
    response = client.post("/user/login/",json={"email":"arv@gmail.com","password":"arv@12345"})
    assert response.status_code == 200
    assert response.json().get("access_token")!=None
    
def test_getAllproducts():
    response = client.get("/api/product",headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(),dict)
    
def test_Succesfullregistiraion():
    registered_deatails={"first_name":"xyz","last_name":"Zyx","email":"xyz{int1}@gmail.com".format(int1=random.randint(100000,9000000)),"role":1,"password":"xyz@1234","date_of_birth":"1992-12-12"}
    response = client.post("/user/register/",json=registered_deatails)
    assert response.status_code == 200

def test_UserLAreadyExistForRegisteration():
    registered_deatails={"first_name":"xyz","last_name":"Zyx","email":"xyz@gmail.com".format(int1=random.randint(100000,9000000)),"role":1,"password":"xyz@1234","date_of_birth":"1992-12-12"}
    response = client.post("/user/register/",json=registered_deatails)
    assert response.status_code == 400

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
    response = client.post("/api/product",json=product,headers=headers)
    assert isinstance(response.json(),dict)
    assert response.status_code==200

def test_UnSuccesfullpostAProductFirstCase():
    product={"productName": "REddjhMIjhgjkfjgfjh TV{int1}".format(int1=random.randint(100000,100000000)),"description": "This is a  REDMI Mobile TV","price": "42350",
"quantity": "2500","categoryName": "REDMI456"}
    response = client.post("/api/product",json=product,headers=headers)
    assert isinstance(response.json(),dict)
    assert response.status_code==400

def test_UnsuccesfullPostProduct():
    product = {"productName": "REMI TV","description": "This is a  REDMI Mobile TV","price": "42350",
    "quantity": "2500"}
    response = client.post("/api/product",json=product,headers=headers)
    assert response.status_code == 422

def test_SuccesfullUpdateProduct():
    response = client.put("/api/product/6",json={"description":"This is a One plus mobile","categoryName":"MObiles"},headers=headers)
    assert response.status_code == 200

def test_UnSuccesfullUpdateProduct():
    response = client.put("/api/product/6",json={"description":"This is a One plus mobile","categoryName":"kjsfvk"},headers=headers)
    assert response.status_code == 400

def test_UnSuccesfullUpdateProductSecondCase():
    response = client.put("/api/product/645646",json={"description":"This is a One plus mobile","categoryName":"kjsfvk"},headers=headers)
    assert response.status_code == 400
    
def test_SuccsesfullpostCategory():
    data={"categoryName": "REDMI{int1}".format(int1=random.randint(100000,100000000)),"description": "This is Mobile Play category"}
    response=client.post("/api/category",json=data,headers=headers)
    assert response.status_code==200

def test_UnSuccsesfullpostCategory():
    data={"categoryName": "REDMI{int1}".format(int1=random.randint(100000,100000000))}
    response=client.post("/api/category",json=data)
    assert response.status_code==422

def test_SuccesfullUpdateCategory():
    data={"description": "This is Mobile Play category23445"}
    response=client.put("/api/category/9",json=data,headers=headers)
    assert response.status_code==200

def test_UnSuccesfullUpdateCategory():
    data={"description": "This is Mobile Play category23445"}
    response=client.put("/api/category/900",json=data,headers=headers)
    assert response.status_code==400

def test_UNSuccesfullDeleteCategory():
    response=client.delete("/api/category/122334",headers=headers)
    assert response.status_code==400

def test_SuccesfullExportToPdf():
    response=client.get("/api/products/exporttopdf",headers=headers)
    assert response.status_code==200

def test_SuccesfullExportToExcel():
    response=client.get("/api/products/exporttoexcel",headers=headers)
    assert response.status_code==200

def test_SuccesfullGetTheUser():
    response = client.get("/user/get/",headers=headers)
    assert isinstance(response.json(),dict)
    assert response.status_code==200
    
def test_TokenExpiered():
    response = client.get("/user/get/",headers={"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhcnZAZ21haWwuY29tIiwiaWF0IjoxNjIxNDA5Nzc3LCJuYmYiOjE2MjE0MDk3NzcsImp0aSI6IjJiY2FhNWMxLWY2ZjMtNDg2MS1iNGQyLWMyZjIyYzJmZDk1NCIsImV4cCI6MTYyMTQxMzM3NywidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZSwicm9sZXMiOlsiQURNSU4iXX0.hmGr5hL5t_bvDNHWcXQVm4tGN-KVSOAC6jJoD_Vhz1I"})
    assert isinstance(response.json(),dict)
    assert response.status_code==422

def test_SuccesfullAddIntoCart():
    response = client.post("/user/cart/add/40",headers=headers)
    assert isinstance(response.json(),dict)
    assert response.status_code==400
    
def test_UnsuccsfulladIntoCart():
    response = client.post("/user/cart/add/40",headers=headers)
    assert isinstance(response.json(),dict)
    assert response.status_code==400

def test_SeachUserFirstCase():
    response = client.get("/user/search/?email=&limit=10&start=0",headers=headers)
    assert response.status_code==200

def test_SeachUserSecondCase():
    response = client.get("/user/search/?limit=10&start=0",headers=headers)
    assert response.status_code==200

def test_GetDeleteUser():
    response = client.get("/user/get/",headers={"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzYmRmaGprc2hmakBnbWFpbC5jb20iLCJpYXQiOjE2MjE0MjExMDgsIm5iZiI6MTYyMTQyMTEwOCwianRpIjoiZGFkMWJmYmYtMTRhMC00YzE0LWJjNzQtYWYwMGM2YmUyNTRhIiwiZXhwIjoxNjUyOTU3MTA4LCJ0eXBlIjoiYWNjZXNzIiwiZnJlc2giOmZhbHNlLCJyb2xlcyI6WyJBRE1JTiJdfQ.0EFPAsstLO7lbBoB4jG5TyZRuUwY4ucXTK8xhjuiDok"})
    assert isinstance(response.json(),dict)
    assert response.status_code==400

def test_UnsuccsefullDeleteProduct():
    response = client.delete("/api/product/646747",headers=headers)
    assert response.status_code == 400
    