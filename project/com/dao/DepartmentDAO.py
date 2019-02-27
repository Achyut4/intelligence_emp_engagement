from project.com.dao import *


class DepartmentDAO:
    #function to insert data into departmentmaster table
    try:
        def insertDepartment(self, departmentVO):
            connection = con_db()
            cursor1 = connection.cursor()
            #Insert query to add data into departmentmaster table
            cursor1.execute(
                "INSERT INTO departmentmaster(departmentName,departmentActiveStatus) VALUES ('" + departmentVO.departmentName + "','" + departmentVO.departmentActiveStatus + "')")
            connection.commit()
            cursor1.close()
            connection.close()
    except:
        Exception

    try:
        #function to search data from departmentmaster table
        def searchDepartment(self,departmentVO):
            connection = con_db()
            cursor1 = connection.cursor()
            #Search query to fetch data from departmentmaster table
            cursor1.execute(
                "SELECT * FROM departmentmaster WHERE departmentActiveStatus = '"+departmentVO.departmentActiveStatus+"' ")

            departmentDict=cursor1.fetchall()
            cursor1.close()
            connection.close()
            return departmentDict
    except:
        Exception

    try:
        #function to change status of data into departmentmaster table
        def deleteDepartment(self, departmentVO):
            connection = con_db()
            cursor1 = connection.cursor()
            #update query to change the data of departmentactivestatus column of departmentmaster table
            cursor1.execute(
                "UPDATE departmentmaster SET departmentActiveStatus = '"+departmentVO.departmentActiveStatus+"' WHERE departmentId= " +departmentVO.departmentId+ ""
            )
            connection.commit()
            cursor1.close()
            connection.close()
    except:
        Exception

    try:
        #function to edit data in departmentmaster table
        def editDepartment(self, departmentVO):
            connection = con_db()
            cursor1 = connection.cursor()
            #select query to get data of selected id from departmentmaster table
            cursor1.execute("SELECT * FROM departmentmaster WHERE departmentId='" +departmentVO.departmentId+ "'")
            departmentDict = cursor1.fetchall()
            connection.commit()
            cursor1.close()
            connection.close()
            return departmentDict
    except:
        Exception

    try:
        #function to update the query in departmentmaster table
        def updateDepartment(self, departmentVO):
            connection = con_db()
            cursor1 = connection.cursor()
            #update query to change the data for selected id from departmentmaster table
            cursor1.execute(
                "UPDATE departmentmaster SET departmentName = '" + departmentVO.departmentName + "' WHERE departmentId = " + departmentVO.departmentId +"")
            connection.commit()
            cursor1.close()
            connection.close()
    except:
        Exception