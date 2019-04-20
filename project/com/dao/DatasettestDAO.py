from project.com.dao import *

class DatasettestDAO:
    def insertDatasettest(self, datasettestVO):
        connection = con_db()
        cursor1 = connection.cursor()
        #Insert query to add data into departmentmaster table
        cursor1.execute(
            "INSERT INTO datasetmaster(datasetName,datasetPath,datset_DepartmentId,dataset_RegisterId,datasetActiveStatus) VALUES ('" + datasettestVO.datasetName + "','" + datasettestVO.datasetPath + "','"+datasettestVO.dataset_DepartmentId+"','"+datasettestVO.dataset_RegisterId+"','" + datasettestVO.datasetActiveStatus + "')")
        connection.commit()
        cursor1.close()
        connection.close()
