"""
# Two Things to do
1. Allow the SMTP use in the naver mail to send an email with python: https://qkqhxla1.tistory.com/804
2. Set Real-time notification through the naver mail app: http://blog.naver.com/PostView.nhn?blogId=wldms3512&logNo=220567926748&parentCategoryNo=&categoryNo=21&viewDate=&isShowPopularPosts=true&from=search
"""
import sys
import tkinter as tk
from tkinter.ttk import Separator
from tkinter.filedialog import askopenfilename
from mss import mss
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import time
import smtplib


class ErrorMessageDetecter(object):

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("ErrorMessageDetecter by DaesooLee")

        # check if there's log-in info.
        isfile_login_info = os.path.isfile('log-in_info.txt')
        if isfile_login_info:
            with open('log-in_info.txt', 'r') as f:
                login_info = f.readlines()

            login_info2 = []
            for i in login_info:
                login_info2.append(i.replace('\n', ''))


        # row=0
        label_title = tk.Label(master=self.root, text="Error Message Window Detector", font="Times 12 bold", bg="white", relief=tk.RIDGE)
        label_title.grid(column=0, columnspan=3, row=0, sticky="nsew")

        # row=1
        label1 = tk.Label(master=self.root, text="Error window image file: ")
        label1.grid(column=0, row=1, sticky='e')

        self.label2 = tk.Label(master=self.root, text="path/file_name", width=20)
        self.label2.grid(column=1, row=1)
        self.label2.config(text="{}".format(login_info2[0])) if isfile_login_info else 0

        self.error_window_filename = ""
        if isfile_login_info:
            self.target_photo_filename = login_info2[0]
        else:
            self.target_photo_filename = ""
        button1 = tk.Button(master=self.root, text="open an image", command=self.open_a_file)
        button1.grid(column=2, row=1)

        # row=2
        separator1 = Separator(self.root, orient='horizontal')
        separator1.grid(column=0, columnspan=3, row=2)

        # row=3
        label_naver_id = tk.Label(master=self.root, text="Naver ID: ")
        label_naver_id.grid(column=0, row=3, sticky='e')

        self.entry_naver_id = tk.Entry(master=self.root, width=25)
        self.entry_naver_id.grid(column=1, columnspan=2, row=3, sticky='w')
        self.entry_naver_id.insert(10, "{}".format(login_info2[1])) if isfile_login_info else 0
        self.naver_id = self.entry_naver_id.get()

        # row=4
        label_naver_pw = tk.Label(master=self.root, text="Naver PW: ")
        label_naver_pw.grid(column=0, row=4, sticky='e')

        self.entry_naver_pw = tk.Entry(master=self.root, width=25)
        self.entry_naver_pw.grid(column=1, columnspan=2, row=4, sticky='w')
        self.entry_naver_pw.insert(10, "{}".format(login_info2[2])) if isfile_login_info else 0
        self.naver_pw = self.entry_naver_pw.get()

        # row=5
        label_detection_period = tk.Label(master=self.root, text="Detection Period [s]: ")
        label_detection_period.grid(column=0, row=5, sticky='e')

        self.entry_detection_period = tk.Entry(master=self.root, width=5)
        self.entry_detection_period.grid(column=1, columnspan=2, row=5, sticky='w')
        self.entry_detection_period.insert(10, "{}".format(login_info2[3])) if isfile_login_info else 0

        # row=6
        label_plot_option = tk.Label(master=self.root, text="Detection Plot Option: ")
        label_plot_option.grid(column=0, row=6, sticky='e')

        self.variable_checkbutton_plot_option = tk.IntVar()
        checkbutton_plot_option = tk.Checkbutton(master=self.root, variable=self.variable_checkbutton_plot_option)
        checkbutton_plot_option.grid(column=1, columnspan=2, row=6)

        # row=7
        button_execute = tk.Button(master=self.root, text="Execute the Detector", command=self.execute, bg="darkgray", fg="black")
        button_execute.grid(column=0, columnspan=3, row=7)

        # =========================================================================

        self.filename_screenshot = 'screenshot.png'
        self.arr_screenshot = self.get_arr_screenshot(cv2.IMREAD_GRAYSCALE)
        self.arr_screenshot_rgb = self.get_arr_screenshot(cv2.IMREAD_COLOR)

        self.template_matching_method = cv2.TM_CCOEFF_NORMED
        self.threshold = 0.9  #threshold
        #self.detecting_period = eval(self.entry_detection_period.get())

        self.st_time = time.time()

        self.run_time = None
        self.current_time = None
        self.detection_log = {'status': False, 'current_time': None}

        # =========================================================================

        self.root.mainloop()

    def open_a_file(self):
        # get the file name of the error window image file
        file_name = askopenfilename()
        self.error_window_filename = file_name
        self.target_photo_filename = self.error_window_filename

        # update the label2
        self.label2.config(text="{}".format(self.error_window_filename))

    def execute(self):
        # update the input variables
        self.detecting_period = eval(self.entry_detection_period.get())
        self.plot_option = self.variable_checkbutton_plot_option.get()  # plot_option

        self.naver_id = self.entry_naver_id.get()
        self.naver_pw = self.entry_naver_pw.get()

        # save the log-in info.
        with open('log-in_info.txt', 'w') as f:
            f.write("{}\n".format(self.target_photo_filename))
            f.write("{}\n".format(self.naver_id))
            f.write("{}\n".format(self.naver_pw))
            f.write("{}\n".format(self.detecting_period))

        self.arr_target_photo = self.get_arr_of_target_photo(cv2.IMREAD_GRAYSCALE)
        self.w, self.h = self.arr_target_photo.shape[::-1]  # w:width, h:height

        # run
        self.run()

    def get_arr_of_target_photo(self, cmap):
        # make a directory
        #isdir_ = os.path.isdir('C:/temp_DetectErrorMessage')
        #if not isdir_:
        #    os.mkdir('C:/temp_DetectErrorMessage')
        #    print("* New directory is generated for this program. [C:/temp_DetectErrorMessage]")

        # read the target photo image
        arr_target_photo = cv2.imread(self.target_photo_filename, cmap)

        return arr_target_photo

    def get_arr_screenshot(self, cmap):
        # get a screenshot
        with mss() as sct:
            sct.shot(output=self.filename_screenshot)

        # read the screenshot image
        arr_screenshot = cv2.imread(self.filename_screenshot, cmap)

        return arr_screenshot

    def template_matching(self):
        method = self.template_matching_method
        #try:
        # update self.arr_screenshot, self.arr_screenshot_rgb
        self.arr_screenshot = self.get_arr_screenshot(cv2.IMREAD_GRAYSCALE)
        self.arr_screenshot_rgb = self.get_arr_screenshot(cv2.IMREAD_COLOR)

        # matchTemplate from cv2
        res = cv2.matchTemplate(self.arr_screenshot, self.arr_target_photo, method)

        loc = np.where(res >= self.threshold)

        if loc[0].shape[0] != 0:

            if self.detection_log['status'] == False:
                print("* Detecting Period is met.")
                print("* Detected!")
                time.sleep(0.1)

                # send an email
                self.send_email()

                # update status, run_time
                self.detection_log['status'] = True
                self.detection_log['current_time'] = self.current_time

                if self.plot_option:
                    for pt in zip(*loc[::-1]):
                        cv2.rectangle(self.arr_screenshot_rgb, pt, (pt[0] + self.w, pt[1] + self.h), (0, 0, 255), 2)
                    cv2.imshow('result: ', self.arr_screenshot_rgb)
                    cv2.waitKey(7000)  # [ms]
                    cv2.destroyAllWindows()

                #
                while True:
                    restart_or_not = input("[NOTE] Would you like to restart the detection? (Y/N): ")

                    if (restart_or_not == 'Y') or (restart_or_not == 'y') or (restart_or_not == 'N') or (
                            restart_or_not == 'n'):
                        break

                if (restart_or_not == 'N') or (restart_or_not == 'n'):
                    self.root.quit()
                    self.root.destroy()
                    sys.exit()

                elif (restart_or_not == 'Y') or (restart_or_not == 'y'):
                    pass
            else:
                pass
        else:
            if self.detection_log['status'] == False:
                print("* Detecting Period is met.")
                print("* Cannot detect the error message window.\n")

                # update status, run_time
                self.detection_log['status'] = True
                self.detection_log['current_time'] = self.current_time

        #except:
        #    print("* [Error] \n")

    def run(self):
        while True:
            self.current_time = time.time()
            self.run_time = np.round(self.current_time - self.st_time, 0)

            if self.run_time % self.detecting_period == 0:

                # run the template_matching
                self.template_matching()

                if self.current_time != self.detection_log['current_time']:
                    self.detection_log['status'] = False

                time.sleep(1.0)

    def send_email(self):
        """
        # reference url: https://qkqhxla1.tistory.com/804
        """

        naver_id = self.naver_id  # 본인 네이버 메일. asdfasfas@naver.com과 같은 형식으로 입력한다.
        naver_pw = self.naver_pw  # 본인 네이버 계정 비밀번호 입력.

        FROM = naver_id

        TO = [naver_id]  # 보낼 메일 주소.  # 여기서는 자기자신한테 보냄

        SUBJECT = "[Simulation Diverged] Error message window was detected!"  # 한글을 보내려면 반드시 utf-8로 인코딩해야합니다.
        TEXT = " Your simulation divered.\nThe error message window was detected.\n Please check your simulation."

        # Prepare actual message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s

        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        try:
            server = smtplib.SMTP("smtp.naver.com", 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(naver_id, naver_pw)
            server.sendmail(FROM, TO, message)
            server.close()
            print('* successfully sent the email\n')

        except smtplib.SMTPException:
            print("* failed to send mail\n")


if __name__ == "__main__":
    # call the class
    gui = ErrorMessageDetecter()

