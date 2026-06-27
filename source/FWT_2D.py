import pywt
import cv2
import numpy as np
import matplotlib.pyplot as plt

bild_pfad = 'images/bird.jpg'
image = cv2.imread(bild_pfad, cv2.IMREAD_GRAYSCALE)

if image is None:
    print(f"Error")
else:
    coeffs2 = pywt.dwt2(image, 'haar')
    
    LL, (LH, HL, HH) = coeffs2

    fig = plt.figure(figsize=(10, 10))

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.imshow(LL, cmap='gray')
    ax1.set_title('LL: Approximation', fontsize=14)
    ax1.axis('off')


    ax2 = fig.add_subplot(2, 2, 2)
    ax2.imshow(np.abs(LH), cmap='gray') 
    ax2.set_title('LH: Horizontal edges', fontsize=14)
    ax2.axis('off')

    ax3 = fig.add_subplot(2, 2, 3)
    ax3.imshow(np.abs(HL), cmap='gray')
    ax3.set_title('HL: Vertical edges', fontsize=14)
    ax3.axis('off')

    ax4 = fig.add_subplot(2, 2, 4)
    ax4.imshow(np.abs(HH), cmap='gray')
    ax4.set_title('HH: Diagonal edges', fontsize=14)
    ax4.axis('off')

    plt.tight_layout()
    plt.show()