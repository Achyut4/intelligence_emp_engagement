from project.com.dao import *


class ComplainDAO:
    def insertComplain(self, complainVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "INSERT INTO complainmaster(complainSubject,complainDescription,complainFrom_LoginId,complainDate,complainTime,complainReply,complainStatus,complainActiveStatus) VALUE ('" + complainVO.complainSubject + "','" + complainVO.complainDescription + "','" + complainVO.complainFrom_LoginId + "','" + complainVO.complainDate + "','" + complainVO.complainTime + "','" + complainVO.complainReply + "','" + complainVO.complainStatus + "','" + complainVO.complainActiveStatus + "')"
        )
        connection.commit()
        cursor1.close()
        connection.close()

    def searchComplain(self, complainVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT * FROM complainmaster INNER JOIN loginmaster ON complainmaster.complainFrom_LoginId = loginmaster.loginId WHERE complainStatus = '" + complainVO.complainStatus + "' AND complainActiveStatus = '" + complainVO.complainActiveStatus + "'"
        )
        complainDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return complainDict

    def searchReplyComplain(self, complainVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT * FROM complainmaster WHERE complainId =" + complainVO.complainId + " "
        )
        complainDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return complainDict

    def insertReplyComplain(self, complainVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "UPDATE complainmaster SET complainReply = '" + complainVO.complainReply + "',complainStatus = '" + complainVO.complainStatus + "',complainTo_LoginId = '" + complainVO.complainTo_LoginId + "' WHERE complainId = '" + complainVO.complainId + "'"
        )
        connection.commit()
        cursor1.close()
        connection.close()

    def searchUserComplain(self, complainVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT * FROM complainmaster LEFT JOIN loginmaster ON complainmaster.complainTo_LoginId=loginmaster.loginId  LEFT JOIN  loginmaster ls1 ON complainmaster.complainFrom_LoginId=ls1.loginId WHERE complainActiveStatus = '" + complainVO.complainActiveStatus + "' and complainFrom_LoginId='" + str(
                complainVO.complainFrom_LoginId) + "'")
        complainDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return complainDict

    def deleteComplain(self, complainVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "UPDATE complainmaster SET complainActiveStatus = '" + complainVO.complainActiveStatus + "' WHERE complainId='" + complainVO.complainId + "'"
        )
        connection.commit()
        cursor1.close()
        connection.close()
