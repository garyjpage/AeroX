# AeroX Aerodynamic Data Exchange Format
AeroX is a simple extension to 'standard' Comma Separated Value (CSV) files that promotes reliable and error prone interchange of aerodynamic data. It addresses both the need of engineers in that the data  is well documented, and also makes it easy for AI tools to ingest and understand the data. The format has been developed within the UK National Wind Tunnel Facility (https://www.nwtf.ac.uk) to improved dissmemination of wind tunnel data, but can be easily used for any type of numeric engineering or scientific data. Since the format extends the CSV, it is trivial to remove the extra information and process with many standard tools (e.g. spreadsheets, scientific visualisation).

# Features
The file format provides:

- free text information about the data

- definitions of the columns of data that are 'inputs' and 'outputs'

- longer descriptions of the data columns

- shorter headers to reference the data columns

- units for each column

- numerical, floating points columns of data

- optional column of textual identifiers


The accompanying python class provides a simple framework to manipulate these files including:

- reading, writing and conversion to standard CSV and webCSV

- filter rows based on input values

- extract, delete, replace and insert columns of data

- line plots

- contour plots

- interpolation

## Installation
For simple usage it is sufficient to navigate to https://github.com/garyjpage/AeroX and download the .zip file.
For developers the normal git clone can be used:
```bash
# Clone the repository
git clone https://github.com/garyjpage/AeroX.git
```
There is no requirement to install the class, it is usually sufficient (and simpler) to merely copy the file aerox.py to the location where your data resides. This also makes it easier to customise the plotting routines to your own requirements.

The download contains the python class, some example AeroX files and short python scripts. 

The python class requires the usual additional packages:
- numpy
- scipy
- matplotlib

Testing has been carried out with python=3.13, numpy=2.3.2, scipy=1.16.0, matplotlib=3.10.5 but any recent releases should work.

## Example AeroX file
```
# simple AeroX polar csv test file
# synthetic aerofoil data with varying angle of attack and Reynolds number
# hence there are two x inputs alpha and Re, and two y outputs CD and CL and an optional identifier (RUNID)
# the first non comment line states the number of inputs x_nd and number of outputs y_nd
# the second non comment line is the long verbose variable names
# the third non comment line are the variable units
# the remainder is a standard CSV 
2,2
angle of attack, "Reynolds number", drag coefficient, lift coefficient
degrees, -, -, - 
alpha, Re ,CD,  CL, RUNID
0, 1.00E+06, 0.02, 0.0, run1
2, 1.00E+06, 0.03, 0.2, run2
4, 1.00E+06, 0.03, 0.31
5, 1.00E+06, 0.05, 0.5, run4
....
```

## Example Usage
To do some simple processing of the preceding example file, copy polar.csv and aerox.py to the same directory, then using the ipython interactive shell enter the following:
```
from aerox import AeroX
polar = AeroX('polar.csv')
polar.add_interpolator('RBF')
polar.interpolate_y('CD', alpha=4.5, Re=1.0E6)
polar.plot('alpha','CD', Re=1.0E6, interpolate=True )
polar.plot_2d('alpha', 'Re', 'CD', interpolate=True)
```
This will read a file, interpolate CD at an angle of attack that is not present in the data, plot a line plot, then plot a coloured contour.

Within the ipython shell it is possible to look at the underlying data, for example

```
polar.x_nd
Out[7]: 2

polar.y_nd
Out[8]: 2

polar.x
Out[9]: 
array([[0.e+00, 1.e+06],
       [2.e+00, 1.e+06],
       .....
```
## Further Information
Some more details on the design of AeroX and its usage is available at [AeroX_Rationale](AeroX_Rationale.md). For information about the NWTF Experimental Database activity see 'AIAA-2026-2475: Building a Metadata-Centric Archive for Experimental Aerodynamics' [DOI](https://arc.aiaa.org/doi/10.2514/6.2026-2475) presented at the AIAA 2026 SciTech Forum and the website [NWTF Experimental Database](https://www.nwtf.ac.uk/experimental-database/)

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 - see the [LICENSE](LICENSE) file for details.

## Contact

Gary Page g.j.page@lboro.ac.uk
https://www.lboro.ac.uk/departments/aae/people/gary-page/

Project Link: [https://github.com/garyjpage/AeroX](https://github.com/garyjpage/AeroX)

## Acknowledgments
This work was supported by Loughborough University through the UK Engineering and Physical Sciences Research Council (EPSRC) National Wind Tunnel Facility (NWTF) Network Grant, EP/X011836/1.  
