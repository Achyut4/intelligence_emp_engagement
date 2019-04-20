from flask import render_template, redirect, request, session, url_for,flash
from project import app
from project.com.dao.AttendanceDAO import AttendanceDAO
from project.com.vo.AttendanceVO import AttendanceVO
from project.com.dao.LogDAO import LogDAO
from project.com.vo.LogVO import LogVO
from project.com.dao.TrackingDAO import TrackingDAO
from project.com.vo.TrackingVO import TrackingVO
from project.com.dao.RoleDAO import RoleDAO
from project.com.vo.RoleVO import RoleVO
import urllib
import cv2
import numpy as np
from datetime import datetime
import pickle
import face_recognition


@app.route('/startAttendance')
def startAttendance():
    if session['sessionloginRole'] == 'admin':

        attendanceDAO = AttendanceDAO()
        attendanceVO = AttendanceVO()
        logDAO = LogDAO()
        logVO = LogVO()
        roleDAO=RoleDAO()
        roleVO=RoleVO()
        trackingDAO=TrackingDAO()
        trackingVO=TrackingVO()

        video_capture = "http://25.62.180.52:8080/shot.jpg"

        all_face_encoding = {}
        try:
            with open(
                    'C:/Users/Dell/PycharmProjects/intelligence_emp_engage/project/static/adminResources/dataset/model/dataset_faces.dat',
                    'rb') as f:
                all_face_encoding = pickle.load(f)

            known_face_encodings = np.array(list(all_face_encoding.values()))
            known_face_loginId = list(all_face_encoding.keys())

        except:
            return redirect('/loadIndex')
        face_locations = []
        face_encodings = []
        face_registerId = []
        process_this_frame = True


        while True:
            try:
                imgResp = urllib.urlopen(video_capture)
            except:
                session['error']='Camera not connected'
                return redirect('/loadIndex')
            imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
            img = cv2.imdecode(imgNp, -1)
            img = cv2.flip(img, -1)

            font = cv2.FONT_HERSHEY_SIMPLEX
            topLeftCornerOfText = (50, 30)
            fontScale = 1
            fontColor = (0, 0, 255)
            lineType = 2

            cv2.putText(img, 'Press q to stop'+str(datetime.now()),
                            topLeftCornerOfText,
                            font,
                            fontScale,
                            fontColor,
                            lineType)

            cv2.imshow('IPWebCam', img)

            # frame = "http://192.168.43.120:8080/shot.jpg"

            # Resize frame of video to 1/4 size for faster face recognition processing
            # small_frame = cv2.resize(frame, None, fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = img[:, :, ::-1]

            if process_this_frame:
                #If there are many people we clear this list(For test purpose to remove it...)
                face_loginId=[]
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:

                        first_match_index = matches.index(True)
                        attendanceVO.attendance_LoginId = known_face_loginId[first_match_index]
                        logVO.log_LoginId = attendanceVO.attendance_LoginId
                        # print logVO.log_LoginId

                        if attendanceVO.attendance_LoginId in face_loginId:
                            # if same person come's in frame then it will continue the loop and duplicate value will not insert into table
                            continue
                        # When new person comes data will be added to list
                        face_loginId.append(attendanceVO.attendance_LoginId)
                        print "Match Found Person Login Id is:-{0}".format(logVO.log_LoginId)
                        print face_loginId

                        logVO.logDate = str(datetime.today().strftime("%d-%m-%Y"))
                        logDict = logDAO.searchDuplicateLog(logVO)
                        if len(logDict) != 0:
                            continue

                        attendanceVO.attendanceDate = str(datetime.today().strftime("%d-%m-%Y"))
                        attendanceVO.attendanceTime = str(datetime.now().hour) + ':' + str(datetime.now().minute)
                        attendanceVO.attendanceStatus = "present"
                        attendanceVO.attendanceActiveStatus = "activate"
                        attendanceDAO.updateAttendance(attendanceVO)

                        logVO.logDate = str(datetime.today().strftime("%d-%m-%Y"))
                        logVO.logTime = str(datetime.now().hour) + ':' + str(datetime.now().minute)

                        departmentDict = logDAO.searchlogDepartment(logVO)
                        logVO.log_DepartmentId = str(departmentDict[0]['register_DepartmentId'])
                        logVO.log_LoginId = logVO.log_LoginId

                        logDAO.insertlog(logVO)

                        roleVO.roleActiveStatus = "activate"
                        RoleDict = roleDAO.searchRole(roleVO)
                        if RoleDict[0]['roleName'] == 'Employee':
                            pass
                        else:
                            trackingVO.trackingPlace = "Entry Gate"
                            trackingVO.trackingTime = str(datetime.now().hour) + ':' + str(datetime.now().minute)
                            trackingVO.tracking_DepartmentId = str(RoleDict[0]['role_DepartmentId'])
                            trackingVO.tracking_RoleId = str(RoleDict[0]['roleId'])
                            trackingVO.tracking_LoginId = str(logVO.log_LoginId)

                            trackingDict=trackingDAO.searchTracking(trackingVO)
                            if len(trackingDict) == 0:

                                trackingDAO.insertTracking(trackingVO)
                            else:
                                trackingDAO.updateTracking(trackingVO)
            process_this_frame = process_this_frame

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

        return redirect('/loadIndex')

    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')


@app.route('/viewAttendance')
def viewAttendance():
    try:
        if session['sessionloginRole'] == 'admin':
            logDAO = LogDAO()
            logVO = LogVO()

            logVO.logDate = str(datetime.today().strftime("%d-%m-%Y"))
            logDict = logDAO.searchLog(logVO)

            return render_template('admin/viewAttendance.html', logDict=logDict,
                                   dateDict=logVO.logDate)

        if session['sessionloginRole'] == 'user':
            attendanceDAO = AttendanceDAO()
            attendanceVO = AttendanceVO()

            attendanceVO.attendance_LoginId = str(session['sessionloginId'])
            attendanceVO.attendanceDate = str(datetime.today().strftime("%d-%m-%Y"))
            attendanceDict = attendanceDAO.searchUserAttendance(attendanceVO)

            return render_template('user/viewAttendance.html', attendanceDict=attendanceDict,
                                   dateDict=attendanceVO.attendanceDate)


        else:
            return render_template('admin/login.html', loginerrorDict='Please login first')

    except:
        return render_template('admin/login.html', loginerrorDict='Please login first')
