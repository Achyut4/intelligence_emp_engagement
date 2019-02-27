from wtforms import *


class RoleVO:
    roleId = IntegerField
    roleName = StringField
    roleActiveStatus = StringField
    role_DepartmentId = IntegerField