from wtforms import *

class RegisterVO:
    registerId=IntegerField
    registerFirstName=StringField
    registerLastName=StringField
    registerContact=IntegerField
    registerGender=StringField
    registerAddress=StringField
    register_DepartmentId=IntegerField
    register_RoleId=IntegerField
    register_LoginId=IntegerField
    registerPhoto=StringField
    registerActiveStatus=StringField