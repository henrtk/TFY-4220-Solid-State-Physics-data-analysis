import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.ndimage as spi
import pylattice.lattice as lat
import cleaner
import seaborn as sns
def F(h,k,l):
    """
    params:
        h, k, l : int
        reciprocal lattice parameters
    returns:
        class complex(), complex number
        Form factor of the diamond lattice in a simple cubic lattice basis
        for a given lattice plane h, k, l.
    """
    return (1+(-1)**(h+k)+(-1)**(k+l)+(-1)**(h+l))*(1+complex(0,-1)**(h+k+l))

def norm(h,k,l):
    """
    h, k, l : int
        reciprocal lattice parameters
    returns:
        np.float64
        norm of a reciprocal lattice vector in units 2pi/a, 
        a is the cubic lattice spacing.
    """
    return np.sqrt(h**2+k**2+l**2,dtype = np.float64)

def exposeNonExtinctions(n):
    """
    params:
        n : int
    
    returns: 
        void
        prints all non-extinct reflections for lattice planes with h, k, l < n
        for diamond basis in simple cubic lattice.
    """
    for h in range(n):
        for k in range(n):
            for l in range(n):
                if F(h,k,l) != 0:
                    print(f"Nonzero at h = {h}, k = {k}, l = {l}. Q is {norm(h,k,l)}, F = {F(h,k,l)}") 

def D(theta):
    wavelength = 0.7093 #Ångströms 
    return wavelength/(2*np.sin(theta/2))

def parseData(filename):
    """
    params:
        filename : string
        target file to read
    returns:
        pd.DataFrame object of the read data
    """
    data = pd.read_table(filename, header = None)
    data.columns = ['Angle', 'Intensity']
    return data

def trapezoidalIntegral(datavals : np.ndarray, a = 0, b = -1) -> np.float64 :
    """
    params:
        datavals : np.ndarray
        feed it data.values, data : pd.DataFrame

        a, b : int
        start and end positions in datavals. 

    returns: 
        numerical integral of datavals[1] with respect to datavals[0], 
        from a to b, using the trapezoidal quadrature.
        
        Assumes uniform spacing for datavals[0].
    """
    if datavals.shape[1] != 2:
        raise TypeError(f"The input datavals has the wrong shape {datavals.shape}, expected (i, 2)")
    dx =  datavals[1,0]-datavals[0,0]
    y  =  datavals[a:b,1]
    subintervalAreas = [dx*(yend+ystart)/2 for yend, ystart in zip(y[1:],y[:-1])]
    return sum(subintervalAreas)

# Testing functions
def _main(): # coords i linjenummer fra -1 og til linjenummer 
    data = parseData("unknown XRD data.txt")
    color = sns.dark_palette("gray")
    sns.palplot(color)
    #plt.plot(data.values[:,0], data.values[:,1] )
    #plt.plot(data.values[:,0],np.sin(data.values[:,0]/20))
    plt.show()
    data = cleaner.removeNoise(data)
   



    return

if __name__ == "__main__":
    _main()