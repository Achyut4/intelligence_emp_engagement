from project.com.dao import *


class LoginDAO:
    def searchEmailLogin(self,loginVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT loginEmail FROM loginmaster WHERE loginEmail='"+loginVO.loginEmail+"'"
        )
        loginEmailDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return loginEmailDict

    def insertLogin(self,loginVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor2 = connection.cursor()
        # Insert query to add data into table
        cursor1.execute(
            "INSERT INTO loginmaster(loginEmail,loginPassword,loginActiveStatus,loginRole) VALUES ('"+loginVO.loginEmail+"','"+loginVO.loginPassword+"','"+loginVO.loginActiveStatus+"','"+loginVO.loginRole+"')")
        connection.commit()
        #select max loginid for taking foereign key in registermaster table
        cursor2.execute("SELECT MAX(loginId) FROM loginmaster")
        loginDict=cursor2.fetchall()
        cursor1.close()
        cursor2.close()
        loginDict=loginDict[0]
        loginDict=loginDict['MAX(loginId)']
        connection.close()
        return loginDict

    def searchLogin(self,loginVO):
        connection = con_db()
        cursor1 = connection.cursor()
        #select query to perform login
        cursor1.execute(
            "SELECT * FROM loginmaster WHERE loginEmail = '"+loginVO.loginEmail+"' "
        )
        loginDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return loginDict
