import numpy as np
import matplotlib.pyplot as plt
import pywt

np.random.seed(42)
N = 256
t = np.linspace(0, 1, N) 

trend = np.sin(4 * np.pi * t) 

noise = 0.2 * np.sin(70 * np.pi * t) 

jump = np.zeros_like(t)
mid_idx = N // 2
jump[mid_idx : mid_idx + 5] = 2.0

# The final signal
original_signal = trend + noise + jump

wavelet = 'haar'
cA, cD = pywt.dwt(original_signal, wavelet)

approximation = pywt.idwt(cA, None, wavelet)[:len(t)]
details = pywt.idwt(None, cD, wavelet)[:len(t)]

# -- Visualize --

plt.style.use('seaborn-v0_8-whitegrid')
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

n = np.arange(1, N + 1)

ax1.plot(n, original_signal, color='black', linewidth=1.5)
ax1.set_title(r"Original Signal $f(n)$", fontsize=14, fontweight='bold')
ax1.set_ylabel("Amplitude")

ax2.plot(n, approximation, color='#1f77b4', linewidth=1.5)
ax2.set_title(r"Approximation $T_{\varphi}$", fontsize=14, fontweight='bold')
ax2.set_ylabel("Amplitude")

ax3.plot(n, details, color='#d62728', linewidth=1.5)
ax3.set_title(r"Details $T_{\psi}$", fontsize=14, fontweight='bold')
ax3.set_ylabel("Amplitude")
ax3.set_xlabel("Time / Position", fontsize=12)

plt.tight_layout()

plt.savefig("results/images/dwt_decomposition.png", format="png", bbox_inches="tight")

plt.show()