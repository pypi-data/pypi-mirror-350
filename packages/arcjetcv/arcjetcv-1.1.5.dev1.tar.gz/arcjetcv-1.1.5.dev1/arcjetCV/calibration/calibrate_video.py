def apply_calibration(frame, calibration_data):
    """
    Apply calibration to a single frame using provided calibration data.

    Args:
        frame (numpy.ndarray): The input frame (image) to calibrate.
        calibration_data (dict): A dictionary containing calibration data with keys:
            - "camera_matrix": The intrinsic camera matrix.
            - "dist_coeffs": The distortion coefficients.
            - "rvec" (optional): The rotation vector for 3D transformations.
            - "tvec" (optional): The translation vector for 3D transformations.

    Returns:
        numpy.ndarray: The calibrated frame (image).
    """
    # Extract calibration data
    camera_matrix = np.array(calibration_data["camera_matrix"])
    dist_coeffs = np.array(calibration_data["dist_coeffs"])

    # Undistort the frame
    h, w = frame.shape[:2]
    new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(
        camera_matrix, dist_coeffs, (w, h), 1, (w, h)
    )
    undistorted_frame = cv2.undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)

    # Apply 3D transformations if rvec and tvec are available
    if "rvec" in calibration_data and "tvec" in calibration_data:
        rvec = np.array(calibration_data["rvec"])
        tvec = np.array(calibration_data["tvec"])

        # Define points on the image plane
        height, width = undistorted_frame.shape[:2]
        object_points = np.array([
            [0, 0, 0],
            [width, 0, 0],
            [width, height, 0],
            [0, height, 0]
        ], dtype=np.float32)

        # Project 3D points to the image plane
        image_points, _ = cv2.projectPoints(object_points, rvec, tvec, new_camera_matrix, None)

        # Compute the perspective transform
        src_points = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
        dst_points = np.float32(image_points[:, 0, :])
        perspective_transform = cv2.getPerspectiveTransform(src_points, dst_points)

        # Apply the perspective transformation
        calibrated_frame = cv2.warpPerspective(undistorted_frame, perspective_transform, (w, h))
    else:
        # If no 3D transformation data, return the undistorted frame
        calibrated_frame = undistorted_frame

    return calibrated_frame