from wtforms import *


class StaffVO:
    registerId = IntegerField
    registerFirstName = StringField
    registerLastName = StringField
    registerContact = IntegerField
    registerEmail = StringField
    registerPassword = StringField
    registerGender = StringField
    registerAddress = StringField
    register_RoleId = IntegerField
    register_DepartmentId = IntegerField
    register_LoginId = IntegerField
    registerActiveStatus = StringField
    loginActiveStatus = StringField
