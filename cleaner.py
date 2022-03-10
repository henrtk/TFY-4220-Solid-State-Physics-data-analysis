import plotly.express as px
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

with open("Unknown.txt") as file:
    df = pd.read_table(file, header=None)
    df.columns = ['Angle', 'Intensity']

def removePeaks(df):
    shouldRemove=set()
    lim = 4
    for i in range(lim+1, df.index.size):
        for j in range(lim):
            delta=(df["Intensity"][i-j]-df["Intensity"][i-j-1])
            if delta > 0:
                break
            if j == lim-1:
                for s in range(i-j-10, i+1):
                    shouldRemove.add(s)
    print(shouldRemove)
    df = df.drop(shouldRemove)
    df["Intensity"] = savgol_filter(df["Intensity"], 5, 2)
                
        

print(removePeaks(df))