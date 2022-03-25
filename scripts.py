import utils
from utils import trapezoidalIntegral
import cleaner
import numpy as np
import pylattice.lattice as lat
import matplotlib.pyplot as plt
import seaborn as sns
# Beware! Dependency on repo Pylattice,
# https://github.com/allevitan/pylattice and check Readme.md for install tips.

def plotSimulations():
    data  =  utils.parseData("unknown XRD data.txt")
    # Set up the crystal structure
    NaCllattice = lat.FCC(5.63)
    Cl,Na = b'Cl1-', b'Na1+'
    NaClbasis = lat.Basis([(Cl,[0,0,0]),
                           (Na,[0.5,0.5,0.5])],
                            l_const=5.63)
    NaCl = NaCllattice + NaClbasis

    K = b'K1+'
    KClLattice = lat.FCC(6.29)
    KClBasis = lat.Basis([(Cl,[0,0,0]),
                           (K,[0.5,0.5,0.5])],
                                l_const=6.29)
    KCl = KClLattice + KClBasis

    data  = cleaner.removeNoise(data)
    # Generate a simulated XRD experiment with molybdenum Ka1 lambda = 0.7093
    scattering_dataNa = lat.powder_XRD(NaCl, 0.7093)
    angles1, values1 = lat.spectrumify(scattering_dataNa)
    scattering_dataK = lat.powder_XRD(KCl, 0.7093)
    angles2, values2 = lat.spectrumify(scattering_dataK)
    
    # Create color palette
    col = sns.dark_palette("gray",n_colors=9)
    # normalization factor for peak 2
    normalize  = max(data.values[:132,3])/(max(values2)*max(data.values[:,3]))

    plt.fill(angles1[650:-7950], values1[650:-7950]/max(values1), color = col[1], label = "Simulated NaCl", linestyle = "-",alpha = 0.5)
    plt.fill(angles2[650:-7950], values2[650:-7950]*normalize, color = col[-2], label = "Simulated KCl", linestyle = "-",alpha = 0.3)

    # plot interesting part of data
    plt.plot(data.values[110:-30,0],data.values[110:-30,3]/max(data.values[:,3]), label = "Filtered data",linewidth = 1, color = "black")
   
    # Add some more info to the plot
    plt.xticks(np.linspace(12.5,35,10))
    plt.legend()
    plt.xlabel(r'Scattering angle $2\theta$', fontsize = 10)
    plt.ylabel(r'Relative intensity', fontsize = 10)
    
    # Index planes
    peaklabels = {0.88:10.3,0.92:15,0.6:15.6,0.7:20.6,0.25:22.5,0.26:25.2} #every other is NaCl (approx)
    planes = ["{200}", "{200}", "{220}","{220}","{222}","{222}"]
    lastplane = 0
    for (i,x),plane in zip(peaklabels.items(),planes):
        if lastplane == 0:
            plt.text(x,i,plane,color = col[-2], fontsize = 11)
            lastplane = 1
        else:
            plt.text(x,i,plane,color = col[0],fontsize = 11)
            lastplane = 0
    plt.show()

    # Print LaTeX tabular of relative integrated peak intensities
    data = data[["Angle","Peaks","Intensity","Fit"]]
    normalizeNa = 1/trapezoidalIntegral(data.values[:,0:2],136,147)
    normalizeK = 1/trapezoidalIntegral(data.values[:,0:2],119,132)
    print(trapezoidalIntegral(data.values[:,0:2],119,132)*normalizeK) 
    print("&",trapezoidalIntegral(data.values[:,0:2],136,147)*normalizeNa,"\\\\\\hline")
    print(trapezoidalIntegral(data.values[:,0:2],176,183)*normalizeK)
    print("&",trapezoidalIntegral(data.values[:,0:2],196,205)*normalizeNa,"\\\\\\hline")
    print(trapezoidalIntegral(data.values[:,0:2],216,223)*normalizeK)
    print("&",trapezoidalIntegral(data.values[:,0:2],242,249)*normalizeNa,"\\\\\\hline")
    print(trapezoidalIntegral(data.values[:,0:2],252,258)*normalizeK)
    print("&","Overlapped","\\\\\\hline")
    print("Overlaped","&",trapezoidalIntegral(data.values[:,0:2],309,315)*normalizeNa,"\\\\\\hline")
    print(trapezoidalIntegral(data.values[:,0:2],314,323)*normalizeK)
    print("&",trapezoidalIntegral(data.values[:,0:2],348,354)*normalizeNa,"\\\\\\hline")
    #Dropping double overlap peak
plotSimulations()