# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cv2 as cv
import cv2.aruco
import numpy as np
from numpy.matlib import zeros


def check_opencv():
    print("OpenCV:", cv.__version__)
    img = np.zeros((120, 400, 3), dtype=np.uint8)
    cv.putText(img, "OpenCV OK", (10, 80), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    # If you installed a non-headless build, you can display a window:
    cv.imshow("hello", img); cv.waitKey(0)
    # Always safe (headless or not): save to file
    # cv.imwrite("hello.png", img)

# The docs for the ArucoTag module can be found here: https://docs.opencv.org/4.12.0/de/d67/group__objdetect__aruco.html#ga2ad34b0f277edebb6a132d3069ed2909
# This is an official tutorial for OpenCV: https://docs.opencv.org/4.12.0/d5/dae/tutorial_aruco_detection.html
#   It uses C++, but the Python API is very similar. If you click on the functions they mention, you can see what they look like in python
# Some notes on python:
#   def my_func(a: int, b: cv2.typing.MatLike) -> cv2.typing.MatLike:
#       ...
#   a is an argument of type int
#   my_func expects b to be of type cv2.typing.MatLike. This is a generic way to return to things openCV treats as multi-dimensional arrays
#       - If you see just cv2.typing.MatLike, it'll probably be expecting an image or frame of some kind
#       - otherwise, it may just be a list of some kind, like a list of coordinates, etc.
#   the -> cv2.typing.MatLike means the function will return something that is MatLike. Once again, this might be an image, or like an array, etc.
def training_task():
    pass
    # TODO: 1) Capture a video stream from your webcam - done done done
    # Hint: just search "capture video feed opencv" in google
    # Hint: this should be a few lines (1 to set up the capture, and a few to check if it opened)

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
        
    while True:

        # Capture frame-by-frame
        ret, frame = cap.read()
 
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        # TODO: 2) Repeatedly read a frame from your videocapture device

        # This will display the video feed
        # Comment out the if-else once you move onto the next part
        # cv.imshow("Webcam Feed", frame)
        # if cv.waitKey(1) == ord('q'): break
        # else: continue

        
        # TODO: 3) Now you you'll do the aruco tag stuff;
        annotated_frame = frame.copy()
        
        # TODO: 3.1) Create your detector
        # Hint: Use cv.aruco.DICT_6X6_100 as your dictionary
        # Look into the ArucoDetector(...), DetectorParameters(...), getPredefinedDictionary(...) methods from cv.aruco

        aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_100)
        parameters = cv.aruco.DetectorParameters()
        
        detector = 	cv.aruco.ArucoDetector(aruco_dict, parameters)
        
        # TODO: 3.2) Use your detector to find the markers
        
        corners, ids, rejected = detector.detectMarkers(annotated_frame)

        # TODO: 3.3) Draw rectangles around your markers
        for corner in corners:
            top_left = (int(corner[0][0][0]), int(corner[0][0][1]))
            bottom_right = (int(corner[0][2][0]), int(corner[0][2][1]))
            
            cv.rectangle(annotated_frame, top_left, bottom_right, (0, 255, 0), 2)
        
        # TODO: 4) Draw a circle at the center point (or average) of all the tags
        if ids is not None:

            # TODO: 4.1) Find the centers of each tag (there may/should be multiple tags)
            # Hint: Look at what format the marker detection gives marker positions in
            #       Use print(x) to get an idea of the format you get the.
            #       You may need to do a few levels of array accesses to get to what you need
            # Hint: The midpoint of several points is the average, the center of a square is the average of the corners
            # Hint: Be careful with types: pixel coordinates should be integers.
            #       For this training using int(x) to turn x into an integer is fine
            centers = []
            
            # Loop over each set of corners (each list should correspond to 1 tag):
            for corner in corners:
                #reset the corner coordinate list
                cornerList = []
                for i in range(4):
                    #gets the x,y coordinate of each corner
                    cornerList.append( (int(corner[0][i][0]), int(corner[0][i][1])) )
                
                #unpacks tuple into x and y to find average
                for x, y in cornerList:
                    xTotal += x
                    yTotal += y
                    
                #average of corners = the center
                centerX = xTotal / 4
                centerY = yTotal / 4
                
                #draws circle at center
                cv.circle(annotated_frame, (centerX, centerY), 50, (0,0,255), 2)
                #adds values to the centers list as tuple
                centers.append( (centerX, centerY) )
            
            # for corner_outer_array in corners:
                # Find the middle of that tag

                # draw a circle at the center of the aruco tag
                # use cv.circle(...) to draw a smallish circle
                # continue


            # TODO: 4.2) Find the center point of the centers of all the tags, if you found 4 tags
            # Hint: This will look almost identical to the previous step, but without the weirdly nested arrays
            if len(centers) == 4:
                # Draw a circle at the point at the average position of all 4 tags
                for centerXCoords, centerYCoords in centers:
                    xTotal += centerXCoords
                    yTotal += centerYCoords
                    
                globalCenterX = xTotal / 4
                globalCenterY = yTotal / 4
                
                cv.circle(annotated_frame, (globalCenterX, globalCenterY), 50, (0,0,255), 2)

        # Draw your frame, with all of your annotations
        cv.imshow('Annotated Frame', annotated_frame)
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # check_opencv()
    training_task()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
