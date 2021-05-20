from passlib.context import CryptContext
import logging
from logging.handlers import TimedRotatingFileHandler
from settings.base import *
import datetime
import os
import sys

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
    INFO="INFO"
    DEBUG="DEBUG"
    WARNING="WARNING"
    EXCEPTION="EXCEPTION"
    CRITICAL="CRITICAL"
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")    
    def verify_password(plain_password, hashed_password):
        return ProjectUtils.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(password):
        return ProjectUtils.pwd_context.hash(password)

    def authenticate_user(userObj, password):
        if not ProjectUtils.verify_password(password, userObj.password):
            return False
        return userObj
    @staticmethod
    def print_log_msg(message,info="INFO",logger="fast-api-logger"):
        if logger=="fast-api-logger":
            log=logging.getLogger("fast-api-logger")
        else:
            log=logging.getLogger("fast-api-server-logger")
        {
            ProjectUtils.INFO:lambda msg:log.info(msg),
            ProjectUtils.DEBUG:lambda msg:log.debug(msg),
            ProjectUtils.EXCEPTION:lambda msg:log.exception(msg),
            ProjectUtils.WARNING:lambda msg:log.warning(msg),
            ProjectUtils.CRITICAL:lambda msg:log.critical(msg),
        }[info](message)
    
    @staticmethod
    def makePath(path):
        if not os.path.exists(path):
            os.makedirs(path)

class Logg():
    def logSetup (self):
        ProjectUtils.makePath(LOG_FILE_PATH)
        logger=logging.getLogger("fast-api-logger")
        logger2=logging.getLogger("fast-api-server-logger")
        logger2.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%m-%d-%y %H:%M:%S')
        fh = TimedRotatingFileHandler(LOG_FILE_PATH+r"\\server.log", when='D', interval=1,backupCount=45)
        fh.namer=lambda name:name.replace("server.log","").replace(".","")+"_server.log"
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        fh2 = TimedRotatingFileHandler(LOG_FILE_PATH+r"\\application.log", when='D', interval=1,backupCount=45)
        fh2.namer=lambda name:name.replace("application.log","").replace(".","")+"_application.log"
        fh2.setFormatter(formatter)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        logger2.addHandler(fh2)
        return logger
