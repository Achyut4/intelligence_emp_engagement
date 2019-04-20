from wtforms import *


class AttendanceVO:
    attendanceId = IntegerField
    attendance_LoginId = IntegerField
    attendanceDate = StringField
    attendanceTime = StringField
