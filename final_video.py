import cv2
import numpy as np

video_path = r"C:\Users\Srivi\C++\application\avatar_video.mp4"
output_path = r"C:\Users\Srivi\C++\application\video_with_overlay.mp4"
overlay_path = r"C:\Users\Srivi\C++\COMP VISION\image_no_bg_grabcut.png"

overlay_rgba = cv2.imread(overlay_path, cv2.IMREAD_UNCHANGED)
if overlay_rgba is None:
    print("Overlay image not found.")
    exit()

overlay_rgb = overlay_rgba[:, :, :3]
overlay_alpha = overlay_rgba[:, :, 3] / 255.0

overlay_rgb = cv2.resize(overlay_rgb, (120, 160))  
overlay_alpha = cv2.resize(overlay_alpha, (120, 160))

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error opening video file.")
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

overlay_x = 1200 
overlay_y = 700  

while True:
    ret, frame = cap.read()
    if not ret:
        break

   
    if (overlay_y + overlay_rgb.shape[0] > frame.shape[0]) or (overlay_x + overlay_rgb.shape[1] > frame.shape[1]):
        continue

    roi = frame[overlay_y:overlay_y + overlay_rgb.shape[0], overlay_x:overlay_x + overlay_rgb.shape[1]]

    for c in range(3): 
        roi[:, :, c] = (roi[:, :, c] * (1 - overlay_alpha) + overlay_rgb[:, :, c] * overlay_alpha).astype(np.uint8)

    frame[overlay_y:overlay_y + overlay_rgb.shape[0], overlay_x:overlay_x + overlay_rgb.shape[1]] = roi

    out.write(frame)


cap.release()
out.release()
cv2.destroyAllWindows()

print("Video saved with overlay at:", output_path)
