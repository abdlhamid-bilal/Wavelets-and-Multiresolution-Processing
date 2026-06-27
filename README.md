# Wavelets and Multiresolution Processing 🌊📉

This repository contains the accompanying Python implementations, visualizations, and Manim animations for our proseminar in **Computer Vision & Image Processing** (RWTH Aachen University). 

The code is designed to make the theoretical and mathematical concepts of multiresolution processing practically accessible – from classic image pyramids to modern wavelet theory.

## 👥 Authors
This project was created in collaboration by:
* **[Your Name]** ([@YourGithubName](https://github.com/YourGithubName))
* **Berk Can Ucar** ([@BerkCanUcar](https://github.com/BerkCanUcar))

---

## 📌 Project Contents & Features

The repository is divided into several conceptual scripts, each addressing a specific topic within multiresolution analysis:

* 📉 **1D Discrete Wavelet Transform (DWT):** Demonstration of the step-by-step decomposition of a one-dimensional signal into its approximation (coarse) and detail coefficients.
* 🖼️ **2D Fast Wavelet Transform (FWT):** Application of the Mallat filter bank to images. Showcases the efficient decomposition of an image into its four frequency bands (LL, LH, HL, HH) for edge detection and compression.
* 🔺 **Gaussian Pyramids (Image Pyramids):** Implementation of the classical approach to resolution scaling through iterative blurring (Gaussian filter) and downsampling.
* ⚠️ **Aliasing Effects:** Visual demonstration of the mathematical consequences of downsampling (decimating) signals or images without prior low-pass filtering.
* 🌊 **Scaling and Wavelet Functions:** Algorithmic construction and visualization of the basis functions (father and mother wavelets) using the **Haar** and **Daubechies wavelets** as examples.

---

## 🚀 Installation & Setup

To run the scripts locally, **Python 3.8+** is recommended. The required libraries from the scientific Python stack can be installed as follows.

Clone the repository:
```bash
git clone [https://github.com/YourName/Wavelets-and-Multiresolution-Processing.git](https://github.com/YourName/Wavelets-and-Multiresolution-Processing.git)
cd Wavelets-and-Multiresolution-Processing
