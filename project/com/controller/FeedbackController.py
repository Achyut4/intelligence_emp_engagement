from flask import render_template, redirect, request, session, url_for
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.FeedbackVO import FeedbackVO
from datetime import datetime
from project import app


@app.route('/loadFeedback')
def loadFeedback():
    if session['sessionloginRole'] == 'user':
        return render_template('user/addFeedback.html')
    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')


@app.route('/insertFeedback', methods=['POST'])
def inserFeedback():
    if session['sessionloginRole'] == 'user':
        feedbackDAO = FeedbackDAO()
        feedbackVO = FeedbackVO()

        feedbackVO.feedbackRating = request.form['FeedbackRating']
        print feedbackVO.feedbackRating
        feedbackVO.feedbackDescription = request.form['FeedbackDescription'].replace("'", "")
        print feedbackVO.feedbackDescription
        feedbackVO.feedbackFrom_LoginId = str(session['sessionloginId'])
        print feedbackVO.feedbackFrom_LoginId
        feedbackVO.feedbackDate = str(datetime.today().strftime("%d-%m-%y"))
        print feedbackVO.feedbackDate
        feedbackVO.feedbackTime = str(datetime.now().hour) + ':' + str(datetime.now().minute)
        print feedbackVO.feedbackTime
        feedbackVO.feedbackActiveStatus = 'activate'
        feedbackDAO.insertFeedback(feedbackVO)
        return redirect("/loadIndex")

    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')


@app.route('/viewFeedback')
def viewFeedback():
    if session['sessionloginRole'] == 'admin':
        feedbackDAO = FeedbackDAO()
        feedbackVO = FeedbackVO()

        feedbackVO.feedbackActiveStatus = 'activate'
        feedbackDict = feedbackDAO.searchFeedback(feedbackVO)

        return render_template('admin/viewFeedback.html', feedbackDict=feedbackDict)

    if session['sessionloginRole'] == 'user':
        feedbackDAO = FeedbackDAO()
        feedbackVO = FeedbackVO()

        feedbackVO.feedbackActiveStatus = 'activate'
        feedbackVO.feedbackFrom_LoginId = str(session['sessionloginId'])
        feedbackDict = feedbackDAO.searchUserFeedback(feedbackVO)

        return render_template('user/viewFeedback.html', feedbackDict=feedbackDict)
    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')


@app.route('/updateFeedback', methods=['POST'])
def updateFeedback():
    if session['sessionloginRole'] == 'admin':
        feedbackDAO = FeedbackDAO()
        feedbackVO = FeedbackVO()

        feedbackVO.feedbackId = str(request.form['FeedbackId'])
        feedbackVO.feedbackTo_LoginId = str(session['sessionloginId'])
        feedbackVO.feedbackActiveStatus = 'activate'
        feedbackDAO.updateFeedback(feedbackVO)

        return redirect(url_for("viewFeedback"))
    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')


@app.route('/deleteFeedback', methods=['POST'])
def deleteFeedback():
    if session['sessionloginRole'] == 'user':
        feedbackDAO = FeedbackDAO()
        feedbackVO = FeedbackVO()

        feedbackVO.feedbackActiveStatus = 'deactivate'
        feedbackVO.feedbackId = request.form['FeedbackId']
        feedbackDAO.deleteFeedback(feedbackVO)

        return redirect('/viewFeedback')
    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')
