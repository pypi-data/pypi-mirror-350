import cv2
import numpy as np


def reproject_with_equalized_xy_scale_safe(
    image_path, calib_result, pattern_size=(4, 9), output_spacing_px=20, max_dim=3000
):
    img = cv2.imread(image_path)
    h, w = img.shape[:2]

    # 1. Undistort image using calibration
    undistorted = cv2.undistort(
        img, calib_result["camera_matrix"], calib_result["dist_coeffs"]
    )

    # 2. Generate unit-spaced asymmetric grid
    objp = []
    for i in range(pattern_size[1]):  # rows
        for j in range(pattern_size[0]):  # cols
            x = (2 * j + i % 2) * 0.5
            y = i
            objp.append([x, y])
    objp = np.array(objp, dtype=np.float32)

    # 3. Project pattern to image
    projected_points, _ = cv2.projectPoints(
        np.hstack((objp, np.zeros((len(objp), 1)))),  # Z=0
        calib_result["rvec"],
        calib_result["tvec"],
        calib_result["camera_matrix"],
        calib_result["dist_coeffs"],
    )
    projected_points = projected_points.reshape(-1, 2)

    # 4. Equalize XY scale
    xs = objp[:, 0]
    ys = objp[:, 1]
    spacing_x = np.mean(np.diff(np.unique(xs)))
    spacing_y = np.mean(np.diff(np.unique(ys)))
    scale_factor = spacing_x / spacing_y
    normalized_objp = objp.copy()
    normalized_objp[:, 1] *= scale_factor

    # 5. Create ideal grid in pixels
    ideal_points = normalized_objp * output_spacing_px

    # 6. Compute homography from distorted → ideal
    H, _ = cv2.findHomography(projected_points, ideal_points)

    # 7. Compute canvas size and prevent memory overflow
    corners = np.array(
        [[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], np.float32
    ).reshape(-1, 1, 2)
    warped_corners = cv2.perspectiveTransform(corners, H).reshape(-1, 2)
    min_xy = np.floor(np.min(warped_corners, axis=0)).astype(int)
    max_xy = np.ceil(np.max(warped_corners, axis=0)).astype(int)
    size = (max_xy - min_xy).astype(int)

    # 8. Scale down if needed to fit max canvas size
    scale = min(max_dim / size[0], max_dim / size[1], 1.0)
    final_size = (int(size[0] * scale), int(size[1] * scale))

    # 9. Combine shift and scale transforms
    T = np.array([[1, 0, -min_xy[0]], [0, 1, -min_xy[1]], [0, 0, 1]], dtype=np.float32)
    S = np.array([[scale, 0, 0], [0, scale, 0], [0, 0, 1]], dtype=np.float32)
    H_adjusted = S @ T @ H

    # 10. Warp the final image
    result = cv2.warpPerspective(undistorted, H_adjusted, final_size)
    return result
