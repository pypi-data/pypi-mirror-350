import cv2
import numpy as np

# Load camera calibration data
data = np.load('calibration_data.npz')
mtx = data['mtx']
dist = data['dist']

# Parameters
steering_angle = 0
max_steering = 45
line_thickness = 4
car_width = 80
car_height = 160
track_offset = 40

# Load car image with alpha channel (RGBA)
car_img = cv2.imread('Resources/Images/maini_cart.png', cv2.IMREAD_UNCHANGED)
car_img = cv2.resize(car_img, (car_width, car_height))
car_img = cv2.rotate(car_img, cv2.ROTATE_180)

def blend_overlay(base_img, overlay_img, alpha=0.6):
    return cv2.addWeighted(base_img, 1 - alpha, overlay_img, alpha, 0)

def warp_overlay_points(points, h_ratio=0.002, v_ratio=0.002):
    warped = []
    for x, y in points:
        new_x = x + (x - 640//2) * h_ratio
        new_y = y + (y - 480//2) * v_ratio
        warped.append((int(new_x), int(new_y)))
    return warped

def draw_bezier_curve(img, p0, p1, p2, segments=30):
    h, w = img.shape[:2]
    warped_points = []

    for i in range(segments + 1):
        t = i / segments
        x = int((1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0])
        y = int((1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1])
        warped = warp_overlay_points([(x, y)])[0]  # Apply trapezoid-style warp
        warped_points.append(warped)

    for i in range(len(warped_points) - 1):
        color = get_zone_color(i, segments)
        cv2.line(img, warped_points[i], warped_points[i + 1], color, 4, lineType=cv2.LINE_AA)
def get_zone_color(index, total):
    ratio = index / total
    if ratio < 0.33:
        return (0, 255, 0)  # Green
    elif ratio < 0.66:
        return (0, 255, 255)  # Yellow
    else:
        return (0, 0, 255)  # Red

def draw_car_overlay(img):
    height, width = img.shape[:2]
    overlay = img.copy()

    car_x = width // 2 - car_width // 2
    car_y = height  - car_height - 5

    if car_x < 0 or car_y < 0 or car_x + car_width > width or car_y + car_height > height:
        return img

    alpha_car = car_img[:, :, 3] / 255.0
    for c in range(3):
        overlay[car_y:car_y+car_height, car_x:car_x+car_width, c] = (
            alpha_car * car_img[:, :, c] +
            (1 - alpha_car) * overlay[car_y:car_y+car_height, car_x:car_x+car_width, c]
        )

    return overlay
def draw_trajectory_lines(frame, steering_angle):
    height, width = frame.shape[:2]
    center_x = width // 2
    start_y = height - 250  # bottom of trapezoid
    curve_length = 300
    angle_rad = np.deg2rad(steering_angle)
    offset_x = int(np.sin(angle_rad) * 150)

    # Wider bottom (p0), narrower top (p2)
    bottom_width = int(width * 0.3)
    top_width = int(width * 0.1)

    for i, side in enumerate([-1, 1]):
        # Bottom start point (wider)
        p0 = (center_x + side * bottom_width // 2, start_y)

        # Top end point (narrower, slightly affected by steering)
        p2 = (center_x + side * top_width // 2 + offset_x, start_y - curve_length)

        # Control point - mid curve
        p1 = ((p0[0] + p2[0]) // 2 + offset_x // 2, (p0[1] + p2[1]) // 2)

        draw_bezier_curve(frame, p0, p1, p2)

    return frame


def put_steering_text(img, angle):
    cv2.putText(img, f"Steering Angle: {angle}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,255,150), 2)

def draw_dashed_arc(img, center, radius, angle=90, flip=False, color=(128, 128, 128)):
    num_dashes = 15
    thickness = 2
    dash_length = angle / num_dashes
    for i in range(num_dashes):
        start_angle = i * dash_length
        end_angle = start_angle + dash_length / 2
        if flip:
            start_angle, end_angle = 180 - end_angle, 180 - start_angle
        cv2.ellipse(img, center, (radius, radius), 0, start_angle, end_angle, color, thickness)

def draw_parking_overlay(frame):
    h, w = frame.shape[:2]
    bottom_width = int(w * 0.6)
    top_width = int(w * 0.2)
    height = int(h * 0.3)

    center_x = w // 2
    bottom_y = h - 250
    top_y = bottom_y - height

    # Parking trapezoid outline
    # pts = np.array([
    #     [center_x - bottom_width // 2, bottom_y],
    #     [center_x + bottom_width // 2, bottom_y],
    #     [center_x + top_width // 2, top_y],
    #     [center_x - top_width // 2, top_y]
    # ], np.int32)

    # cv2.polylines(frame, [pts], isClosed=True, color=(255, 0, 0), thickness=4)  # Blue
    # Draw only selected sides
    # Define points of the trapezoid
    pt1 = (center_x - bottom_width // 2, bottom_y)
    pt2 = (center_x + bottom_width // 2, bottom_y)
    pt3 = (center_x + top_width // 2, top_y)
    pt4 = (center_x - top_width // 2, top_y)

    warped_pts = warp_overlay_points([pt1, pt2, pt3, pt4])
    pt1, pt2, pt3, pt4 = warped_pts

    overlay = frame.copy()
    cv2.line(overlay, pt1, pt2, (255, 0, 0), 4)
    cv2.line(overlay, pt2, pt3, (255, 0, 0), 4)
    cv2.line(overlay, pt3, pt4, (255, 0, 0), 4)
    cv2.line(overlay, pt4, pt1, (255, 0, 0), 4)

    step = height // 3
    for i in range(1, 3):
        y = bottom_y - i * step
        width = int(bottom_width - (bottom_width - top_width) * (i * step / height))
        warped_line_pts = warp_overlay_points([(center_x - width // 2, y), (center_x + width // 2, y)])
        cv2.line(overlay, warped_line_pts[0], warped_line_pts[1], (0, 255, 255), 2)

    cv2.line(overlay, pt1, pt2, (0, 0, 255), 4)

    draw_dashed_arc(overlay, center=(center_x - 150, bottom_y + 100), radius=300, angle=90, color=(128, 128, 128))
    draw_dashed_arc(overlay, center=(center_x + 150, bottom_y + 100), radius=300, angle=90, flip=True, color=(128, 128, 128))

    frame[:] = blend_overlay(frame, overlay)

# Open camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    newcameramtx, _ = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1)
    undistorted = cv2.undistort(frame, mtx, dist, None, newcameramtx)

    # draw_static_guidelines(undistorted)
    draw_parking_overlay(undistorted)
    draw_trajectory_lines(undistorted, steering_angle)
    final_frame = draw_car_overlay(undistorted)
    put_steering_text(final_frame, steering_angle)

    cv2.imshow("Pro Parking Assist", final_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('a'):
        steering_angle = max(steering_angle - 3, -max_steering)
    elif key == ord('d'):
        steering_angle = min(steering_angle + 3, max_steering)
    elif key == ord('s'):
        steering_angle = 0

cap.release()
cv2.destroyAllWindows()
