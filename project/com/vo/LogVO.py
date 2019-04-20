from wtforms import *


class LogVO:
    logId=IntegerField
    logDate=StringField
    logTime=StringField
    log_LoginId=IntegerField
    log_DepartmentId=IntegerField