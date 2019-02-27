"""Department controller used to add,view,delete,update the details of Department at admin Side"""

from flask import render_template,redirect,request,session,url_for
from project.com.dao.DepartmentDAO import DepartmentDAO
from project.com.vo.DepartmentVO import DepartmentVO
from project import app

# default function to open addDepartment.html page
@app.route('/loadDepartment')
def loadDepartment():
    try:
        if session['sessionloginRole'] == 'admin':
            return render_template('admin/addDepartment.html')
        else:
            return render_template('admin/login.html', loginerrorDict='Please login first')
    except:
        return render_template("admin/login.html", loginerrorEmailDict="Please login first")

# method to insert data into Department table
@app.route('/insertDepartment', methods=['POST'])
def insertDepartment():
    try:
        if session['sessionloginRole']=='admin':
            departmentDAO = DepartmentDAO()
            departmentVO = DepartmentVO()

            #take department name into DepartmentVO object
            departmentVO.departmentName = request.form['DepartmentName']
            departmentVO.departmentActiveStatus = 'activate'
            #pass VO object value to DepartmentDAO class(insertDepartment function)
            departmentDAO.insertDepartment(departmentVO)

            #return to addDepartment.html page
            return render_template("admin/addDepartment.html")
        else:
            return render_template('admin/login.html', loginerrorDict='Please login first')
    except:
        return render_template("admin/login.html", loginerrorEmailDict="Please login first")

#method to display dato of Department table
@app.route('/viewDepartment')
def viewDepartment():
    try:
        if session['sessionloginRole'] == 'admin':
            departmentDAO = DepartmentDAO()
            departmentVO = DepartmentVO()

            departmentVO.departmentActiveStatus = 'activate'
            #pass VO object value to DepartmentDAO class(viewDepartment function)
            departmentDict=departmentDAO.searchDepartment(departmentVO)

            return render_template("admin/viewDepartment.html",departmentDict=departmentDict)
        else:
            return render_template('admin/login.html', loginerrorDict='Please login first')
    except:
        return render_template("admin/login.html", loginerrorEmailDict="Please login first")

@app.route('/deleteDepartment', methods=['POST'])
def deleteDepartment():
    if session['sessionloginRole'] == 'admin':
        departmentDAO = DepartmentDAO()
        departmentVO = DepartmentVO()

        departmentVO.departmentId = request.form['DepartmentId']
        departmentVO.departmentActiveStatus = 'deactivate'
        departmentDAO.deleteDepartment(departmentVO)
        return redirect(url_for('viewDepartment'))
    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')

@app.route('/editDepartment', methods=['POST'])
def editDepartment():
    if session['sessionloginRole'] == 'admin':
        departmentDAO = DepartmentDAO()
        departmentVO = DepartmentVO()

        departmentVO.departmentId = request.form['DepartmentId']
        departmentDict=departmentDAO.editDepartment(departmentVO)

        return render_template("admin/editDepartment.html", departmentDict = departmentDict)
    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')

@app.route('/updateDepartment', methods=['POST'])
def updateDepartment():
    try:
        if session['sessionloginRole']=='admin':
            departmentDAO = DepartmentDAO()
            departmentVO = DepartmentVO()

            departmentVO.departmentId = request.form['DepartmentId']
            departmentVO.departmentName = request.form['DepartmentName']
            departmentDAO.updateDepartment(departmentVO)
            return redirect('/viewDepartment')
        else:
            return render_template('admin/login.html', loginerrorDict='Please login first')
    except:
        return render_template("admin/login.html", loginerrorEmailDict="Please login first")