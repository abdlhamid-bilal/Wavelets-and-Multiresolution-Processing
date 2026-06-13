import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('images/bird.jpg')

max_height = 600
h_orig, w_orig = image.shape[:2]

if h_orig > max_height:
    scale = max_height / h_orig
    new_w = int(w_orig * scale)
    image = cv2.resize(image, (new_w, max_height))

h, w = image.shape[:2]


decimated_1 = cv2.pyrDown(image)
decimated_2 = cv2.pyrDown(decimated_1)
decimated_3 = cv2.pyrDown(decimated_2)


decimated_upscaled_1 = cv2.resize(decimated_1, (w, h), interpolation=cv2.INTER_NEAREST)
decimated_upscaled_2 = cv2.resize(decimated_2, (w, h), interpolation=cv2.INTER_NEAREST)
decimated_upscaled_3 = cv2.resize(decimated_3, (w, h), interpolation=cv2.INTER_NEAREST)

comparison = np.hstack((image, decimated_upscaled_1, decimated_upscaled_2, decimated_upscaled_3))

cv2.namedWindow("Original vs. Starke Decimation", cv2.WINDOW_NORMAL)
cv2.imshow("Original vs. Starke Decimation", comparison)
cv2.imwrite("images/decimation.png", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()