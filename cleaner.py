import plotly.express as px
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
import scipy.optimize
import typing

"""
Removes diffraction peaks from dataframe df,
so that we can curve fit to it later
"""
def removePeaks(df):
    shouldRemove=set() # Data points which should be removed
    # Remove points if lim=3 consecutive decreaces
    lim = 3
    for i in range(lim+1, df.index.size): 
        for j in range(lim):
            delta=(df["Intensity"][i-j]-df["Intensity"][i-j-1])
            if delta > 0:
                break
            if j == lim-1:
                for s in range(i-j-10, i+1):
                    shouldRemove.add(s)
    # Remove points if lim=4 consecutive increaces
    lim = 4
    for i in range(lim+1, df.index.size):
        for j in range(lim):
            delta=(df["Intensity"][i-j]-df["Intensity"][i-j-1])
            if delta < 0:
                break
            if j == lim-1:
                for s in range(i-j-7, i+7):
                    if (s >= 0 and s < df.index.size):
                        shouldRemove.add(s)
    # Remove the rows from df
    for i in range(lim+1, df.index.size):
        if (df["Intensity"][i] > 35):
            shouldRemove.add(i)
    df = df.drop(shouldRemove)
    #df["Intensity"] = savgol_filter(df["Intensity"], 5, 2) #Smoothening filter
    return df

""" 
For curve fitting to
exponential decay
"""
def monoExp(x, m, t, b):
    return m * np.exp(-t * x) + b

def __main():
    with open("Si.txt") as file:
        df = pd.read_table(file, header=None)
        df.columns = ['Angle', 'Intensity']
        #print(removePeaks(df))

    filtered = removePeaks(df)
    ys = filtered["Intensity"]
    xs = filtered.index

    p0 = (1, .0005, 10) # start with values near those we expect
    params, cv = scipy.optimize.curve_fit(monoExp, xs, ys, p0)
    m, t, b = params
    sampleRate = 20_000 # Hz
    tauSec = (1 / t) / sampleRate

    # determine quality of the fit
    squaredDiffs = np.square(ys - monoExp(xs, m, t, b))
    squaredDiffsFromMean = np.square(ys - np.mean(ys))
    rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
    print(f"R² = {rSquared}")

    filtered["Fit"]=np.square(monoExp(xs, m, t, b))

    p=px.line(filtered, x='Angle', y=['Intensity', 'Fit'])
    p.show()

               
if __name__=="__main__":
    __main()