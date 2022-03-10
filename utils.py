import numpy

def F(h,k,l):
    """
    params:
        h, k, l -> int
        reciprocal lattice parameters
    returns:
        class complex(), complex number
        Form factor of the diamond lattice in a simple cubic lattice basis
        for a given lattice plane h, k, l.
    """
    return (1+(-1)**(h+k)+(-1)**(k+l)+(-1)**(h+l))*(1+complex(0,-1)**(h+k+l))

def norm(h,k,l):
    """
    h, k, l -> int
        reciprocal lattice parameters
    returns:
        np.float64
        norm of a reciprocal lattice vector in units 2pi/a, 
        a is the cubic lattice spacing.
    """
    return numpy.sqrt(h**2+k**2+l**2,dtype = numpy.float64)

def exposeNonExtinctions(n):
    """
    params:
        n -> int
    
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
    wavelength = 0.7093
    return wavelength/(2*numpy.sin(theta))

def parseData(filename):
    with open(filename, "r") as f:
        pass

def main():
    return

if __name__ == "__main__":
    main()