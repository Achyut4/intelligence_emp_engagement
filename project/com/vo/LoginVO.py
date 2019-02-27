from wtforms import *

class LoginVO:
    loginId = IntegerField
    loginEmail = StringField
    loginPassword = StringField
    loginActiveStatus = StringField
    loginRole = StringField