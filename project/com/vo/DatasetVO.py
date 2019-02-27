from wtforms import *
from wtforms.fields.html5 import IntegerField

class DatasetVO:
    datasetId=IntegerField
    datasetName=StringField
    datasetPath=StringField
    datasetDescription=StringField
    datasetActiveStatus=StringField
