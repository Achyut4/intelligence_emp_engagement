from project.com.dao import *

class StaffDAO:
    def insertStaff(self,staffVO,departmentVO):
        pass

    def searchStaff(self,staffVO,departmentVO,roleVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT * FROM (((registermaster INNER JOIN departmentmaster ON registermaster.register_DepartmentId = departmentmaster.departmentId) INNER JOIN rolemaster ON registermaster.register_RoleId = rolemaster.roleId )INNER JOIN loginmaster ON registermaster.register_LoginId = loginmaster.loginId) WHERE departmentActiveStatus = '"+departmentVO.departmentActiveStatus+"' AND roleActiveStatus = '"+roleVO.roleActiveStatus+"' AND registerActiveStatus = '"+staffVO.registerActiveStatus+"'"
        )
        staffDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return staffDict

    def deleteStaff(self,staffVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor2 = connection.cursor()
        cursor1.execute(
            "UPDATE registermaster SET registerActiveStatus = '"+staffVO.registerActiveStatus+"' WHERE register_LoginId = '"+staffVO.register_LoginId+"'"
        )
        cursor2.execute(
            "UPDATE loginmaster SET loginActiveStatus = '" + staffVO.loginActiveStatus + "' WHERE loginId = '" + staffVO.register_LoginId + "'"
        )
        connection.commit()
        cursor1.close()
        cursor2.close()
        connection.close()

    def editStaff(self,staffVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT * FROM (((registermaster INNER JOIN loginmaster ON registermaster.register_LoginId = loginmaster.loginId)INNER JOIN departmentmaster ON registermaster.register_DepartmentId = departmentmaster.departmentId)INNER JOIN rolemaster ON registermaster.register_RoleId = rolemaster.roleId) WHERE register_LoginId = "+staffVO.register_LoginId+""
        )
        staffDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return staffDict


    def updateStaff(self,staffVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor2 = connection.cursor()
        cursor1.execute(
            "UPDATE registermaster SET registerFirstName = '"+staffVO.registerFirstName+"',registerLastName = '"+staffVO.registerLastName+"',registerContact = '"+staffVO.registerContact+"',registerGender = '"+staffVO.registerGender+"',registerAddress = '"+staffVO.registerAddress+"',register_DepartmentId = '"+staffVO.register_DepartmentId+"',register_RoleId = '"+staffVO.register_RoleId+"' WHERE register_LoginId = "+staffVO.register_LoginId+""
        )
        cursor2.execute(
            "UPDATE loginmaster SET loginEmail = '"+staffVO.registerEmail+"' WHERE loginId = "+staffVO.register_LoginId+""
        )
        connection.commit()
        cursor1.close()
        cursor2.close()
        connection.close()