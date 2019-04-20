from wtforms import *

class TrackingVO:
    trackingId=IntegerField
    trackingPlace=StringField
    trackingTime=StringField
    tracking_DepartmentId=IntegerField
    tracking_RoleId=IntegerField
    tracking_LoginId=IntegerField