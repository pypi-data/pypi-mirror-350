import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = "/Users/alexandrequintart/Downloads/IMG_3837.jpeg"
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Define pattern size based on the image details (4x9)
pattern_size = (4, 9)

# Try to detect the pattern
found_chessboard, corners_chessboard = cv2.findChessboardCorners(gray, pattern_size)

found_circles_grid, centers_circles_grid = cv2.findCirclesGrid(
    gray, pattern_size, flags=cv2.CALIB_CB_SYMMETRIC_GRID
)

found_asymmetric_grid, centers_asymmetric_grid = cv2.findCirclesGrid(
    gray, pattern_size, flags=cv2.CALIB_CB_ASYMMETRIC_GRID
)

# Visualize the result
if found_chessboard:
    cv2.drawChessboardCorners(image, pattern_size, corners_chessboard, found_chessboard)
    detected_pattern = "Chessboard"

elif found_circles_grid:
    cv2.drawChessboardCorners(image, pattern_size, centers_circles_grid, found_circles_grid)
    detected_pattern = "Symmetric Circles Grid"

elif found_asymmetric_grid:
    cv2.drawChessboardCorners(image, pattern_size, centers_asymmetric_grid, found_asymmetric_grid)
    detected_pattern = "Asymmetric Circles Grid"

else:
    detected_pattern = "No pattern detected"

# Show the detected pattern
plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title(f"Detected Pattern: {detected_pattern}")
plt.axis("off")
plt.show()

# Return detection results
detected_pattern