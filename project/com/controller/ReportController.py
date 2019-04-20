from flask import render_template, redirect, request, session, url_for, jsonify
from project import app
from datetime import datetime
from project.com.dao.LogDAO import LogDAO
from project.com.vo.LogVO import LogVO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.RegisterVO import RegisterVO


@app.route('/loadReport')
def loadReport():
    if session['sessionloginRole'] == 'admin':
        return redirect(ajaxLoadReport)
    elif session['sessionloginRole'] == 'user':
        return render_template('user/viewReport.html')


@app.route('/ajaxLoadReport', methods=['GET'])
def ajaxLoadReport():
    try:
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

            registerVO.registerActiveStatus='activate'
            registerLogDict = registerDAO.searchRegisterLog(registerVO)

            logDict = logDAO.searchReport(logVO,registerVO)

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
            print count
            return render_template('admin/viewReport.html', registerLogDict=registerLogDict, count=count, c=len(count))

        elif session['sessionloginRole'] == 'user':

            logDAO = LogDAO()
            logVO = LogVO

            logVO.log_LoginId = str(session['sessionloginId'])
            logVO.logDate = request.args.get('report_Month')
            logVO.logDate = logVO.logDate.split('-')
            logVO.logDate = logVO.logDate[1] + '-' + logVO.logDate[0]

            logDict = logDAO.searchUserReport(logVO)

            response = jsonify(logDict)

            response.headers.add('Access-Control-Allow-Origin', '*')

            return response


    except:
        return render_template("admin/login.html", loginerrorEmailDict="Please login first")
