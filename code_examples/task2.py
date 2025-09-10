from pyniryo import *
from pyniryo.vision import *
import cv2
import numpy as np
from pyniryo.vision import extract_img_workspace, relative_pos_from_pixels
from skimage.measure import regionprops, label

robot = NiryoRobot('169.254.200.200')

robot.calibrate_auto()

vision_pose = PoseObject(x = -0.0026, y = -0.1650, z = 0.3154, roll = -0.184, pitch = 1.370, yaw = 2.300)

robot.move_pose(vision_pose)

count = 0  # Initialize count outside the loop

try:
    while True:
        # Capture a compressed image from the robot's camera

        camera_intrinsics, distortion_coefficients = robot.get_camera_intrinsics()
        print("Camera Intrinsics:", camera_intrinsics)
        print("Distortion Coefficients:", distortion_coefficients)

        compressed_img = robot.get_img_compressed()

        # Decompress the image into a NumPy array
        img = uncompress_image(compressed_img)
        
        
                # Undistort the image
        undistorted_img = undistort_image(img, camera_intrinsics,distortion_coefficients)
        if undistorted_img is None or undistorted_img.size == 0:
            print("Error: Undistorted image is invalid.")
            continue
        # Extract the workspace
        workspace_img = extract_img_workspace(undistorted_img, workspace_ratio=1.0)
        # Display the image using OpenCV
        if workspace_img is None or workspace_img.size == 0:
            print("Error: Workspace image is invalid.")
            continue

        cv2.imshow("workspace Image", workspace_img)

         # HSV Thresholding
        thresh = threshold_hsv(workspace_img, [90, 85, 70], [125, 255, 255])

        # Morphological operation parameters
        morpho_type = MorphoType.OPEN
        kernel_shape = (11, 11)
        kernel_type = KernelType.ELLIPSE

        # Perform morphological transformations
        cleaned = morphological_transformations(thresh, morpho_type=morpho_type, kernel_shape=kernel_shape, kernel_type=kernel_type)
        # Find Contours
        contours = biggest_contours_finder(cleaned, nb_contours_max=5)

        # Draw contours on the workspace image
        for cnt in contours:
            cv2.drawContours(workspace_img, [cnt], -1, (0, 255, 0), 2)

        # Display the HSV and Contours
        cv2.imshow("HSV and Contours", cleaned)

        # Analyze Regions
        lbl_img = label(cleaned > 200)
        props = regionprops(lbl_img)
        for prop in props:
            circ = 4 * np.pi * prop.area / (prop.perimeter ** 2)
            if 0.70 < circ < 0.90:  # Square candidate
                print(f"Square detected with area: {prop.area}")

        # Approximate Contours for Polygon Shape
        for cnt in contours:
            poly = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
            if len(poly) == 4:  # Found a quadrilateral
                print("Quadrilateral detected")
        
        # Refresh the OpenCV window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Adjust unpacking to match the return structure of detect_object()
        detection_result = robot.detect_object("summer_school")
        if detection_result:
            detection_status, object_data = detection_result[0], detection_result[1:]
            if detection_status:
                relative_position, shape, color = object_data
                print(f"Detected {color} {shape} at {relative_position}")

                # Convert relative position to pixel coordinates
                print("length",workspace_img.shape[1] )
                print("width",workspace_img.shape[0] )
                center_x = int(relative_position[0] * workspace_img.shape[1])
                center_y = int(relative_position[1] * workspace_img.shape[0])
                rotation = relative_position[2]  # Rotation in radians

                # Convert pixel coordinates to relative position
                relative_position = (center_x, center_y)

                cx_rel, cy_rel = relative_pos_from_pixels(workspace_img, center_x, center_y)

                # Print the relative position
                print(f"pixel Position: {relative_position}")
                print(f"tranformed Position: {(cx_rel,cy_rel)}")


                print(f"Object Center (pixels): ({center_x}, {center_y})")
                print(f"Object Rotation (radians): {rotation}")

                # Draw the detected object on the workspace image
                cv2.circle(workspace_img, (center_x, center_y), 5, (0, 255, 0), -1)
                cv2.putText(workspace_img, f"Rotation: {rotation:.2f} rad", (center_x + 10, center_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    
except KeyboardInterrupt:
    print("Exiting program...")
finally:
    # Close OpenCV window and robot connection
    cv2.destroyAllWindows()
    robot.close_connection()




#backup

# if detection_result:
#             detection_status, *object_data = detection_result
#             if detection_status:
#                 relative_position, shape, color = object_data
#                 print(f"Detected {color} {shape} at {relative_position}")
#                 robot.move_to_object("summer_school", 0.08, ObjectShape.SQUARE, ObjectColor.RED)