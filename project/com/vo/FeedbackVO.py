from wtforms import *

class FeedbackVO:
    feedbackId = IntegerField
    feedbackRating = StringField
    feedbackDescription = StringField
    feedbackFrom_LoginId = IntegerField
    feedbackTo_LoginId = IntegerField
    feedbackDate = StringField
    feedbackTime = StringField
    feedbackActiveStatus = StringField