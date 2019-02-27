from project.com.dao import *

class DatasetDAO:
    def insertDataset(self, datasetVO):
        connection = con_db()
        cursor1 = connection.cursor()
        #Insert query to add data into departmentmaster table
        cursor1.execute(
            "INSERT INTO datasetmaster(datasetName,datasetPath,datasetDescription,datasetActiveStatus) VALUES ('" + datasetVO.datasetName + "','" + datasetVO.datasetPath + "','" + datasetVO.datasetDescription + "','" + datasetVO.datasetActiveStatus + "')")
        connection.commit()
        cursor1.close()
        connection.close()

    def viewDataset(self,datasetVO):
        connection=con_db()
        cursor1=connection.cursor()
        cursor1.execute(
            "SELECT * FROM datasetmaster WHERE datasetActiveStatus='activate' "
        )
        datasetDict=cursor1.fetchall()
        cursor1.close()
        connection.close()
        return datasetDict

    def deleteDataset(self,datasetVO):
        connection=con_db()
        cursor1=connection.cursor()
        cursor1.execute(
            "UPDATE datasetmaster SET datasetActiveStatus = '"+datasetVO.datasetActiveStatus+"' WHERE datasetId=" +datasetVO.datasetId+ ""
        )
        connection.commit()
        cursor1.close()
        connection.close()