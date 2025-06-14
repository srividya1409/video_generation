import cv2
import numpy as np

img = cv2.imread(r"C:\Users\Srivi\C++\COMP VISION\bear.jpg")
if img is None:
    print("[ERROR] Image not found.")
    exit()
print("[INFO] Image loaded.")

mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

rect = (50, 50, img.shape[1] - 100, img.shape[0] - 100)
cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
print("[INFO] GrabCut applied.")

mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

b, g, r = cv2.split(img)
a = mask2 * 255
transparent = cv2.merge((b, g, r, a))

# Save PNG
output_path = r"C:\Users\Srivi\C++\COMP VISION\image_no_bg_grabcut.png"
cv2.imwrite(output_path, transparent)
print("[INFO] Transparent image saved at:", output_path)
