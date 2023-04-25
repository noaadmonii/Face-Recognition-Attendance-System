import cv2
import math
import os
import face_recognition
import numpy as np


class FaceRecognition:
    #same order of users in each list
    user_faces_encoded = []
    usernames = []

    def __init__(self):
        self.encodeKnownUsers()

    def identifyUser(self, video_cap):
        if len(self.usernames) == 0:
            return 'Empty DB'
        
        ret, frame = video_cap.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        #face_recognition works with RGB and cv2 with BGR
        small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        unknown_face_location = face_recognition.face_locations(small_frame)
        if len(unknown_face_location) == 0:
            return 'No faces detected'
        if len(unknown_face_location) > 1:
            return 'More than one face detected'

        unknown_face_encoded = face_recognition.face_encodings(small_frame, unknown_face_location)[0]
        

        possible_matches = face_recognition.compare_faces(self.user_faces_encoded, unknown_face_encoded, tolerance=0.4)
        dist_array = face_recognition.face_distance(self.user_faces_encoded, unknown_face_encoded)

        closest_match_idx = np.argmin(dist_array)
        if possible_matches[closest_match_idx]:
            return self.usernames[closest_match_idx]
        else:
            return 'No good match'
        
    def encodeKnownUsers(self):
        for img in os.listdir('db'):
            user_image_path = face_recognition.load_image_file('./db/{}'.format(img))
            self.user_faces_encoded.append(face_recognition.face_encodings(user_image_path)[0])
            self.usernames.append(img[0:-4])


