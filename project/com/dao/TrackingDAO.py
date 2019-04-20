from project.com.dao import *

class TrackingDAO:

    def insertTracking(self,trackingVO):
        connection=con_db()
        cursor1=connection.cursor()
        cursor1.execute(
            "INSERT INTO trackingmaster(trackingPlace,trackingTime,tracking_DepartmentId,tracking_RoleId,tracking_LoginId) VALUES('"+trackingVO.trackingPlace +"','"+trackingVO.trackingTime +"','"+trackingVO.tracking_DepartmentId +"','"+trackingVO.tracking_RoleId +"','"+trackingVO.tracking_LoginId +"') "
        )
        connection.commit()
        cursor1.close()
        connection.close()

    def searchTracking(self,trackingVO):
        connection=con_db()
        cursor1=connection.cursor()
        cursor1.execute(
            "SELECT * FROM trackingmaster WHERE tracking_LoginId='"+trackingVO.tracking_LoginId+"'"
        )
        trackingDict=cursor1.fetchall()
        cursor1.close()
        connection.close()
        return trackingDict

    def updateTracking(self,trackingVO):
        connection=con_db()
        cursor1=connection.cursor()
        cursor1.execute(
            "UPDATE trackingmaster SET trackingPlace='"+trackingVO.trackingPlace+"',trackingTime='"+trackingVO.trackingTime+"' WHERE tracking_LoginId='"+trackingVO.tracking_LoginId+"'"
        )
        connection.commit()
        cursor1.close()
        connection.close()

    def searchAjaxTracking(self,trackingVO):
        connection=con_db()
        cursor1=connection.cursor()
        cursor1.execute(
            "SELECT * FROM (((trackingmaster INNER JOIN registermaster ON trackingmaster.tracking_LoginId=registermaster.register_LoginId) INNER JOIN departmentmaster ON trackingmaster.tracking_DepartmentId=departmentmaster.departmentId)INNER JOIN rolemaster ON trackingmaster.tracking_RoleId=rolemaster.roleId) WHERE tracking_RoleId='"+trackingVO.tracking_RoleId+"'"
        )
        trackingDict=cursor1.fetchall()
        cursor1.close()
        connection.close()
        return trackingDict