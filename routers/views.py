from product_database.models import *
from product_database.database import *
from product_database.serializer import *
from product_database.crud import *
from fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends,Response, status
from utils import *
from product_database.pdfmaker import PdfMaker,ExcelMaker
from starlette.responses import FileResponse
from .pydanticmodels import *

router = APIRouter()

@router.post("/api/category")
def postCategory(category:BasePostCategory,response:Response,Authorze:AuthJWT=Depends()):
    Authorze.jwt_required()
    try:
        if not get_category(category_name=category.categoryName):
            create_category(category)
            return {Statuses.status_code:Statuses.HTTP_200_OK,Statuses.status:Statuses.success}
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:"Category already exists"}
    except Exception as exc:
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ProjectUtils.print_log_msg(exc,ProjectUtils.EXCEPTION)
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}

@router.put("/api/category/{category_id}")
def updateCategory(category_id:int,category:BaseupdateCategory,response:Response,Authorze:AuthJWT=Depends()):
    Authorze.jwt_required()
    try:
        cateObj=get_category(category_id=category_id)
        if cateObj:
            update_category(category,cateObj)
            return {Statuses.status_code:Statuses.HTTP_200_OK,Statuses.status:Statuses.success}
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:"Category Not Found"}
    except Exception as exc:
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ProjectUtils.print_log_msg(exc,ProjectUtils.EXCEPTION)
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}

@router.delete("/api/category/{category_id}")
def deleteCategory(category_id:int,response:Response,Authorze:AuthJWT=Depends()):
    Authorze.jwt_required()
    try:
        cateObj=get_category(category_id=category_id)
        if cateObj:
            delete_category([category_id])
            return {Statuses.status_code:Statuses.HTTP_200_OK,Statuses.status:Statuses.success}
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:"Category Not Found"}
    except Exception as exc:
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ProjectUtils.print_log_msg(exc,ProjectUtils.EXCEPTION)
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}

@router.get("/api/product")
def getAllproducts(response:Response,Authorze:AuthJWT=Depends()):
    Authorze.jwt_required()
    try:
        objs=get_all_products()
        return {Statuses.status_code:Statuses.HTTP_200_OK,Statuses.status:Statuses.success,Statuses.count:objs.count(),Statuses.data: SerilizerMixin.serialize(objs,many=True),} 
    except Exception as exc:
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ProjectUtils.print_log_msg(exc,ProjectUtils.EXCEPTION)
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}
  
@router.post("/api/product")
async def postProduct(product:BasePostProduct,response:Response,Authorze:AuthJWT=Depends()):
    Authorze.jwt_required()
    try:
        if not get_product(product_name=product.productName):
            cateObj=get_category(category_name=product.categoryName)
            if cateObj:
                product.category_id=cateObj.category_id
                del product.categoryName
                create_product(product)
                return {Statuses.status_code:Statuses.HTTP_200_OK,Statuses.status:Statuses.success}
            response.status_code=status.HTTP_400_BAD_REQUEST
            return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:"Category Not Found"}
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:"Product already exists"}
    except Exception as exc:
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ProjectUtils.print_log_msg(exc,ProjectUtils.EXCEPTION)
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}

@router.put("/api/product/{product_id}")
def updateProduct(product:BaseUpdateProduct,product_id:int,response:Response,Authorze:AuthJWT=Depends()):
    Authorze.jwt_required()
    try:
        prodObj=get_product(product_id=product_id)
        if prodObj:
            if product.categoryName!=None:
                cateObj=get_category(category_name=product.categoryName)
                if cateObj:
                    product.category_id=cateObj.category_id
                else:
                    response.status_code=status.HTTP_400_BAD_REQUEST
                    return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:"Category Not Found"}
            del product.categoryName
            update_product(product,prodObj)
            return {Statuses.status_code:Statuses.HTTP_200_OK,Statuses.status:Statuses.success}
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:f"Product not found {product_id}"}
    except Exception as exc:
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ProjectUtils.print_log_msg(exc,ProjectUtils.EXCEPTION)
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}

@router.delete("/api/product/{product_id}")
def deleteProduct(product_id:int,response:Response,Authorze:AuthJWT=Depends()):
    Authorze.jwt_required()
    try:
        if get_product(product_id=product_id):
            delete_product([product_id,])
            return {Statuses.status_code:Statuses.HTTP_200_OK,Statuses.status:Statuses.success}
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {Statuses.status_code:Statuses.HTTP_BAD_REQUEST,Statuses.status:Statuses.failed,Statuses.description:f"Product not found {product_id}"}
    except Exception as exc:
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ProjectUtils.print_log_msg(exc,ProjectUtils.EXCEPTION)
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}

@router.get("/api/products/exporttopdf")
def productsExportToPdf(response:Response,Authorze:AuthJWT=Depends()):
    Authorze.jwt_required()
    try:
        pdf=PdfMaker(format='A4')
        pdf.set_title("Products List")
        pdf.add_page()
        validatedObjects=get_all_prodcuts_for_fileUpload()
        pdf.makeData(validatedObjects)
        pdf.output("productslist.pdf")
        return FileResponse("productslist.pdf", media_type='application/octet-stream',filename="productslist.pdf")
    except Exception as exc:
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ProjectUtils.print_log_msg(exc,ProjectUtils.EXCEPTION)
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}

@router.get("/api/products/exporttoexcel")
def productsExportToExcel(response:Response,Authorze:AuthJWT=Depends()):
    Authorze.jwt_required()
    try:
        validatedObjects=get_all_prodcuts_for_fileUpload()
        ExcelMaker().makeExcelSheet(validatedObjects)
        return FileResponse("productslist.xls", media_type='application/octet-stream',filename="productslist.xls")
    except Exception as exc:
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ProjectUtils.print_log_msg(exc,ProjectUtils.EXCEPTION)
        return {Statuses.status_code:Statuses.HTTP_500_INTERNAL_SERVER_ERROR,Statuses.status:Statuses.exception,Statuses.description:str(exc)}
        
        




