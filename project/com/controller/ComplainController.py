from flask import render_template, redirect, request, session, url_for
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.LoginVO import LoginVO
from datetime import datetime
from project import app


@app.route('/loadComplain')
def loadComplain():
    if session['sessionloginRole'] == 'user':
        return render_template('user/addComplain.html')
    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')


@app.route('/insertComplain', methods=['POST'])
def insertComplain():
    if session['sessionloginRole'] == 'user':
        complainDAO = ComplainDAO()
        complainVO = ComplainVO()
        complainVO.complainSubject = request.form['ComplainSubject'].replace("'", "")
        complainVO.complainDescription = request.form['ComplainDescription'].replace("'", "")
        complainVO.complainFrom_LoginId = str(session['sessionloginId'])
        complainVO.complainDate = str(datetime.today().strftime("%d-%m-%Y"))
        complainVO.complainTime = str(datetime.now().hour) + ':' + str(datetime.now().minute)
        complainVO.complainReply = 'NIL'
        complainVO.complainStatus = 'pending'
        complainVO.complainActiveStatus = 'activate'

        complainDAO.insertComplain(complainVO)
        return render_template('user/index.html')
    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')


@app.route('/viewComplain')
def viewComplain():
    if session['sessionloginRole'] == 'admin':
        complainDAO = ComplainDAO()
        complainVO = ComplainVO()

        complainVO.complainStatus = 'pending'
        complainVO.complainActiveStatus = 'activate'
        complainDict = complainDAO.searchComplain(complainVO)
        return render_template('admin/viewComplain.html', complainDict=complainDict)

    if session['sessionloginRole'] == 'user':
        complainDAO = ComplainDAO()
        complainVO = ComplainVO()

        complainVO.complainFrom_LoginId = str(session['sessionloginId'])
        complainVO.complainActiveStatus = 'activate'

        complainDict = complainDAO.searchUserComplain(complainVO)

        return render_template('user/viewComplain.html', complainDict=complainDict)

    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')


@app.route('/loadReplyComplain', methods=['POST'])
def replyComplain():
    if session['sessionloginRole'] == 'admin':
        complainDAO = ComplainDAO()
        complainVO = ComplainVO()
        complainVO.complainId = request.form['ComplainId']

        complainDict = complainDAO.searchReplyComplain(complainVO)
        return render_template('admin/replyComplain.html', complainDict=complainDict)

    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')


@app.route('/insertReplyComplain', methods=['POST'])
def insertReplyComplain():
    if session['sessionloginRole'] == 'admin':
        complainDAO = ComplainDAO()
        complainVO = ComplainVO

        complainVO.complainId = request.form['ComplainId']
        complainVO.complainReply = request.form['ComplainReply'].replace("'", "")
        complainVO.complainStatus = 'replyed'
        complainVO.complainTo_LoginId = str(session['sessionloginId'])

        complainDAO.insertReplyComplain(complainVO)

        return redirect(url_for("viewComplain"))
    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')


@app.route('/deleteComplain', methods=['POST'])
def deleteComplain():
    if session['sessionloginRole'] == 'user':
        complainDAO = ComplainDAO()
        complainVO = ComplainVO()

        complainVO.complainId = request.form['ComplainId']
        complainVO.complainActiveStatus = 'deactivate'
        complainDAO.deleteComplain(complainVO)
        return redirect('/viewComplain')