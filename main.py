import cv2
import os.path
import face_recognition
import tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk
import calendar
import time


from face_recognition_helper import FaceRecognition
from attendance_manager import AttManager

class AttendanceSystem:
    fr_inst = FaceRecognition()
    att_manager = AttManager()
    type_of_log = 'arrival'  #could be arrival or exit

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("900x520+200+80")
        self.main_window.title("Attendance System")
        self.main_window.configure(bg='white')

        self.welcome_label = tk.Label(self.main_window, text='Welcome!', font=("Arial", 25), bg='white', fg='green')
        self.welcome_label.config( justify="center")
        self.welcome_label.place(x=670, y= 180)

        self.login_button = tk.Button(self.main_window, text='Log In', fg='white', activebackground='pink', bg='blue',height=2, width=20, command=self.loginUser)
        self.login_button.place(x=670, y= 260)

        self.newuser_button = tk.Button(self.main_window, text='New User', fg='white', activebackground='pink', bg='lightblue',height=2, width=20, command=self. createNewUser)
        self.newuser_button.place(x=670, y= 340)

        self.webcam_label = tk.Label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=600, height=500)

        self.add_webcam()


    #The function creates the graphics for the 'new user' window
    def createNewUser(self):
        tk.messagebox.showinfo(title='Alert', message='Press \"Okay\" when you\'re ready to take your picture!')

        self.new_user_window = tk.Toplevel(self.main_window)
        self.new_user_window.geometry("900x520+200+80")
        self.new_user_window.title("Taking a picture")
        self.new_user_window.configure(bg='white')

        self.enter_name_label = tk.Label(self.new_user_window, text='Enter your name \nhere', font=("Arial", 20), bg='white', fg='green')
        self.enter_name_label.config( justify="center")
        self.enter_name_label.place(x=660, y= 100)

        self.new_user_webcam_label = tk.Label(self.new_user_window)
        self.new_user_webcam_label.place(x=10, y=0, width=600, height=500)

        self.new_user_img = self.most_recent_capture_pil
        self.new_user_img = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        
        self.new_user_webcam_label.configure(image=self.new_user_img)
        self.new_user_webcam_label.image = self.new_user_img

        self.username_text_box = tk.Text(self.new_user_window ,height=2, width=20)
        self.username_text_box.place(x=670, y= 180)

        self.addpicture_button = tk.Button(self.new_user_window, text='Register', fg='white', activebackground='pink', bg='blue',height=2, width=20, command=self.addPictureToDB)
        self.addpicture_button.place(x=670, y= 260)

        self.tryagain_button = tk.Button(self.new_user_window, text='Try Again', fg='white', activebackground='pink', bg='lightblue',height=2, width=20, command=self.destroyNewUserWin)
        self.tryagain_button.place(x=670, y= 340)


    #Closes the new user window when we're done with it.
    def destroyNewUserWin(self):
        self.new_user_window.destroy()
    

    #Creates an object that captures the video stream, then calls a function to process it.
    def add_webcam(self):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self.process_webcam()


    #The function that creates the simulation of a live video, presenting new a frame every 20ms.
    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        
        self.webcam_label.configure(image=imgtk)
        self.webcam_label.image = imgtk

        self.webcam_label.after(20, self.process_webcam)
        self.new_user_img_arr =  self.most_recent_capture_arr.copy()


    #Called when a new user wants to save his picture to the data base
    def addPictureToDB(self):
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.new_user_name = self.username_text_box.get("1.0",'end-1c')
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(self.new_user_name)), self.new_user_img_arr)

        self.fr_inst.encodeKnownUsers()

        tk.messagebox.showinfo(title='Alert', message='You\'re in! All you need to do now is to log in!')
        self.new_user_window.destroy()


    #Called when a user presses the login button on the main window
    def loginUser(self):
        self.new_arrival_or_exit_window = tk.Toplevel(self.main_window)
        self.new_arrival_or_exit_window.geometry("370x280+260+100")
        self.new_arrival_or_exit_window.configure(bg='white')

        self.arrival_or_exit_label = tk.Label(self.new_arrival_or_exit_window, text='Are you arriving or exiting?', font=("Arial", 12), bg='white', fg='green')
        self.arrival_or_exit_label.config( justify="center")
        self.arrival_or_exit_label.place(x=90, y= 100)

    

        self.arriving_button = tk.Button(self.new_arrival_or_exit_window, text='Arriving', fg='white', activebackground='pink', bg='blue',height=2, width=10, command=lambda: self.updateTypeOfLog('arrival'))
        self.arriving_button.place(x=80, y= 150)

        self.exiting_button = tk.Button(self.new_arrival_or_exit_window, text='Exiting', fg='white', activebackground='pink', bg='lightblue',height=2, width=10, command=lambda: self.updateTypeOfLog('exit'))
        self.exiting_button.place(x=180, y= 150)


        #recognition_res = self.fr_inst.identifyUser(self.cap)

        #if recognition_res == 'No faces detected':
         #   tk.messagebox.showinfo(title='Alert', message='No faces detected, please try again.')
        #elif recognition_res == 'More than one face detected':
         #   tk.messagebox.showinfo(title='Alert', message='More than one face detected, please try again alone!')
        #elif recognition_res == 'No good match':
         #   tk.messagebox.showinfo(title='Alert', message='No good match, please try again or create new user.')
        #else:
         #   tk.messagebox.showinfo(title='Alert', message='hi {}! Good to see you!'.format(recognition_res))
          #  curr_time = time.gmtime()
           # hour_minute_log = "{:d}:{:02d}".format(curr_time.tm_hour, curr_time.tm_min)
            #date = "{}-{}-{}".format(curr_time.tm_mday, curr_time.tm_mon, curr_time.tm_year)
            #self.att_manager.addToAttendanceSheet(recognition_res, hour_minute_log, date, self.type_of_log)

    def recognizeUser(self):
        recognition_res = self.fr_inst.identifyUser(self.cap)

        if recognition_res == 'No faces detected':
            tk.messagebox.showinfo(title='Alert', message='No faces detected, please try again.')
        elif recognition_res == 'More than one face detected':
            tk.messagebox.showinfo(title='Alert', message='More than one face detected, please try again alone!')
        elif recognition_res == 'Empty DB':
            tk.messagebox.showinfo(title='Alert', message='My Data Base is Empty! Create New users!')
        elif recognition_res == 'No good match':
            tk.messagebox.showinfo(title='Alert', message='No good match, please try again or create new user.')
        else:
            if self.type_of_log == 'arrival':
                tk.messagebox.showinfo(title='Alert', message='Hi {}! Good to see you!'.format(recognition_res))
            elif self.type_of_log == 'exit':
                tk.messagebox.showinfo(title='Alert', message='Bye {}!'.format(recognition_res))
            curr_time = time.gmtime()
            hour_minute_log = "{:d}:{:02d}".format(curr_time.tm_hour, curr_time.tm_min)
            date = "{}-{}-{}".format(curr_time.tm_mday, curr_time.tm_mon, curr_time.tm_year)
            self.att_manager.addToAttendanceSheet(recognition_res, hour_minute_log, date, self.type_of_log)
    
    
    def updateTypeOfLog(self, log_type):
        self.type_of_log = log_type
        self.recognizeUser()
        self.new_arrival_or_exit_window.destroy()

    #def userArriving(self):
    #    self.type_of_log = 'arrival'
       # self.recognizeUser()

   # def userExiting(self):
    #    self.type_of_log = 'exit'
      #  recognition_res = self.fr_inst.identifyUser(self.cap)


    def start_run(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    attSys = AttendanceSystem()
    attSys.start_run()