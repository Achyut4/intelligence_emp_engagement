from flask import render_template, redirect, request, session, url_for
from project import app
from project.com.dao.AttendanceDAO import AttendanceDAO
from project.com.vo.AttendanceVO import AttendanceVO
from project.com.dao.LogDAO import LogDAO
from project.com.vo.LogVO import LogVO
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

        video_capture = "http://25.132.49.167:8080/shot.jpg"
        all_face_encoding = {}
        try:
            with open(
                    'C:/Users/Dell/PycharmProjects/intelligence_emp_engage/project/static/adminResources/dataset/model/dataset_faces.dat',
                    'rb') as f:
                all_face_encoding = pickle.load(f)

            known_face_encodings = np.array(list(all_face_encoding.values()))
            known_face_registerId = list(all_face_encoding.keys())

        except:
            return render_template('admin/index.html', ErrorDatasetDictDict="Please Enter Atleast One Dataset")
        face_locations = []
        face_encodings = []
        face_registerId = []
        process_this_frame = True

        while True:
            imgResp = urllib.urlopen(video_capture)
            imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
            img = cv2.imdecode(imgNp, -1)
            img = cv2.flip(img, -1)

            font = cv2.FONT_HERSHEY_SIMPLEX
            topLeftCornerOfText = (50, 30)
            fontScale = 1
            fontColor = (0, 0, 255)
            lineType = 2

            cv2.putText(img, 'Press q to stop',
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
                        attendanceVO.attendance_LoginId = known_face_registerId[first_match_index]
                        logVO.log_LoginId = attendanceVO.attendance_LoginId
                        # print logVO.log_LoginId
                        if attendanceVO.attendance_LoginId in face_registerId:
                            # if same person come's in frame then it will continue the loop and duplicate value will not insert into table
                            continue
                        # When new person comes data will be added to list
                        face_registerId.append(attendanceVO.attendance_LoginId)
                        print "Match Found Person Register Id is:-{0}".format(logVO.log_LoginId)
                        print face_registerId

                        logVO.logDate = str(datetime.today().strftime("%d-%m-%y"))
                        logDict = logDAO.searchDuplicateLog(logVO)
                        if len(logDict) != 0:
                            continue

                        attendanceVO.attendanceDate = str(datetime.today().strftime("%d-%m-%y"))
                        attendanceVO.attendanceTime = str(datetime.now().hour) + ':' + str(datetime.now().minute)
                        attendanceVO.attendanceStatus = "present"
                        attendanceVO.attendanceActiveStatus = "activate"
                        attendanceDAO.updateAttendance(attendanceVO)
                        logVO.logDate = str(datetime.today().strftime("%d-%m-%y"))
                        logVO.logTime = str(datetime.now().hour) + ':' + str(datetime.now().minute)
                        logVO.log_LoginId = logVO.log_LoginId
                        logDAO.insertlog(logVO)
            process_this_frame = process_this_frame

            # Display the results
            # for (top, right, bottom, left), name in zip(face_locations, face_names):
            #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            #     top *= 4
            #     right *= 4
            #     bottom *= 4
            #     left *= 4
            #
            #     # Draw a box around the face
            #     cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
            #
            #     # Draw a label with a name below the face
            #     cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            #     font = cv2.FONT_HERSHEY_DUPLEX
            #     cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            #
            # # img = cv2.flip(img, -1)
            # # cv2.imshow('IPWebCam', img)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

        return render_template('admin/index.html')

    else:
        return render_template('admin/login.html', loginerrorDict='Please login first')


@app.route('/viewAttendance')
def viewAttendance():
    try:
        if session['sessionloginRole'] == 'admin':
            logDAO = LogDAO()
            logVO = LogVO()

            logVO.logDate = str(datetime.today().strftime("%d-%m-%y"))
            logDict = logDAO.searchLog(logVO)

            return render_template('admin/viewAttendance.html', logDict=logDict,
                                   dateDict=logVO.logDate)

        if session['sessionloginRole'] == 'user':
            attendanceDAO = AttendanceDAO()
            attendanceVO = AttendanceVO()

            print session['sessionloginId']
            print session['sessionloginRole']
            attendanceVO.attendance_LoginId = str(session['sessionloginId'])
            print attendanceVO.attendance_LoginId
            attendanceVO.attendanceDate = str(datetime.today().strftime("%d-%m-%y"))
            attendanceDict = attendanceDAO.searchUserAttendance(attendanceVO)

            print attendanceDict

            return render_template('user/viewAttendance.html', attendanceDict=attendanceDict,
                                   dateDict=attendanceVO.attendanceDate)


        else:
            return render_template('admin/login.html', loginerrorDict='Please login first')

    except:
        return render_template('admin/login.html', loginerrorDict='Please login first')
