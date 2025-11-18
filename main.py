import cv2
import numpy as np


low = np.array([20, 100, 100])
high = np.array([40, 255, 255])


camera = cv2.VideoCapture(0)
fps = 60

size = (int(cv2.CAP_PROP_FRAME_WIDTH), int(cv2.CAP_PROP_FRAME_HEIGHT))

video = cv2.VideoWriter("video.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, size)


while (True):
    succes, frame = camera.read()
    if not succes:
        break
    video.write(frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, low, high)

    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.erode(mask,kernel,iterations = 10)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        for contour in contours:
            ((x, y), radius) = cv2.minEnclosingCircle(contour)
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
    #cv2.imshow('Ball', frame)

    cv2.imshow('Mask', mask)



    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
video.release()
cv2.destroyAllWindows()