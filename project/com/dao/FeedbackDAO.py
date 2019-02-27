from project.com.dao import *


class FeedbackDAO:
    def insertFeedback(self, feedbackVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "INSERT INTO feedbackmaster(feedbackRating,feedbackDescription,feedbackFrom_LoginId,feedbackDate,feedbackTime,feedbackActiveStatus) VALUES ('" + feedbackVO.feedbackRating + "','" + feedbackVO.feedbackDescription + "','" + feedbackVO.feedbackFrom_LoginId + "','" + feedbackVO.feedbackDate + "','" + feedbackVO.feedbackTime + "','" + feedbackVO.feedbackActiveStatus + "')"
        )
        connection.commit()
        cursor1.close()
        connection.close()

    def searchFeedback(self, feedbackVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT * FROM feedbackmaster INNER JOIN loginmaster ON feedbackmaster.feedbackFrom_LoginId = loginmaster.loginId WHERE feedbackActiveStatus='" + feedbackVO.feedbackActiveStatus + "'"
        )
        feedbackDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return feedbackDict

    def updateFeedback(self, feedbackVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "UPDATE feedbackmaster SET feedbackTo_LoginId='" + feedbackVO.feedbackTo_LoginId + "' WHERE feedbackId = '" + feedbackVO.feedbackId + "'"
        )
        connection.commit()
        cursor1.close()
        connection.close()

    def searchUserFeedback(self, feedbackVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT * FROM feedbackmaster LEFT JOIN loginmaster ON feedbackmaster.feedbackTo_LoginId=loginmaster.loginId LEFT JOIN loginmaster ls1 ON  feedbackmaster.feedbackFrom_LoginId=ls1.loginId WHERE feedbackActiveStatus = '" + feedbackVO.feedbackActiveStatus + "' AND feedbackFrom_LoginId='" + feedbackVO.feedbackFrom_LoginId + "'"
        )
        feedbackDict = cursor1.fetchall()
        cursor1.close()
        connection.close()
        return feedbackDict

    def deleteFeedback(self, feedbackVO):
        connection=con_db()
        cursor1=connection.cursor()
        cursor1.execute(
            "UPDATE feedbackmaster SET feedbackActiveStatus='"+feedbackVO.feedbackActiveStatus+"' WHERE feedbackId = '"+feedbackVO.feedbackId+"'"
        )
        connection.commit()
        cursor1.close()
        connection.close()