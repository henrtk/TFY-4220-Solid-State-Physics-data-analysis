import plotly.express as px
import numpy as np
import pandas as pd
import scipy.optimize
import typing
from scipy.signal import savgol_filter

"""
Main functionality. Takes in dataframe with columns
    - "Angle": 2 theta
    - "Intensity": original measurement
This function adds the following columns:
    - "Fit": Curve fit to noise
    - "Peaks": Data substracted noise
"""

def removeNoise(df: pd.DataFrame) -> pd.DataFrame:
    filtered = _removePeaks(df) # Extract noise
    ys = filtered["Intensity"]
    xs = filtered['Angle']
    # Curve fit exponential to noise
    def func(x, a, b, c): # Function blueprint
        return a * np.exp(-b*x) + c
    popt, pcov = scipy.optimize.curve_fit(func, xs, ys)
    a, b, c = popt

    df["Fit"] = func(df["Angle"], a, b, c) # Noise curve
    df["Peaks"] = df["Intensity"] - df["Fit"] # Data substracted noise
    return df


"""
Removes diffraction peaks from dataframe df,
so that we can curve fit to it later.

"""
def _removePeaks(df, smooth = False):
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

    # Remove points if lim=4 consecutive increases
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

    if smooth:
        df["Intensity"] = savgol_filter(df["Intensity"], 5, 2) #Smoothening filter
    return df

def __main():
    with open("Si.txt") as file:
        df = pd.read_table(file, header=None)
        df.columns = ['Angle', 'Intensity']
    
    df = removeNoise(df)
    p=px.line(df, x='Angle', y=['Intensity', 'Fit', "Peaks"])
    p.show()
               
if __name__=="__main__":
    __main()