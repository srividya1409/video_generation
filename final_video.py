import cv2
import numpy as np

# === File paths ===
video_path = r"C:\Users\Srivi\C++\application\avatar_video.mp4"
output_path = r"C:\Users\Srivi\C++\application\video_with_overlay.mp4"
overlay_path = r"C:\Users\Srivi\C++\COMP VISION\image_no_bg_grabcut.png"

# === Load transparent overlay image ===
overlay_rgba = cv2.imread(overlay_path, cv2.IMREAD_UNCHANGED)
if overlay_rgba is None:
    print("Overlay image not found.")
    exit()

# Separate color and alpha channels
overlay_rgb = overlay_rgba[:, :, :3]
overlay_alpha = overlay_rgba[:, :, 3] / 255.0

# Resize overlay image to fit the table size
overlay_rgb = cv2.resize(overlay_rgb, (120, 160))  # width, height
overlay_alpha = cv2.resize(overlay_alpha, (120, 160))

# === Open the video file ===
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error opening video file.")
    exit()

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# === Output video writer ===
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# === Position where the bear should be placed on the table ===
overlay_x = 1200  # Horizontal position (adjusted for center of table)
overlay_y = 700  # Vertical position (adjusted to sit on table)

# === Process video frames ===
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Ensure overlay fits within frame bounds
    if (overlay_y + overlay_rgb.shape[0] > frame.shape[0]) or (overlay_x + overlay_rgb.shape[1] > frame.shape[1]):
        continue

    # Extract region of interest (ROI) from the frame
    roi = frame[overlay_y:overlay_y + overlay_rgb.shape[0], overlay_x:overlay_x + overlay_rgb.shape[1]]

    # Blend the overlay with the ROI
    for c in range(3):  # B, G, R channels
        roi[:, :, c] = (roi[:, :, c] * (1 - overlay_alpha) + overlay_rgb[:, :, c] * overlay_alpha).astype(np.uint8)

    # Place blended ROI back into frame
    frame[overlay_y:overlay_y + overlay_rgb.shape[0], overlay_x:overlay_x + overlay_rgb.shape[1]] = roi

    # Write the frame to output
    out.write(frame)

    # Optional: show live preview
    # cv2.imshow("Preview", frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# === Cleanup ===
cap.release()
out.release()
cv2.destroyAllWindows()

print("Video saved with overlay at:", output_path)
