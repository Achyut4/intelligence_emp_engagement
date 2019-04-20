from project.com.dao import *


class AttendanceDAO:
    def insertAttendance(self, attendanceVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "INSERT INTO attendancemaster(attendance_LoginId,attendanceDate,attendanceTime,attendanceStatus,attendanceActiveStatus) VALUES ('" + attendanceVO.attendance_LoginId + "','" + attendanceVO.attendanceDate + "','" + attendanceVO.attendanceTime + "','" + attendanceVO.attendanceStatus + "','"+attendanceVO.attendanceActiveStatus+"')"
        )
        connection.commit()
        cursor1.close()
        connection.close()

    def searchAttendance(self, attendanceVO):
        connection=con_db()
        cursor1=connection.cursor()
        cursor1.execute(
            "SELECT * FROM (((registermaster INNER JOIN attendancemaster ON attendancemaster.attendance_LoginId=registermaster.register_LoginId) INNER JOIN departmentmaster ON registermaster.register_DepartmentId = departmentmaster.departmentId) INNER JOIN rolemaster ON registermaster.register_RoleId=rolemaster.roleId) WHERE attendanceStatus='"+attendanceVO.attendanceStatus+"' AND attendanceDate='"+attendanceVO.attendanceDate+"'"
        )
        attendanceDict=cursor1.fetchall()
        cursor1.close()
        connection.close()
        return attendanceDict

    def searchUserAttendance(self,attendanceVO):
        connection=con_db()
        cursor1=connection.cursor()
        cursor1.execute(
            "SELECT * FROM attendancemaster WHERE attendance_LoginId='"+attendanceVO.attendance_LoginId+"'"
        )
        attendanceDict=cursor1.fetchall()
        cursor1.close()
        connection.close()
        return attendanceDict

    def updateAttendance(self,attendanceVO):
        connection=con_db()
        cursor1=connection.cursor()
        cursor1.execute(
            "UPDATE attendancemaster SET attendanceDate='"+attendanceVO.attendanceDate+"',attendanceTime='"+attendanceVO.attendanceTime+"',attendanceStatus='"+attendanceVO.attendanceStatus+"' WHERE attendance_LoginId='"+attendanceVO.attendance_LoginId+"' AND attendanceActiveStatus='"+attendanceVO.attendanceActiveStatus+"'"
        )
        connection.commit()
        cursor1.close()
        connection.close()