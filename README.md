# TFY-4220-Solid-State-Physics-data-analysis
This is a repository for the sole purpose of conducting simple data analysis of XRD data for a group lab project in the course TFY4220 Solid State Physics.
Probable evil within. Review or use at your own peril. 

### Installing dependencies

`pip install -r requirements.txt`

The generation of simulated data for XRD depends on the github repository Pylattice. To install and use it, navigate into your project folder in terminal and use

 	`git clone https://github.com/allevitan/pylattice`
 
This creates a copy of the repository in your project folder.
However, there are some things to fix before Pylattice works. 
In Pylattice/lattice/\_\_init\_\_.py, change  
```python
from crystal import *
from experiments import *
# to:
from .crystal import *
from .experiments import *
```

The repository needs to properly access formfactors.csv to attain form factors, but the current code does do this properly (at least on Windows 10)

Setting

```python
form_factors_file = os.path.dirname(os.path.abspath(__file__))\
                       + '\\form_factors.csv'
```
 
on line 14 should fix this (remember to also import os)
 
