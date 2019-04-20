from project.com.dao import *


class RegisterDAO:
    try:
        # function to insert data into registermaster table
        def insertRegister(self, registerVO):
            connection = con_db()
            cursor1 = connection.cursor()
            cursor2 = connection.cursor()
            # Insert query to add data into table
            cursor1.execute(
                "INSERT INTO registermaster(registerFirstName,registerLastName,registerContact,registerGender,registerAddress,register_DepartmentId,register_LoginId,register_RoleId,registerActiveStatus) VALUES ('" + registerVO.registerFirstName + "','" + registerVO.registerLastName + "','" + registerVO.registerContact + "','" + registerVO.registerGender + "','" + registerVO.registerAddress + "','" + registerVO.register_DepartmentId + "','" + registerVO.register_LoginId + "','" + registerVO.register_RoleId + "','" + registerVO.registerActiveStatus + "')")

            connection.commit()
            cursor1.close()
            connection.close()
    except:
        Exception

    def searchRegister(self,registerVO):
        connection=con_db()
        cursor1=connection.cursor()
        cursor1.execute(
            "SELECT * FROM registermaster WHERE register_LoginId='"+registerVO.register_LoginId+"'"
        )
        registerDict=cursor1.fetchall()
        cursor1.close()
        connection.close()
        return registerDict

    def ajaxRegisterDepartment(self, registerVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT * FROM registermaster WHERE register_DepartmentId='" + registerVO.register_DepartmentId + "' AND registerActiveStatus='activate' "
        )
        ajaxRegisterDatasetDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return ajaxRegisterDatasetDict

    def searchRegisterLog(self,registerVO):
        connection=con_db()
        cursor1=connection.cursor()
        cursor1.execute(
            "SELECT * FROM ((registermaster INNER JOIN datasetmaster ON registermaster.register_LoginId=datasetmaster.dataset_LoginId)INNER JOIN departmentmaster ON registermaster.register_DepartmentId=departmentmaster.departmentId) WHERE registerActiveStatus='"+registerVO.registerActiveStatus+"'"
        )
        registerLogDict=cursor1.fetchall()
        cursor1.close()
        connection.close()
        return registerLogDict