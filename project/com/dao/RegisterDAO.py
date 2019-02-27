from project.com.dao import *

class RegisterDAO:
    try:
        #function to insert data into registermaster table
        def insertRegister(self,registerVO):
            connection = con_db()
            cursor1 = connection.cursor()
            # Insert query to add data into table
            cursor1.execute(
                "INSERT INTO registermaster(registerFirstName,registerLastName,registerContact,registerGender,registerAddress,register_DepartmentId,register_LoginId,register_RoleId,registerActiveStatus) VALUES ('" + registerVO.registerFirstName + "','"+  registerVO.registerLastName +"','" +registerVO.registerContact+ "','"+ registerVO.registerGender +"','" +registerVO.registerAddress+ "','"+registerVO.register_DepartmentId+"','"+registerVO.register_LoginId+"','"+registerVO.register_RoleId+"','"+registerVO.registerActiveStatus+"')")
            connection.commit()
            cursor1.close()
            connection.close()
    except:
        Exception