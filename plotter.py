import plotly.express as px
import numpy as np
import pandas as pd
from cleaner import removePeaks

def __main():

    with open("Unknown.txt") as file:
        df = pd.read_table(file, header=None)
        df.columns = ['Angle', 'Intensity']

    print(df)
    plot = px.line(removePeaks(df), x='Angle', y='Intensity')
    plot.update_xaxes(title=r"$2 \theta [\mathrm{deg}]$", title_font=dict(size=24))
    plot.update_yaxes(title=r"$I [\mathrm{a.u.}]$", title_font=dict(size=24))
    plot.update_layout(
        legend={},
        template='simple_white',
        font = dict(
        family='Latin Modern Math',
        size=24,
        color = '#0e1111'
        )
    )
    plot.show()
           
if __name__=="__main__":
    __main()