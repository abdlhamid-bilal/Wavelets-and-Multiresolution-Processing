import os
import cv2
import matplotlib.pyplot as plt

image = cv2.imread("images/half_white_half_black.png")

if image is None:
    raise FileNotFoundError("Could not load image")

max_height = 600
h_orig, w_orig = image.shape[:2]

if h_orig > max_height:
    scale = max_height / h_orig
    new_w = int(w_orig * scale)
    image = cv2.resize(image, (new_w, max_height))

output_dir = "results/images/half_white_half_black_results"
os.makedirs(output_dir, exist_ok=True)

levels = 6

images = [image]
current = image

for _ in range(levels):
    current = cv2.pyrDown(current)
    images.append(cv2.resize(current, (w_orig, h_orig), interpolation=cv2.INTER_NEAREST))

for i, img in enumerate(images):
    path = os.path.join(output_dir, f"{i}_level.png")
    cv2.imwrite(path, img)

    plt.figure(figsize=(8, 6))
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.title(f"Level {i}")
    plt.savefig(os.path.join(output_dir, f"plot_{i}.png"), bbox_inches="tight", dpi=300)
    plt.close()