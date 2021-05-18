from passlib.context import CryptContext

class Statuses:
    exception = "EXCEPTION"
    failed = "FAILED"
    success = "SUCCESS"
    status="STATUS"
    description="DESCRIPTION"
    data="DATA"
    count="COUNT"
    bearer="Bearer"
    type="type"
    status_code="STATUS_CODE"
    HTTP_200_OK=200
    HTTP_500_INTERNAL_SERVER_ERROR=500
    HTTP_BAD_REQUEST=400
    HTTP_404_NOT_FOUND=404
    HTTP_401_UNAUTHORIZED=401

class ProjectUtils:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    @staticmethod
    def is_authenticated(Authorize):
        try:
            Authorize.jwt_required()
            return True
        except Exception as exc:
            return False
        
    def verify_password(plain_password, hashed_password):
        return ProjectUtils.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(password):
        return ProjectUtils.pwd_context.hash(password)

    def authenticate_user(userObj, password):
        if not ProjectUtils.verify_password(password, userObj.password):
            return False
        return userObj
