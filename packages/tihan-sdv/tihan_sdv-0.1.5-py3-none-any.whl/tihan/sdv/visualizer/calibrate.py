import cv2
import numpy as np

# Define the chessboard dimensions
chessboard_rows = 6
chessboard_cols = 8

# Prepare object points
objp = np.zeros((chessboard_rows * chessboard_cols, 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_cols, 0:chessboard_rows].T.reshape(-1, 2)

# Arrays to store object points and image points
objpoints = []
imgpoints = []

# Capture images for calibration
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (chessboard_cols, chessboard_rows), None)
    
    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)
        cv2.drawChessboardCorners(frame, (chessboard_cols, chessboard_rows), corners, ret)
    
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Calibrate the camera
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Save the calibration data
np.savez('calibration_data.npz', mtx=mtx, dist=dist)

print("Calibration data saved to calibration_data.npz")