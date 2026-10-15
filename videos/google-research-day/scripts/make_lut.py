"""Light corrective grade (warm & witty recipe from videos/travelopod/scripts/make_lut.py) -> grade/google_research_warm_witty.cube.
Measured only on the shared still: the same warm indoor cast as travelopod, so it starts from the same recipe.
Re-measure on the real footage before final."""
import os
import numpy as np
from common import ROOT
N = 33


def grade(rgb):
    x = rgb * np.array([0.985, 1.0, 1.06])            # cool the warm indoor cast
    x = np.clip(x, 0, 1)
    s = x * x * (3 - 2 * x); x = 0.75 * x + 0.25 * s  # gentle S-curve contrast
    x = 0.012 + x * (1 - 0.012)                       # tiny black lift (soft, not crushed)
    l = (x * np.array([0.2126, 0.7152, 0.0722])).sum(-1, keepdims=True)
    x = l + (x - l) * 1.07                            # +7% saturation
    return np.clip(x, 0, 1)


g = np.linspace(0, 1, N)
b, gg, r = np.meshgrid(g, g, g, indexing='ij')        # cube order: R fastest
out = grade(np.stack([r, gg, b], -1).reshape(-1, 3))
os.makedirs(os.path.join(ROOT, 'grade'), exist_ok=True)
with open(os.path.join(ROOT, 'grade', 'google_research_warm_witty.cube'), 'w') as f:
    f.write('TITLE "google research warm witty"\nLUT_3D_SIZE 33\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
    for v in out:
        f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
print('wrote grade/google_research_warm_witty.cube')
