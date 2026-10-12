import numpy as np
N=33
def grade(rgb):
    x=rgb*np.array([0.985,1.0,1.06])            # cool the warm indoor cast
    x=np.clip(x,0,1)
    s=x*x*(3-2*x); x=0.75*x+0.25*s              # gentle S-curve contrast
    x=0.012+x*(1-0.012)                          # tiny black lift (soft, not crushed)
    l=(x*np.array([0.2126,0.7152,0.0722])).sum(-1,keepdims=True)
    x=l+(x-l)*1.07                               # +7% saturation
    return np.clip(x,0,1)
g=np.linspace(0,1,N)
b,gg,r=np.meshgrid(g,g,g,indexing='ij')         # cube order: R fastest
rgb=np.stack([r,gg,b],-1).reshape(-1,3)
out=grade(rgb)
with open('/Users/harnoor/Downloads/travelopod/edit/grade/travelopod_warm_witty.cube','w') as f:
    f.write('TITLE "travelopod warm witty"\nLUT_3D_SIZE 33\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
    for v in out: f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
