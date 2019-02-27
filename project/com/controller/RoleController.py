from flask import render_template,redirect,request,session,url_for
from project.com.dao.RoleDAO import RoleDAO
from project.com.vo.RoleVO import RoleVO
from project.com.dao.DepartmentDAO import DepartmentDAO
from project.com.vo.DepartmentVO import DepartmentVO
from project import app


@app.route('/loadRole')
def loadRole():
    try:
        if session['sessionloginRole'] == 'admin':
            departmentDAO = DepartmentDAO()
            departmentVO = DepartmentVO()
            departmentVO.departmentActiveStatus = 'activate'
            departmentDict = departmentDAO.searchDepartment(departmentVO)
            return render_template("admin/addRole.html",departmentDict = departmentDict)
        else:
            return render_template('admin/login.html',loginerrorDict ='Please login first')
    except:
        return render_template("admin/login.html",loginerrorEmailDict="Please login first")

@app.route('/insertRole', methods=['POST'])
def insertRole():
    try:
        if session['sessionloginRole'] == 'admin':
            roleDAO = RoleDAO()
            roleVO = RoleVO()
            roleVO.role_DepartmentId = request.form['RoleDepartment']
            roleVO.roleName= request.form['RoleName']
            roleVO.roleActiveStatus = 'activate'
            roleDAO.insertRole(roleVO)
            return redirect(url_for("loadRole"))
        else:
            return render_template('admin/login.html',loginerrorDict ='Please login first')
    except:
        return render_template("admin/login.html", loginerrorEmailDict="Please login first")

@app.route("/viewRole")
def viewRole():
    try:
        if session['sessionloginRole'] == 'admin':
            roleDAO = RoleDAO()
            roleVO = RoleVO()
            roleVO.roleActiveStatus = 'activate'
            roleDict = roleDAO.searchRole(roleVO)
            return render_template("admin/viewRole.html", roleDict=roleDict)
        else:
            return render_template('admin/login.html',loginerrorDict ='Please login first')
    except:
        return render_template("admin/login.html",loginerrorEmailDict="Please login first")

@app.route('/deleteRole', methods=['POST'])
def deleteRole():
    try:
        if session['sessionloginRole'] == 'admin':
            roleDAO = RoleDAO()
            roleVO = RoleVO()

            roleVO.roleId = request.form['RoleId']
            roleVO.roleActiveStatus = 'deactivate'
            roleDAO.deleteRole(roleVO)
            return redirect('/viewRole')
        else:
            return render_template('admin/login.html',loginerrorDict ='Please login first')
    except:
        return render_template("admin/login.html", loginerrorEmailDict="Please login first")

@app.route('/editRole', methods=['POST'])
def editRole():
    try:
        if session['sessionloginRole'] == 'admin':
            roleDAO = RoleDAO()
            roleVO = RoleVO()
            departmentDAO = DepartmentDAO()
            departmentVO = DepartmentVO()
            roleVO.roleId = request.form['RoleId']
            departmentVO.departmentActiveStatus = 'activate'
            departmentDict = departmentDAO.searchDepartment(departmentVO)
            roleDict = roleDAO.editRole(roleVO)
            print roleDict
            return render_template("admin/editRole.html", roleDict=roleDict ,departmentDict = departmentDict)
        else:
            return render_template('admin/login.html',loginerrorDict ='Please login first')
    except:
        return render_template("admin/login.html", loginerrorEmailDict="Please login first")

@app.route('/updateRole', methods=['POST'])
def updateRole():
    try:
        if session['sessionloginRole'] == 'admin':
            roleDAO = RoleDAO()
            roleVO = RoleVO()
            roleVO.roleId = request.form['RoleId']
            roleVO.role_DepartmentId = request.form['RoleDepartmentId']
            roleVO.roleName = request.form['RoleName']
            roleDict=roleDAO.updateRole(roleVO)
            #roleDict = roleDAO.searchRole(roleVO)
            return redirect(url_for('viewRole'))
        else:
            return render_template('admin/login.html',loginerrorDict ='Please login first')
    except:
        return render_template("admin/login.html", loginerrorEmailDict="Please login first")