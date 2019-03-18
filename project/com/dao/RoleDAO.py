from project.com.dao import *

class RoleDAO:

    try:
        #function to insert data into rolemaster table
        def insertRole(self, roleVO):
            print "Process 1.1"
            connection= con_db()
            cursor1 = connection.cursor()
            #query to insert data into rolemaster table
            cursor1.execute("INSERT INTO rolemaster(roleName,roleActiveStatus,role_DepartmentId) VALUES('" + roleVO.roleName + "','" + roleVO.roleActiveStatus + "','"+roleVO.role_DepartmentId+"')")
            connection.commit()
            cursor1.close()
            connection.close()
    except:
        Exception

    try:
        #function to search data from rolemaster table
        def searchRole(self, roleVO):
            connection = con_db()
            cursor1 = connection.cursor()
            # Search query to fetch data from rolemastertable
            cursor1.execute(
                "SELECT * FROM (rolemaster INNER JOIN departmentmaster ON rolemaster.role_DepartmentId = departmentmaster.departmentId)  WHERE roleActiveStatus = '"+roleVO.roleActiveStatus+"' ")

            roleDict = cursor1.fetchall()
            connection.commit()
            cursor1.close()
            connection.close()
            return roleDict
    except:
        Exception

    try:
        #function to delete data into rolemaster table
        def deleteRole(self, roleVO):
            connection = con_db()
            cursor1 = connection.cursor()
            #update query to change activestatus of rolemaster table
            cursor1.execute(
                "UPDATE rolemaster SET roleActiveStatus = '"+roleVO.roleActiveStatus+"' WHERE roleId= " + roleVO.roleId + "")
            connection.commit()
            cursor1.close()
            connection.close()
    except:
        Exception

    try:
        #function to edit data into rolemaster table
        def editRole(self, roleVO):
            connection = con_db()
            cursor1 = connection.cursor()
            #select query to fetch data from rolemaster table of selected id
            cursor1.execute("SELECT * FROM rolemaster INNER JOIN departmentmaster ON rolemaster.role_DepartmentId = departmentmaster.departmentId WHERE roleId=" +roleVO.roleId+ "")
            roleDict = cursor1.fetchall()
            connection.commit()
            cursor1.close()
            connection.close()
            return roleDict
    except:
        Exception

    try:
        #function to update data into rolemaster table
        def updateRole(self, roleVO):
            connection = con_db()
            cursor1 = connection.cursor()
            #update query to update data into rolemaster table of selected id
            cursor1.execute(
                "UPDATE rolemaster SET roleName = '" + roleVO.roleName + "',role_DepartmentId = '"+roleVO.role_DepartmentId+"' WHERE roleId = " + roleVO.roleId + "")
            connection.commit()
            cursor1.close()
            connection.close()
    except:
        Exception

    def ajaxRoleRegister(self,roleVO):
        connection = con_db()
        cursor1=connection.cursor()
        cursor1.execute(
            "SELECT * FROM rolemaster WHERE role_DepartmentId = '"+roleVO.role_DepartmentId+"' and roleActiveSTatus='activate'"
        )
        ajaxRoleRegisterDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return ajaxRoleRegisterDict
