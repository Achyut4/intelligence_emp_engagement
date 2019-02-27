import smtplib
import string
from random import choice

from flask import render_template, redirect, request, session, url_for
from smtplib import SMTP
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import Message
from project import app
from project.com.dao.DepartmentDAO import DepartmentDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.dao.RoleDAO import RoleDAO
from project.com.vo.DepartmentVO import DepartmentVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO
from project.com.vo.RoleVO import RoleVO


@app.route('/loadRegister')
def loadregister():
    # Here we take DepartmentDAO and RoleDAO object and pass search method to get department and role data
    departmentDAO = DepartmentDAO()
    departmentVO = DepartmentVO()
    roleDAO = RoleDAO()
    roleVO = RoleVO()
    departmentVO.departmentActiveStatus = 'activate'
    roleVO.roleActiveStatus = 'activate'
    departmentDict = departmentDAO.searchDepartment(departmentVO)

    roleDict = roleDAO.searchRole(roleVO)
    # we pass departmentDict & roleDict to register.html and call it in drop-down
    return render_template('user/register.html', departmentDict=departmentDict, roleDict=roleDict)


# method to insert data in registermaster table
@app.route('/insertRegister', methods=['POST'])
def insertregister():
    registerDAO = RegisterDAO()
    registerVO = RegisterVO()
    loginDAO = LoginDAO()
    loginVO = LoginVO()
    departmentDAO = DepartmentDAO()
    departmentVO = DepartmentVO()
    roleDAO = RoleDAO()
    roleVO = RoleVO()
    departmentVO.departmentActiveStatus = 'activate'
    roleVO.roleActiveStatus = 'activate'

    departmentDict = departmentDAO.searchDepartment(departmentVO)

    roleDict = roleDAO.searchRole(roleVO)

    # generate random password
    alphabet = string.ascii_letters + string.digits
    password = ''.join(choice(alphabet) for i in range(8))

    # get data from HTML form
    registerVO.registerFirstName = request.form['RegisterFirstName']
    registerVO.registerLastName = request.form['RegisterLastName']
    registerVO.registerContact = request.form['RegisterContact']
    registerVO.registerGender = request.form['RegisterGender']
    registerVO.registerAddress = request.form['RegisterAddress']

    # get departmentid
    registerVO.register_DepartmentId = str(request.form['RegisterDepartment'])

    # get roleid
    registerVO.register_RoleId = str(request.form['RegisterRole'])

    # registerVO.registerImage=request.form['RegisterImage']

    registerVO.registerActiveStatus = 'activate'
    loginVO.loginEmail = request.form['RegisterEmail']
    loginVO.loginPassword = password
    loginVO.loginActiveStatus = 'activate'
    loginVO.loginRole = 'user'

    loginEmailDict = loginDAO.searchEmailLogin(loginVO)
    if loginVO.loginEmail in loginEmailDict[0].values():
        return render_template('admin/register.html', registerErrorEmail='Email already registered',
                               registererrorFirstName=registerVO.registerFirstName,
                               registererrorLastName=registerVO.registerLastName,
                               registererrorContact=registerVO.registerContact, registererrorEmail=loginVO.loginEmail,
                               departmentDict=departmentDict, roleDict=roleDict)

    # store loginId in loginDict
    # if(validate_email(loginVO.loginEmail) == 'FALSE' or 'false'):
    #
    #     return render_template('admin/register.html',registererrorEmail ="Please enter valid Email")
    # else:
    loginDict = loginDAO.insertLogin(loginVO)

    # Send Password through Mail
    fromaddr = "dabhi9597@gmail.com"

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = loginVO.loginEmail
    msg['Subject'] = "PYTHON PASSWORD"

    msg.attach(MIMEText(loginVO.loginPassword, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()

    password = "dabhi143"
    server.login(fromaddr, password)

    text = msg.as_string()

    server.sendmail(fromaddr, loginVO.loginEmail, text)

    server.quit()

    registerVO.register_LoginId = str(loginDict)
    # insert data into registermaster table
    # if (validate_email(registerVO.registerEmail) == 'FALSE'):
    #     return render_template('admin/register.html',registererrorEmail ="Please enter valid Email")
    # else:
    registerDAO.insertRegister(registerVO)

    # return to login.html after successful data insertion into registermaster and loginmaster table

    return render_template("admin/login.html")
