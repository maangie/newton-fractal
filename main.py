import numpy as np
import matplotlib.pyplot as plt
from numba import njit

COEFFS = np.array([1.0, 0.0, 0.0, -1.0])  # z^3 - 1
MAX_ITER = 40
EPS = 1e-8
XMIN, XMAX = -1.5, 1.5
YMIN, YMAX = -1.5, 1.5
RES = 900  # 解像度

def polyval(c, z):
  v = 0.0 + 0.0j
  for a in c:
    v = v * z + a
  return v

def polyder(c):
  n = len(c) - 1
  return np.array([c[i] * (n - i) for i in range(n)], dtype=np.complex128)

DCOEFFS = polyder(COEFFS)

@njit
def newton_fractal(xmin, xmax, ymin, ymax, res, coeffs, dcoeffs, max_iter, eps):
  w = h = res
  xs = np.linspace(xmin, xmax, w)
  ys = np.linspace(ymin, ymax, h)
  conv_idx = np.full((h, w), -1, np.int32)
  conv_it = np.zeros((h, w), np.int32)

  roots = []
  for k in range(64):
    theta = 2 * np.pi * k / 64
    z = 1.2 * np.exp(1j * theta)
    for _ in range(60):
      f = 0j
      g = 0j
      for a in coeffs:
        f = f * z + a
      for b in dcoeffs:
        g = g * z + b
      if abs(g) < 1e-14:
        break
      z = z - f / g
    ok = True
    for r in roots:
      if abs(z - r) < 1e-6:
        ok = False
        break
    if ok:
      roots.append(z)
  roots = np.array(roots, dtype=np.complex128)

  for j in range(h):
    for i in range(w):
      z = xs[i] + 1j * ys[j]
      for it in range(max_iter):
        f = 0j
        g = 0j
        for a in coeffs:
          f = f * z + a
        for b in dcoeffs:
          g = g * z + b
        if abs(g) < 1e-14:
          break
        z = z - f / g
        for r_idx in range(len(roots)):
          if abs(z - roots[r_idx]) < eps:
            conv_idx[j, i] = r_idx
            conv_it[j, i] = it + 1
            break
        if conv_idx[j, i] != -1:
          break
  return conv_idx, conv_it, roots

idx, its, roots = newton_fractal(
  XMIN, XMAX, YMIN, YMAX, RES,
  COEFFS.astype(np.complex128),
  DCOEFFS.astype(np.complex128),
  MAX_ITER, EPS
)

plt.figure(figsize=(6, 6), dpi=120)
valid = idx >= 0
img = np.zeros((RES, RES, 3), dtype=float)

if len(roots) > 0:
  root_colors = np.linspace(0.2, 0.9, max(1, len(roots)))
  for r_i in range(len(roots)):
    mask = (idx == r_i)
    if not np.any(mask):
      continue
    base = root_colors[r_i]
    norm_it = np.zeros_like(its, dtype=float)
    m = its > 0
    norm_it[m] = its[m] / its[m].max()
    img[mask] = np.stack([
      base * (0.3 + 0.7 * (1 - norm_it[mask])),
      0.1 + 0.8 * (1 - norm_it[mask]),
      0.1 + 0.8 * (1 - norm_it[mask])
    ], axis=1)

plt.imshow(img, extent=[XMIN, XMAX, YMIN, YMAX], origin='lower')
plt.title("Newton Fractal for polynomial with coeffs {}".format(COEFFS.tolist()))
plt.xlabel("Re(z)")
plt.ylabel("Im(z)")
plt.tight_layout()
plt.show()
