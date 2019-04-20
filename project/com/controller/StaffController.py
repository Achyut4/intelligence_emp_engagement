"""Staff controller used to view,delete,update the details of particular Staff """

from flask import render_template, redirect, request, session, url_for
from project.com.dao.StaffDAO import StaffDAO
from project.com.vo.StaffVO import StaffVO
from project.com.dao.DepartmentDAO import DepartmentDAO
from project.com.vo.DepartmentVO import DepartmentVO
from project.com.dao.RoleDAO import RoleDAO
from project.com.vo.RoleVO import RoleVO
from project import app


@app.route('/loadStaff')
def loadStaff():
    pass


@app.route('/insertStaff')
def insertStaff():
    pass


# view staff method
@app.route('/viewStaff')
def viewStaff():

    try:
        if session['sessionloginRole'] == 'admin':
            staffDAO = StaffDAO()
            departmentVO = DepartmentVO()
            roleVO = RoleVO()
            staffVO = StaffVO()
            staffVO.registerActiveStatus = 'activate'
            departmentVO.departmentActiveStatus = 'activate'
            roleVO.roleActiveStatus = 'activate'
            staffDict = staffDAO.searchStaff(staffVO, departmentVO, roleVO)
            return render_template("admin/viewStaff.html", staffDict=staffDict)

        elif session['sessionloginRole'] == 'user':
            staffDAO = StaffDAO()
            departmentVO = DepartmentVO()
            roleVO = RoleVO()
            staffVO = StaffVO()

            staffVO.register_LoginId = str(session['sessionloginId'])
            staffVO.registerActiveStatus = 'activate'
            departmentVO.departmentActiveStatus = 'activate'
            roleVO.roleActiveStatus = 'activate'
            staffDict = staffDAO.searchUserStaff(staffVO, departmentVO, roleVO)
            return render_template("user/viewStaff.html", staffDict=staffDict)

        else:
            return render_template('admin/login.html', loginerrorDict='Please login first')


    except:
        return render_template("admin/login.html", loginerrorEmailDict="Please login first")


# delete staff method
@app.route('/deleteStaff', methods=['POST'])
def deleteStaff():
    if session['sessionloginRole'] == 'admin':
        staffDAO = StaffDAO()
        staffVO = StaffVO()

        # we have to change activestatus of staff in registermaster table and loginmaster table
        staffVO.register_LoginId = request.form['Register_LoginId']
        staffVO.registerActiveStatus = 'deactivate'
        staffVO.loginActiveStatus = 'deactivate'
        staffDAO.deleteStaff(staffVO)

        return redirect('/viewStaff')
    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')


# edit staff method
@app.route('/editStaff', methods=['POST'])
def editStaff():
    # for edit the details of staff first we have to load the data in dropdown so DepartmentDAO's and RoleDAO's search method called
    if session['sessionloginRole'] == 'admin':
        staffDAO = StaffDAO()
        staffVO = StaffVO()
        departmentDAO = DepartmentDAO()
        departmentVO = DepartmentVO()
        roleDAO = RoleDAO()
        roleVO = RoleVO()
        staffVO.loginActiveStatus = 'activate'
        departmentVO.departmentActiveStatus = 'activate'
        roleVO.roleActiveStatus = 'activate'

        departmentDict = departmentDAO.searchDepartment(departmentVO)
        roleDict = roleDAO.searchRole(roleVO)
        staffVO.register_LoginId = request.form['Register_LoginId']
        staffDict = staffDAO.editStaff(staffVO)
        return render_template('admin/editStaff.html', staffDict=staffDict, departmentDict=departmentDict,
                               roleDict=roleDict)
    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')


# update staff method
@app.route('/updateStaff', methods=['POST'])
def updateStaff():
    try:
        if session['sessionloginRole'] == 'admin':
            staffDAO = StaffDAO()
            staffVO = StaffVO()

            staffVO.register_LoginId = request.form['Register_LoginId']
            staffVO.registerFirstName = request.form['RegisterFirstName']
            staffVO.registerLastName = request.form['RegisterLastName']
            staffVO.registerContact = request.form['RegisterContact']
            staffVO.registerEmail = request.form['RegisterEmail']
            staffVO.registerGender = request.form['RegisterGender']
            staffVO.registerAddress = request.form['RegisterAddress']
            staffVO.register_DepartmentId = request.form['RegisterDepartmentId']
            staffVO.register_RoleId = request.form['RegisterRoleId']
            staffDAO.updateStaff(staffVO)
            return redirect('/viewStaff')

        elif session['sessionloginRole']=='user':
            staffDAO = StaffDAO()
            staffVO = StaffVO()
            staffVO.register_LoginId = str(session['sessionloginId'])
            staffVO.registerFirstName = request.form['RegisterFirstName']
            staffVO.registerLastName = request.form['RegisterLastName']
            staffVO.registerContact = request.form['RegisterContact']
            staffVO.registerEmail = request.form['RegisterEmail']
            staffVO.registerPassword=request.form['RegisterPassword']
            staffVO.registerAddress = request.form['RegisterAddress']
            staffDAO.updateUserStaff(staffVO)
            return redirect('/viewStaff')

        else:
            return render_template('admin/login.html', loginerrorDict='Please login first')

    except:
        return render_template("admin/login.html", loginerrorEmailDict="Please login first")
