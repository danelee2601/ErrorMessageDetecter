# Description
 It detects an error message (pop-up window), and notifies the user by email. <br>
 Initially made to detect an error message pop-up window during simulation in the commercial software "ANSYS-FLUENT". <br>
 Howver, later it was developed expanding its use to detect any popup window message for a general use. <br>
 <br>
 For the convience of use, it is made in a GUI form.<br>
 
# Dependency (Names of Libraries)
  tkinter, numpy, matplotlib, cv2
  
# Quick Start
<b>[NOTE] Two three to do in advance (These are simple. No worries.)</b> <br>
(a) Allow the SMTP use in the naver mail to send an email with python: https://qkqhxla1.tistory.com/804 <br>
(b) Download the naver mail app on your phone: http://blog.naver.com/PostView.nhn? blogId=wldms3512&logNo=220567926748&parentCategoryNo=&categoryNo=21&viewDate=&isShowPopularPosts=true&from=search <br>
(c) Get an image file of the error message of yours. (you can use the snipping tool(=캡쳐도구)) (NOTE: Don't change the scale of the image!) <br>

<br>

<img src="ErrorMessageDetecter/images/a01.PNG"> <br>
1. If you execute 'ErrorMessageDetecter_GUI.py', you will see this window. <br>

<img src="ErrorMessageDetecter/images/a02.PNG"> <br>
2. Click 'open an image', and choose the image of the error message. <br>

<img src="ErrorMessageDetecter/images/a03.PNG"> <br>
3. It's the window with the image file uploaded. <br>

<img src="ErrorMessageDetecter/images/a09.PNG"> <br>
4. Type your Naver id, password and detection period (= how often you want the detecter to detect.) [in seconds] <br>
- FYI. If 'Detection Plot Option' is checked, when the error message is detected, the program will show where it finds the message by a red square. But you don't have to check it. Not necessary at all. <br>

<img src="ErrorMessageDetecter/images/a05.PNG"> <br>
5. The Detecter is running ... <br>

<img src="ErrorMessageDetecter/images/a06-1.PNG"> <br>
6. if the detecter finds the error message, it prints "Detected!" and sends a notification email to your Naver email account. <br>

<img src="ErrorMessageDetecter/images/a08.PNG"> <br>
7. The notification email. <br>

