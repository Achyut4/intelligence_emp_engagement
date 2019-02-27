from wtforms import *
from wtforms.fields.html5 import IntegerField

class DepartmentVO:

    departmentId=IntegerField
    departmentName=StringField
    departmentActiveStatus=StringField
