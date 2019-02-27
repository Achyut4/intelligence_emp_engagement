from flask import render_template,redirect,request,session,url_for
from werkzeug.utils import secure_filename
from project.com.dao.DatasetDAO import DatasetDAO
from project.com.vo.DatasetVO import DatasetVO
from project import app
import os


#first it loads addDataset.html page
@app.route('/loadDataset')
def loaddataset():
    try:
        if session['sessionloginRole'] == 'admin':
            return render_template("admin/addDataset.html")
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

        UPLOAD_FOLDER = 'C:/Users/Dell/PycharmProjects/intelligence_emp_engage/project/static/adminResources/dataset'

        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        file = request.files['DatasetFile']
        datasetVO.datasetName = secure_filename(file.filename)

        #join path with file name
        datasetVO.datasetPath = os.path.join(app.config['UPLOAD_FOLDER'])

        #save uploaded file at specific path
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],datasetVO.datasetName))

        datasetVO.datasetDescription = request.form['DatasetDescription'].replace("'", "")
        #datasetVO.datasetDescription = datasetVO.datasetDescription.replace("'"," ")
        datasetVO.datasetActiveStatus = 'activate'
        datasetDAO.insertDataset(datasetVO)

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