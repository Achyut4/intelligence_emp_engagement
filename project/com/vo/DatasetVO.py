from wtforms import *
from wtforms.fields.html5 import IntegerField

class DatasetVO:
    datasetId=IntegerField
    datasetName=StringField
    datasetPath=StringField
    dataset_DepartmentId=IntegerField
    dataset_LoginId=IntegerField
    datasetActiveStatus=StringField
