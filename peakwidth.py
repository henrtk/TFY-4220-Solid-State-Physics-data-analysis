import numpy as np
import matplotlib.pyplot as plt


sigmaSi = np.array([1.86073267e-1])
sigmaKCl = np.array([1.85481121e-1, 1.31084516e-1, 0.13680354])
sigmaNaCl = np.array([1.47464807e-1, 1.44908341e-1, 0.14553081])

def findB(sigmas):
    return 2*np.sqrt(2*np.log(2))*sigmas
    
betaSi = findB(sigmaSi)
betaKCl = findB(sigmaKCl)
betaNaCl = findB(sigmaNaCl)

thetasKCl = np.array([12.8535, 18.4575, 22.5195])
thetasNaCl = np.array([14.499, 20.6685, 25.244])
xKCl = 1/np.cos(thetasKCl*np.pi/180)
xNaCl = 1/np.cos(thetasNaCl*np.pi/180)

plt.figure(figsize=(10,3.5))
plt.axhline(y = betaSi, color = 'k', linestyle = 'dashed', label="Si reference")
plt.scatter(xKCl, betaKCl, color="k", marker="s", label="KCl")
plt.scatter(xNaCl, betaNaCl, color="k", marker="v", label="NaCl")
plt.legend(["Si reference", "KCl", "NaCl"],loc = 'upper right', ncol = 3) #bbox_to_anchor=(0.6,0.60))
plt.ylim(0.27, 0.50)

fsize = 11

tsize = 10

tdir = 'in'

major = 5.0

minor = 3.0

lwidth = 0.8

lhandle = 2.0

plt.rcParams['font.size'] = fsize

plt.rcParams['legend.fontsize'] = tsize

plt.rcParams['xtick.direction'] = tdir

plt.rcParams['ytick.direction'] = tdir

plt.rcParams['xtick.major.size'] = major

plt.rcParams['xtick.minor.size'] = minor

plt.rcParams['ytick.major.size'] = 5.0

plt.rcParams['ytick.minor.size'] = 3.0

plt.rcParams['axes.linewidth'] = lwidth

plt.rcParams['legend.handlelength'] = lhandle

plt.title(r"FWHM vs. $(\cos{\theta})^{-1}$")
plt.xlabel(r"$(\cos{\theta})^{-1}$")
plt.ylabel(r"FWHM [$^{\circ}$]")

plt.show()

#ys = Bs[1:]
