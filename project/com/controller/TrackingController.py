from flask import render_template, redirect, request, session, url_for, jsonify
from project import app
from project.com.dao.DepartmentDAO import DepartmentDAO
from project.com.vo.DepartmentVO import DepartmentVO
from project.com.dao.RoleDAO import RoleDAO
from project.com.vo.RoleVO import RoleVO
from project.com.dao.TrackingDAO import TrackingDAO
from project.com.vo.TrackingVO import TrackingVO
from datetime import datetime
import urllib
import json
import cv2
import numpy as np
import face_recognition
import pickle


@app.route('/startTracking')
def startTracking():
    trackingDAO = TrackingDAO()
    trackingVO = TrackingVO()

    if session['sessionloginRole'] == 'admin':
        video_capture1 = "http://192.168.43.30:8080/shot.jpg"
        video_capture2 = "http://192.168.43.42:8080/shot.jpg"

        try:
            with open(
                    'C:/Users/Dell/PycharmProjects/intelligence_emp_engage/project/static/adminResources/dataset/model/dataset_faces.dat',
                    'rb') as f:
                all_face_encoding = pickle.load(f)

            known_face_encodings = np.array(list(all_face_encoding.values()))
            known_face_loginId = list(all_face_encoding.keys())

        except:
            session['error'] = 'Please Enter atleast One Dataset'
            return redirect('/loadIndex')
        # face_locations = []
        # face_encodings = []
        face_loginId = []
        process_this_frame = True

        while True:
            try:
                imgResp1 = urllib.urlopen(video_capture1)
            except:
                session['error'] = 'Camera-1 not connected'
                return redirect('/loadIndex')
                #return render_template('admin/index1.html', cameraerrorDict="Camera-1 Not Connected")
            imgNp1 = np.array(bytearray(imgResp1.read()), dtype=np.uint8)
            img1 = cv2.imdecode(imgNp1, -1)
            img1 = cv2.flip(img1, -1)
            # cv2.imshow('IPWebCam1', img1)
            try:
                imgResp2 = urllib.urlopen(video_capture2)
            except:
                session['error'] = 'Camera-2 not connected'
                return redirect('/loadIndex')
                #return render_template('admin/index.html',cameraerrorDict="Camera-2 Not Connected")
            imgNp2 = np.array(bytearray(imgResp2.read()), dtype=np.uint8)
            img2 = cv2.imdecode(imgNp2, -1)

            # cv2.imshow('IPWebCam2', img2)

            # frame = "http://192.168.43.120:8080/shot.jpg"

            # Resize frame of video to 1/4 size for faster face recognition processing
            # small_frame = cv2.resize(frame, None, fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame1 = img1[:, :, ::-1]
            rgb_small_frame2 = img2[:, :, ::-1]

            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations1 = face_recognition.face_locations(rgb_small_frame1)
                face_encodings1 = face_recognition.face_encodings(rgb_small_frame1, face_locations1)

                face_loginId1 = []
                for face_encoding in face_encodings1:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        face_loginId = known_face_loginId[first_match_index]

                        trackingVO.trackingPlace = "Lab No.1"
                        trackingVO.trackingTime = str(datetime.now().hour) + ':' + str(datetime.now().minute)
                        trackingVO.tracking_LoginId = face_loginId

                        trackingDAO.updateTracking(trackingVO)

                    face_loginId1.append(face_loginId)

                face_locations2 = face_recognition.face_locations(rgb_small_frame2)
                face_encodings2 = face_recognition.face_encodings(rgb_small_frame2, face_locations2)

                face_loginId2 = []
                for face_encoding in face_encodings2:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        face_loginId = known_face_loginId[first_match_index]

                        trackingVO.trackingPlace = "Lab No.2"
                        trackingVO.trackingTime = str(datetime.now().hour) + ':' + str(datetime.now().minute)
                        trackingVO.tracking_LoginId = face_loginId

                        trackingDAO.updateTracking(trackingVO)

                    face_loginId2.append(face_loginId)
                print "face names1@@@@@@@@", face_loginId1
                print "face names2########", face_loginId2
            process_this_frame = process_this_frame

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

        return redirect('/loadIndex')

    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')


@app.route('/viewTracking')
def viewTracking():
    if session['sessionloginRole'] == 'admin':

        departmentDAO = DepartmentDAO()
        departmentVO = DepartmentVO()

        departmentVO.departmentActiveStatus = 'activate'

        departmentDict = departmentDAO.searchDepartment(departmentVO)

        return render_template('admin/viewDetection.html', departmentDict=departmentDict)

    elif session['sessionloginRole'] == 'user':

        departmentDAO = DepartmentDAO()
        departmentVO = DepartmentVO()

        departmentVO.departmentActiveStatus = 'activate'

        departmentDict = departmentDAO.searchDepartment(departmentVO)

        return render_template('user/viewDetection.html', departmentDict=departmentDict)


@app.route('/ajaxRoleTracking')
def ajaxRoleTracking():
    roleDAO = RoleDAO()
    roleVO = RoleVO()
    roleVO.role_DepartmentId = request.args.get('tracking_DepartmentId')

    roleVO.role_DepartmentId = roleVO.role_DepartmentId[1:len(roleVO.role_DepartmentId) - 1]

    ajaxRoleTrackingDict = roleDAO.ajaxRoleTracking(roleVO)

    jsn = json.dumps(ajaxRoleTrackingDict)

    return jsn


@app.route('/ajaxLoadTracking')
def ajaxLoadTracking():
    trackingDAO = TrackingDAO()
    trackingVO = TrackingVO()

    trackingVO.tracking_RoleId = request.args.get('tracking_RoleId')
    trackingDict = trackingDAO.searchAjaxTracking(trackingVO)
    print trackingDict
    response = jsonify(trackingDict)

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
