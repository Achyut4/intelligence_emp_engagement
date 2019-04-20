"""Login controller is used to perform login activity
first in this line[@app.route('/')] loads login.html page when user submit login credentials
it checks for records in loginmaster table and set session according
to login role
and when logout method called it clear the session data"""
import smtplib
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import render_template, redirect, request, session, url_for
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.RegisterVO import RegisterVO
from project.com.vo.LoginVO import LoginVO
from project.com.dao.LogDAO import LogDAO
from project.com.vo.LogVO import LogVO
from datetime import datetime
from project import app


# load the login page at beggining
@app.route('/')
def loadLogin():
    return render_template('admin/login.html')


# check login credentials
@app.route('/checkLogin', methods=['POST'])
def checkLogin():
    loginDAO = LoginDAO()
    loginVO = LoginVO()
    registerDAO = RegisterDAO()
    registerVO = RegisterVO()
    loginVO.loginEmail = request.form['LoginEmail']
    loginVO.loginPassword = request.form['LoginPassword']
    loginDict = loginDAO.searchLogin(loginVO)


    # if email is not existes in loginmaster return error
    if len(loginDict) == 0:
        return render_template('admin/login.html', loginerrorEmailDict="Invalid Email",
                               loginerrorEmail=loginVO.loginEmail, loginerrorPassword=loginVO.loginPassword)

    # if password doesn't match with records so return error
    elif loginDict[0]["loginPassword"] != loginVO.loginPassword:
        return render_template('admin/login.html', loginerrorPasswordDict="Invalid Password",
                               loginerrorPassword=loginVO.loginPassword, loginerrorEmail=loginVO.loginEmail)

    # when login successfully stores loginId&loginrole in session
    else:
        session['sessionloginId'] = loginDict[0]["loginId"]
        session['sessionloginRole'] = loginDict[0]["loginRole"]
        return redirect(url_for("loadIndex"))


# loadIndex method to load index page for Admin
@app.route('/loadIndex')
def loadIndex():
    # try:

    if session['sessionloginRole'] == 'admin':
        logDAO = LogDAO()
        logVO = LogVO()

        registerDAO = RegisterDAO()
        registerVO = RegisterVO()

        logVO.logDate = str(datetime.today().strftime("%d-%m-%Y"))

        logVO.logDate = logVO.logDate.split('-')

        logVO.logDate.pop(0)

        separater = '-'
        logVO.logDate = separater.join(logVO.logDate)
        logVO.logDate = separater + logVO.logDate

        registerVO.registerActiveStatus = 'activate'
        registerLogDict = registerDAO.searchRegisterLog(registerVO)

        logDict = logDAO.searchReport(logVO, registerVO)

        log_LoginId = []
        loginIdDict = logDAO.searchlogin(logVO)
        for i in range(len(loginIdDict)):
            log_LoginId.append(loginIdDict[i]['log_LoginId'])
        count = []

        for i in range(len(logDict)):
            number = 0
            for j in range(len(logDict)):
                if logDict[j]['log_LoginId'] == i:
                    number = number + 1
            if number == 0:
                continue
            else:
                count.append(number)
        error="Hello Admin"
        if 'error' in session:
            error=session['error']
            session.pop('error')
        print count
        return render_template('admin/index.html', registerLogDict=registerLogDict, count=count, c=len(count),error=error)


    else:
        logDAO = LogDAO()
        logVO = LogVO()

        registerDAO = RegisterDAO()
        registerVO = RegisterVO()

        logVO.logDate = str(datetime.today().strftime("%d-%m-%Y"))

        logVO.logDate = logVO.logDate.split('-')

        logVO.logDate.pop(0)

        separater = '-'
        logVO.logDate = separater.join(logVO.logDate)
        logVO.logDate = separater + logVO.logDate
        logVO.log_LoginId=str(session['sessionloginId'])

        logDict = logDAO.searchUserReport(logVO)
        count=len(logDict)
        print count
        return render_template('user/index.html',month=logVO.logDate,count=count)
    # except:
    #     return render_template('admin/login.html', loginerrorEmailDict="Please login first")


@app.route('/loadForgotPassword')
def loadForgotPassword():
    return render_template('admin/forgotPassword.html')


@app.route('/insertForgotPassword', methods=['POST'])
def insertForgotPassword():
    loginDAO = LoginDAO()
    loginVO = LoginVO()
    loginVO.loginEmail = request.form['ForgotPasswordEmailId']
    loginDict = loginDAO.searchLogin(loginVO)
    if len(loginDict) == 0:
        return render_template('admin/forgotPassword.html', forgotPassworderrorEmailDict='No Email Address found')
    else:
        fromaddr = "dabhi9597@gmail.com"

        msg = MIMEMultipart()

        msg['From'] = fromaddr

        msg['To'] = loginDict[0]['loginEmail']
        msg['Subject'] = "PYTHON PASSWORD"
        userpassword = loginDict[0]['loginPassword']

        msg.attach(MIMEText(userpassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        password = "dabhi143"
        server.login(fromaddr, password)

        text = msg.as_string()

        server.sendmail(fromaddr, loginVO.loginEmail, text)

        server.quit()
        return redirect('/')


# when logout method calls it clear the session value and redirect to login.html page
@app.route('/logout')
def logout():
    # clear the content of cookies
    session.clear()
    return redirect('/')
