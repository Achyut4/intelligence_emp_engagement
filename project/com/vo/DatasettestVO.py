from wtforms import *


class DatasettestVO:
    datasetId = IntegerField
    datasetName = StringField
    datasetPath = StringField
    dataset_DepartmentId = IntegerField
    dataset_RegisterId = IntegerField
    datasetActiveStatus = IntegerField
