"""
Figure 1 - Scaling functions phi and wavelet functions psi.
"""

import numpy as np
import matplotlib.pyplot as plt
import pywt

# --- consistent colour semantics across the whole paper -----------------
C_APPROX = "#1f4e79"   # approximation / scaling / low-pass  (blue)
C_DETAIL = "#c55a11"   # detail / wavelet / high-pass        (orange)

WAVELETS = ["haar", "db2"]
NICE_NAME = {"haar": "Haar", "db2": "Daubechies db2"}
LEVEL = 8  # refinement level for wavefun() -> smooth curves

fig, axes = plt.subplots(len(WAVELETS), 2, figsize=(8.0, 4.8), sharex="row")

for row, name in enumerate(WAVELETS):
    w = pywt.Wavelet(name)
    phi, psi, x = w.wavefun(level=LEVEL)

    ax_phi, ax_psi = axes[row]

    ax_phi.plot(x, phi, color=C_APPROX, lw=1.6)
    ax_phi.fill_between(x, phi, color=C_APPROX, alpha=0.12)
    ax_phi.axhline(0, color="0.6", lw=0.7)
    ax_phi.set_ylabel(NICE_NAME[name], fontsize=10)

    ax_psi.plot(x, psi, color=C_DETAIL, lw=1.6)
    ax_psi.fill_between(x, psi, color=C_DETAIL, alpha=0.12)
    ax_psi.axhline(0, color="0.6", lw=0.7)

    for ax in (ax_phi, ax_psi):
        ax.grid(True, ls=":", lw=0.5, alpha=0.6)
        ax.margins(x=0.02)

axes[0, 0].set_title(r"Scaling function $\varphi(x)$  (approximation)",
                     color=C_APPROX, fontsize=11)
axes[0, 1].set_title(r"Wavelet function $\psi(x)$  (detail)",
                     color=C_DETAIL, fontsize=11)

for ax in axes[-1]:
    ax.set_xlabel("x")

fig.tight_layout()
fig.savefig("fig1_scaling_wavelet.pdf", bbox_inches="tight")
fig.savefig("fig1_scaling_wavelet.png", dpi=200, bbox_inches="tight")
print("wrote fig1_scaling_wavelet.pdf / .png")
