# Here we import "openCV2".
import cv2
# Here we import "time" to use sleep function for waiting during the loop.
import time
# Here we import os to ensure that the correct path for the xml files are used cross-os.
import os
# Here we import pymouse, a framework which makes manipulation of the mouse cursor possible.
from pymouse import PyMouse

# TODO: Implement eyes casacde

##########################! PLEASE NOTE !############################
#                   PLEASE NOTE This program requires pywin32 to run in Windows                         #
#           Sadly since pywin32 contains allot of C++ it cannot be installed through pip              #
#     Download PyWin executable from https://github.com/mhammond/pywin32/releases    #
#                   Works in Linux through pip packages included in requirements.txt                       #
#################################################################

# Here we download the nose cascade, face cascade and eye cascade file.
# This is the xml files that contains the code for recognizing  specific parts of the body.
# The file is obtained from :
# https://github.com/opencv/opencv_contrib/blob/master/modules/face/data/cascades/haarcascade_mcs_nose.xml
# Here we create a relative path so that the software can be used on different computers without getting path errors.
directory = os.path.dirname(__file__)
noseXML = os.path.join(directory, 'cascade/haarcascade_mcs_nose.xml')
faceXML = os.path.join(directory, 'cascade/haarcascade_frontalface_default.xml')
eyeXML = os.path.join(directory, 'cascade/eyes.xml')
nose_cascade = cv2.CascadeClassifier(noseXML)
face_cascade = cv2.CascadeClassifier(faceXML)
eye_cascade = cv2.CascadeClassifier(eyeXML)

# Here we set a variable m to PyMouse for later use.
m = PyMouse()

# Error handling for empty files, due to us not wanting to force user to install GTK or QT.
# These errors are displayed in the terminal instead.
# TODO: Do something else than cv2.destroyAllWindows() as windows are not live yet.
if nose_cascade.empty():
    raise IOError('Unable to load the nose cascade xml file')
    cv2.destroyAllWindows()

if face_cascade.empty():
    raise IOError('Unable to load the face cascade xml file')
    cv2.destroyAllWindows()

if eye_cascade.empty():
    raise IOError('Unable to load the eye cascade xml file')
    cv2.destroyAllWindows()

# Here we create a variable cap that contains the information about which camera the program is to use.
# In this case we have set it to 0 (expecting the user to use a integrated camera if they have one).
# IF the user is using external camera instead of an his/hers integrated one, we would have to change the input to 1.
cap = cv2.VideoCapture(0)
# Display_factor is set to 1 to keep the original size of the captured image..
# This however is an issue if screen has lower resolution  than the web cameras resolution.
# This factor will be used further down in the frame variable that contains cv2.resize.
ds_factor = 1

#  Here we start a loop that will continue until the Esc-button is pushed (27) .
while True:
    # Capture the frames right now.
    ret, frame = cap.read()
    # Flipping the image so that moving nose to the left equivalates to moving cursor left.
    frame = cv2.flip(frame, 1)
    # Re-size based on the factor from before.
    frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
    # Since the face-detector only works on black and white images we do a conversion to BGR2GRAY here.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    nose_rect = nose_cascade.detectMultiScale(gray, 1.3, 5)
    # Here we draw the square around the nose that is detected.
    x_dim, y_dim = m.screen_size()
    face_rect = face_cascade.detectMultiScale(gray, 1.3, 5)
    eye_rect = eye_cascade.detectMultiScale(gray, 1.3, 5)
    # Here we draw the square around the nose, face and eyes that is detected.
    if len(nose_rect) > 0:
        print("Only Nose at ", nose_rect)
        for (x, y, w, h) in nose_rect:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
            # m (the variable created before), should move the mouse using the x, and y variable from the nose rect.
            # We accelerate movement speed by 4 to make it possible to navigate the cursor through the whole screen.
            m.move(x * 4, y * 4)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                m.click(x * 4, y * 4, 1)
                print("CLICK")

        # TODO: Write and if that goes into face if nose is not visible
    elif len(face_rect) > 0:
        print("Only Face at ", face_rect)
        for (x, y, w, h) in face_rect:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
    elif len(face_rect) > 0:
        print("Only Eye at ", eye_rect)
        for (x, y, w, h) in eye_rect:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (205, 0, 0), 3)
    else:
        print("Nothing detected.")

    cv2.imshow('Rhino-Control', frame)

    # Waiting 1 millisecond to show the next frame.
    time.sleep(0.001)
    if cv2.waitKey(2) & 0xFF == ord('q'):
        # Exit on pressing 'q'.
        break
        # Exit on pressing 'q'.
# Here we release the web cam to be used by other programs before we shut down the program.
cap.release()
# Terminating the window the software is running in. 
cv2.destroyAllWindows()
cv2.waitKey(1)
