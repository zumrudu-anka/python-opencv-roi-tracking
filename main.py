import numpy as np
import cv2

def run_main():

    videoName = "crosswalk"
    cap = cv2.VideoCapture(f'./resources/inputs/videos/{videoName}.avi')

    # Read the first frame of the video
    ret, frame = cap.read()

    # Set the ROI (Region of Interest). Actually, this is a
    # rectangle of the building that we're tracking

    if videoName == "crosswalk":
        c, r, w, h = 1080, 500, 30, 90
    
    elif videoName == "fourway":
        c, r, w, h = 1530, 150, 380, 895

    track_window = (c, r, w, h)
    
    # Create mask and normalized histogram
    roi = frame[r:(r + h), c:(c + w)]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, np.array((0., 30., 32.)), np.array((180., 255., 255.)))
    roi_hist = cv2.calcHist([hsv_roi], [0], mask, [185], [0, 185])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    # Setup the termination criteria, either 80 iteration or move by atleast 1 pt
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1)
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0,180], 1)

        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        x, y, w, h = track_window
        cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)

        cv2.putText(frame, 'Tracked', (x - 25, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        cv2.imshow('Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_main()