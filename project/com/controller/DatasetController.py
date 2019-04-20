from flask import render_template,redirect,request,session,url_for
from werkzeug.utils import secure_filename
from project.com.dao.DatasetDAO import DatasetDAO
from project.com.vo.DatasetVO import DatasetVO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.RegisterVO import RegisterVO
from project.com.dao.DepartmentDAO import DepartmentDAO
from project.com.vo.DepartmentVO import DepartmentVO

from project import app
import os
import json
import face_recognition
import pickle



#first it loads addDataset.html page
@app.route('/loadDataset')
def loaddataset():
    try:
        if session['sessionloginRole'] == 'admin':
            departmentDAO = DepartmentDAO()
            departmentVO = DepartmentVO()
            departmentVO.departmentActiveStatus = 'activate'
            departmentDict = departmentDAO.searchDepartment(departmentVO)
            return render_template("admin/addDataset.html", departmentDict=departmentDict)
        else:
            return render_template('admin/login.html',loginerrorDict ='Please login first')
    except:
        return render_template("admin/login.html", loginerrorEmailDict="Please login first")


#it inserts the dataset values into the table
@app.route('/insertDataset',methods=['POST'])
def insertDataset():

    if session['sessionloginRole'] == 'admin':
        datasetDAO=DatasetDAO()
        datasetVO = DatasetVO()

        UPLOAD_FOLDER = 'C:/Users/Dell/PycharmProjects/intelligence_emp_engage/project/static/adminResources/dataset/employee'

        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        file = request.files['DatasetFile']
        datasetVO.datasetName = secure_filename(file.filename)

        #join path with file name
        datasetVO.datasetPath = os.path.join(app.config['UPLOAD_FOLDER'])

        #save uploaded file at specific path
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],datasetVO.datasetName))

        datasetVO.dataset_DepartmentId=str(request.form['DatasetDepartment'])
        datasetVO.dataset_LoginId=str(request.form['DatasetLoginId'])
        #datasetVO.datasetDescription = datasetVO.datasetDescription.replace("'"," ")
        datasetVO.datasetActiveStatus = 'activate'
        datasetDAO.insertDataset(datasetVO)

        #Save image encodings in pickel file
        all_face_encoding = {}
        #it will load model from adminResources/dataset folder 
        path = 'C:/Users/Dell/PycharmProjects/intelligence_emp_engage/project/static/adminResources/dataset/model/dataset_faces.dat'

        if os.path.exists(path):
            pass
        else:
            #if the model is not created then this line make empty file
            open(path,'w')
            print "**File Created Successfuly**"

        # registerId = datasetVO.dataset_RegisterId
        image_file = face_recognition.load_image_file(
            UPLOAD_FOLDER+"/{}".format(
                datasetVO.datasetName))
        all_face_encoding[datasetVO.dataset_LoginId[0]] = face_recognition.face_encodings(image_file)[0]
        
        #this line will update the model
        with open('C:/Users/Dell/PycharmProjects/intelligence_emp_engage/project/static/adminResources/dataset/model/dataset_faces.dat',
                  'ab') as f:
            pickle.dump(all_face_encoding, f)
        print "*****File Updated Successfully*****"

        return render_template("admin/addDataset.html")

    else:
        return render_template('admin/login.html',loginerrorDict ='Please login first')

#method to view dataset
@app.route('/viewDataset')
def viewDataset():
    try:
        if session['sessionloginRole'] == 'admin':
            datasetDAO = DatasetDAO()
            datasetVO = DatasetVO()
            datasetDict=datasetDAO.viewDataset(datasetVO)
            return render_template("admin/viewDataset.html",datasetDict=datasetDict)

        else:
            return render_template('admin/login.html', loginerrorDict='Please login first')
    except:
        return render_template("admin/login.html", loginerrorEmailDict="Please login first")


#method to deleteDataset
@app.route('/deleteDataset',methods=['POST'])
def deleteDataset():
    if session['sessionloginRole'] == 'admin':
        datasetDAO = DatasetDAO()
        datasetVO = DatasetVO()
        datasetVO.datasetId = request.form['DatasetId']
        datasetVO.datasetActiveStatus = 'deactivate'
        datasetDAO.deleteDataset(datasetVO)
        return redirect("/viewDataset")

    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')

@app.route('/ajaxDatasetRegister')
def DatasetRegister():
    registerDAO = RegisterDAO()
    registerVO = RegisterVO()
    registerVO.register_DepartmentId = request.args.get('dataset_DepartmentId')

    registerVO.register_DepartmentId=registerVO.register_DepartmentId[1:len(registerVO.register_DepartmentId)-1]
    print "=======>>>",registerVO.register_DepartmentId
    ajaxRegisterDatasetDict = registerDAO.ajaxRegisterDepartment(registerVO)
    print ajaxRegisterDatasetDict

    jsn=json.dumps(ajaxRegisterDatasetDict)
    print jsn
    return jsn