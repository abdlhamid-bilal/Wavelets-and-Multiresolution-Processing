import cv2
import numpy as np
import matplotlib.pyplot as plt

image_bgr = cv2.imread('images/square_pattern.jpg')

if image_bgr is None:
    print("Fehler: Bild nicht gefunden. Bitte Pfad überprüfen!")
    exit()

image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

h, w = image_rgb.shape[:2]
mitte_y, mitte_x = h // 2, w // 2

offset = 1000
image_crop = image_rgb[mitte_y - offset : mitte_y + offset, mitte_x - offset : mitte_x + offset]

r = 25

# Naive downsampling
aliased_image = image_crop[::r, ::r]

# Decimation with Gaussian Kernel
sigma = r / 2.0
ksize = int(2 * round(3 * sigma) + 1) 
smoothed_image = cv2.GaussianBlur(image_crop, (ksize, ksize), sigmaX=sigma)
decimated_image = smoothed_image[::r, ::r] # Take every r-th pixel

# -- Visualize --

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(image_crop, interpolation='nearest')
axes[0].set_title("Original \n Square Pattern")

axes[1].imshow(aliased_image, interpolation='nearest')
axes[1].set_title(f"Naive Downsampling (r={r})\nALIASING")

axes[2].imshow(decimated_image, interpolation='nearest')
axes[2].set_title(f"Real Decimation (r={r})\nANTI-ALIASING")

plt.tight_layout()
plt.savefig("images/aliasing.png", format="png", bbox_inches="tight")
plt.show()