# AeroX Description  
In creating the current NWTF experimental database, one of the main tasks has been to take existing published data and reformat and process it in such a way that it is easily understandable in a relatively consistent and logical form. Up until this point, we have not attempted a standardisation of the data format, but the lessons learned have allowed us to create a proposal for sharing experimental aerodynamic data with the Aerodynamic Exchange (AeroX) format.  
  
There are several key issues we wish to address:  
1. The file should be easily readable by both humans and automated processing tools. The latter is becoming increasingly important as a large number of downloads from our data repository appear to be AI 'bots' trawling the web for data.  
2. The file should be easily created using existing tools such as text editors and spreadsheets, and should also be easily read using a wide variety of common engineering processing software.  
3. There should be a logical structure imposed such that it is clear what the independent variables (or 'inputs') are and what the dependent variables (or 'outputs') are.  
4. All data should have units (or be marked as dimensionless).  
5.  The file should be self-contained and verbosely descriptive, so that the source of the data is clear.  
  
So-called 'Comma-Separated Values' (CSV) files are incredibly common amongst science, engineering, finance, and data science. It is a simple and lightweight format consisting of one row of variable names and then multiple rows of data with all items separated by commas (although some use tabs or | symbols for separators!). However, it does not address many of the issues noted above.   
  
Similar issues have been addressed by others, in particular the CSV on the Web proposal ([https://w3c.github.io/csvw/primer/](https://w3c.github.io/csvw/primer/)) which adds a second metadata file to describe the existing CSV file. This metafile uses the JavaScript Object Notation (JSON), a format that is hierarchical and structured and if desired could store the data as well as its description. Although it is 'human readable', it is not so easy to write, in general requiring key-value pairs and the use of matched braces { } to provide the structure. A key flaw is that the metadata can become detached from the CSV; if a human or AI tool has access to just the CSV file, there is no way of linking that back to a JSON file that may exist somewhere. Finally, there are no options of including units - an absolutely essential requirement for engineering.  
  
Our proposal here is a very simple extension to a standard CSV file by adding a number of lines at the beginning, such that by simply removing them (or skipping on read), you recover the 'standard' CSV. There are two fundamental design decisions. First, that the data columns should be ordered in such a way that all the independent variables (or 'inputs') are first, followed by all the dependent variables (or 'outputs'). This follows common data science approaches where the former is X and the latter is Y. Although this seems an entirely logical way to organise the data, our experience has found that this is not always followed. Second, all data is numeric and consists of real numbers. This is reasonable for engineering and avoids the complexity of a more general format that has to deal with a variety of types such as strings, dates, and integers.  
  
A generic description is provided below followed by an example.
  
```
# zero or more comment lines
x_nd, y_nd
x0_long_description, x1_long_description, ..., y0_long_description, y1_long_description ...
x0_units, x1_units, ..., y0_units, y1_units ...
x0_name, x1_name, ..., y0_name, y1_name ...
x0, x1, x2 ... , y0, y1, y2.., (ident)
.......

```
  
  
```
# this is a simple AeroX csv test file
# it contains **synthetic** aerofoil data with varying angle of attack $\alpha$ and Reynolds number
# hence there are two x inputs and two y outputs, 
# the tag on the second data point is ignored
2,2
angle of attack, Reynolds number, drag coefficient, lift coefficient
degrees, -, -, - 
alpha, Re ,CD,  CL
0, 1.00E+06, 0.02, 0.0
2, 1.00E+06, 0.03, 0.2, run10
4, 1.00E+06, 0.03, 0.3
....
7, 2.00E+06, 0.08, 0.6
10,2.00E+06, 0.11, 0.6

```
  
The file starts with zero or more comment lines beginning with the standard comment character # and one blank space. This should be used to describe the data and in particular should reference published papers, web pages and data repositories, preferably including Digital Object Identifiers. It both makes the data accessible and provides authority as to its quality. If more than simple text formatting is desired, then markup syntax should be used for bold, italic, headings etc., and for equations LateX commands should be included surrounded by $ symbols.  
  
The following line simply contains two integers: `x_nd`, the number of columns in the input x; `y_nd`, the number of columns in the output y. This addition has huge benefits in that it defines the logic of the data in one simple line.  
  
The following three lines are expanded column headers. The first is a more human-readable and verbose description, the second is the units of the data, and the final third line is the traditional single-word column variable name. The first line is particularly useful in that different organisations or countries may adopt differing naming conventions - especially with Greek characters - and avoids misunderstanding of the short name. The units line is key in that it avoids misinterpretation and allows tools to automatically convert data. The string used to define the unit should be parsable by the Python Pint software ([https://pint.readthedocs.io/](https://pint.readthedocs.io/)). This is both comprehensive (for example, understanding Imperial, CGS and MKS unit systems) and flexible (e.g. understanding that s, second and seconds are the same thing). For any non-dimensional quantity, a single - symbol should be used or the word dimensionless. The final line contains the traditional CSV headers consisting of single words. It would be impossible to define a standard naming scheme for aerodynamic data, so the naming is left to the convention of the authors - with the benefit that the earlier long name helps remove ambiguity.  
  
The remaining rows of the file  are `(x_nd + y_nd)` of columns of numeric data. If any additional columns are included in the file, they are ignored. If desired, this allows tagging of the data point (for example a code referring to the run or a  comment about potential probe drop out). Note the second line of the example. If data is missing or invalid then the 'NaN' convention should be used.

Often an experimental data point will have some underlying textual reference as part of the data capture system. We refer to this as an identifier, and these can optionally appear as an extra column after the outputs. This gives extra authority to the data in that it can potentially be traced back to its origin. It also allows a user to add some extra context (e.g. 'possible probe error for this point'). If an identifier is used, it does not need to appear after every row, and optionally a short header can be used.
  
There is one special case of `x_nd` is zero. This means that there no 'inputs', only 'outputs' and the numeric data consists of a single line. This is useful to capture 'constants', for example the atmospheric conditions of a test, or geometric data on the vehicle.  
  
```
# This is an AeroX constant file special case
# if the input dimensions x_nd is zero, then we just have a list of constants
# there will be one line of numeric data and any other lines will be silently ignored
0,3
ISA SL density, ISA SL pressure, ISA SL temperature
kg.m^-3,Pa,K
rho0,P0,T0
1.225,101325.0,288.15

```
  
We have developed a small Python class to process this data format and made openly available under the GPL V3 license. The class provides functions to read an existing AeroX CSV file, filter rows based on input values, create line and contour plots, and interpolate the data. It can also modify an existing or create a new AeroX CSV file, manipulate columns, edit comments, change units and write a new AeroX CSV file, a 'standard' CSV or a JSON file.  
  
The class has multiple uses:  
1. For a user, a few keystrokes allows examination of the data, quick plots as line or contour, and simple filtering (e.g. selecting just a single Reynolds number case and writing a new file).  
2. For development of the NWTF database, it allows us to script the import, manipulation and checking of other Universities' data, and finally outputting in the AeroX format.  
3. For modellers, it allows existing (often sparse) experimental data to be easily imported into a simulation model, and the interpolation function creates a smooth model of the data for any combination of input variable values. Indeed, the data does not need to be experimental, and it has already been used to generate an AeroX file from a complex aerodynamic simulation model of an EVTOL across a variety of conditions, so that a separate, simple simulation tool can then use the aerodynamic data independently.  
  
It should be noted that although we have developed this file format and tool around aerodynamic data for the NWTF experimental database, it could easily be applied to almost any engineering data.  
