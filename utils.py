class Statuses:
    exception = "EXCEPTION"
    failed = "FAILED"
    success = "SUCCESS"
    status="STATUS"
    description="DESCRIPTION"
    data="DATA"
    count="COUNT"
    status_code="STATUS_CODE"
    HTTP_200_OK=200
    HTTP_500_INTERNAL_SERVER_ERROR=500
    HTTP_BAD_REQUEST=400
    HTTP_404_NOT_FOUND=404
    HTTP_401_UNAUTHORIZED=401

class ProjectUtils:
    @staticmethod
    def is_authenticated(Authorize):
        try:
            Authorize.jwt_required()
            return True
        except Exception as exc:
            return False