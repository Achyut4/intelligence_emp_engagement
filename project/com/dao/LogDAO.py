from project.com.dao import *


class LogDAO:
    def insertlog(self, logVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "INSERT INTO logmaster(logDate,logTime,log_LoginId,log_DepartmentId) VALUES ('" + logVO.logDate + "','" + logVO.logTime + "','" + logVO.log_LoginId + "','" + logVO.log_DepartmentId + "')"
        )
        connection.commit()
        cursor1.close()
        connection.close()

    def searchDuplicateLog(self, logVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT log_LoginId FROM logmaster WHERE logDate='" + logVO.logDate + "'AND log_LoginId='" + logVO.log_LoginId + "'"
        )
        logDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return logDict

    def searchlogDepartment(self, logVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT * FROM logmaster INNER JOIN registermaster ON logmaster.log_LoginId = registermaster.register_LoginId WHERE register_LoginId='" + logVO.log_LoginId + "'"
        )
        departmentDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return departmentDict

    def searchLog(self, logVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT * FROM (((registermaster INNER JOIN logmaster ON logmaster.log_LoginId=registermaster.register_LoginId) INNER JOIN departmentmaster ON registermaster.register_DepartmentId = departmentmaster.departmentId) INNER JOIN rolemaster ON registermaster.register_RoleId=rolemaster.roleId) WHERE logDate='" + logVO.logDate + "'"
        )
        logDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return logDict

    def searchlogin(self,logVO):
        connection=con_db()
        cursor1=connection.cursor()
        cursor1.execute(
            "SELECT DISTINCT(log_LoginId) FROM logmaster"
        )
        loginIdDict=cursor1.fetchall()
        cursor1.close()
        connection.close()
        return loginIdDict

    def searchReport(self, logVO,registerVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT * FROM (((logmaster INNER JOIN registermaster ON logmaster.log_LoginId = registermaster.register_LoginId)INNER JOIN datasetmaster ON logmaster.log_LoginId=datasetmaster.dataset_LoginId)INNER JOIN departmentmaster ON logmaster.log_DepartmentId=departmentmaster.departmentId) WHERE logmaster.logDate LIKE '%" + logVO.logDate + "' AND registermaster.registerActiveStatus='"+registerVO.registerActiveStatus+"'"
            # ORDER BY COUNT(logId)

        )
        logDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return logDict

    def searchUserReport(self, logVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT * FROM logmaster WHERE log_LoginId='" + logVO.log_LoginId + "' AND logDate LIKE '%" + logVO.logDate + "' "
        )
        logDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return logDict
