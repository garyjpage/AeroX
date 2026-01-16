#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeroX class
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RBFInterpolator
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import NearestNDInterpolator

def extract_array(string_list, start_index, col_start, col_end, string=False):
    """
    Convenience function for reading
    Skips values that can't be converted to floats
    use col_start and col_end to define 
    what to extract
    """
    # this can happen if x_nd is zero
    if col_end<=col_start:
        return []
    
    results = []
    for line in string_list[start_index:]:
        words = [word.strip() for word in line.split(',')[col_start:col_end]]
        
        if string:
            if not words:
                words=[''] # only works if extracting one column
            results.append(words)
  
        else: 
            numbers = []
            for word in words:
                try:
                    numbers.append(float(word))
                except ValueError:
                    print(f"Warning: '{word}' is not a valid float, skipping")
            results.append(numbers)
            
    array = np.array(results)
    return array 


def extract_strings(text, col_start, col_end):
    """
    Convenience function to extract comma-separated strings, 
    remove leading/trailing spaces and remove enclosing quotes, 
    use col_start and col_end to define parts to extract
     """
    # this can happen if x_nd is zero
    if col_end<=col_start:
        return []

    # Split by comma
    parts = text.split(',')[col_start:col_end]
    
    # Strip spaces and quotes from each part
    cleaned = [part.strip().strip('\'"') for part in parts]
    
    return cleaned

def format_number(num, sig_figs=6):
    """
    Convenience function to format numbers, ensures at least one decimal place
    """
 
    formatted = f'{num:.{sig_figs}g}'
    
    # Check if in exponential notation
    if 'e' in formatted:
        # Split into mantissa and exponent
        mantissa, exponent = formatted.split('e')
        # Add .0 if no decimal point in mantissa
        if '.' not in mantissa:
            mantissa += '.0'
        formatted = f'{mantissa}e{exponent}'
    # Regular number without decimal
    elif '.' not in formatted:
        formatted += '.0'
    
    return formatted


class AeroX:
    def __init__(self, filename=None, simple_CSV=False, delimiter_char=',', quote_char='"', comment_char='#',
                 x_nd=0, y_nd=0, nrows=0):
        """
        initialise AeroX instance by reading filename
        splitting out comment section
        processing headers and cleaning up spaces and double quotes
        reading body data into x and y and setting min, max and means
        if no filename is supplied then initialise an empty object
        """

        self.comments = []
        self.x_nd = 0; self.y_nd = 0
        self.constants = False
        
        self.x_longnames = []
        self.x_units =     []
        self.x_names =     []
        self.x =  np.array([])
 
        self.y_longnames = []
        self.y_units =     []
        self.y_names =     []
        self.y =  np.array([])
        
        self.id_name =     []
        self.id = np.array([])
        
                        
        if filename is None: # special case empty
            self.x_nd = x_nd
            self.y_nd = y_nd
        
            if nrows > 0 : # special case create empty array
                self.x = np.zeros((nrows,x_nd))
                self.y = np.zeros((nrows,y_nd))
                                            
            return
        
        if simple_CSV:
            data_line = 1
        else:
            data_line = 4 # location of body of data
        
        # Normal case read from file            
        # read file and split into header and body
        body = self._read(filename, comment_char)
                
        if not simple_CSV:
            # read dimensions of input x and output y in first clean line
            # since a valid csv may have extra commas just read first two columns
            x_nd, y_nd = map(int, body[0].split(',')[:2])
       
        self.constants = (x_nd==0) # special case x_nd zero for constants
 
        self.x_nd = x_nd
        self.y_nd = y_nd

        if not simple_CSV:
            # extract headers in next 3 lines, store as lists
            self.x_longnames =  extract_strings(body[1], 0, x_nd)
            self.x_units =      extract_strings(body[2], 0, x_nd)
            self.y_longnames =  extract_strings(body[1], x_nd, x_nd+y_nd)
            self.y_units =      extract_strings(body[2], x_nd, x_nd+y_nd) 
        
        self.x_names =      extract_strings(body[data_line-1], 0, x_nd)
        self.y_names =      extract_strings(body[data_line-1], x_nd, x_nd+y_nd)
        
        # extract data in remaining lines, store as numpy array            
        self.x = extract_array(body, data_line, 0,    x_nd)
        self.y = extract_array(body, data_line, x_nd, x_nd+y_nd)

        # deal with optional identifier
        self.id_name =  extract_strings(body[data_line-1], x_nd+y_nd, x_nd+y_nd+1 )
        self.id =       extract_array(body, data_line,   x_nd+y_nd, x_nd+y_nd+1, string=True )
       
        # compute min, max and mean of columns of data
        self._set_minmaxmean_x()
        self._set_minmaxmean_y()

    
    def write(self, filename, simple_CSV=False, JSON=False, 
              delimiter_char=',', quote_char='"', comment_char='#', sig_figs=6):
        """
        writes AeroX file
        has the option of a standard format CSV (one header line)
        and the option of a JSON file to describe the data
        default delimiter, quote and comment characters can be over-ridden
        default writes data up to 6 significant figures
        """

        f = open(filename,'w')
        delimiter_char = delimiter_char + ' ' # adds extra space when writing
                
        if not simple_CSV: # default is normal AeroX file
            for comment in self.comments:
                f.write(comment+'\n')
            
            f.write(f'{self.x_nd}, {self.y_nd}\n')           
            f.write(delimiter_char.join(self.x_longnames + self.y_longnames)+'\n')             
            f.write(delimiter_char.join(self.x_units + self.y_units )+'\n') 

        f.write(delimiter_char.join(self.x_names + self.y_names + self.id_name)+'\n')   
        
        if self.constants:
            xy = self.y
        else:
            xy = np.column_stack((self.x, self.y))
                   
        for i,row in enumerate(xy):
            line = delimiter_char.join([format_number(num,sig_figs) 
                                        for num in xy[i]])
 
            if self.id.size > 0 : # if id is not empty
                if self.id[i]: # add to line if we find some text
                    line += delimiter_char + str(self.id[i,0])
            
            line += '\n'
            f.write(line)
               
        f.close()
        
        return
    
       
    def _read(self, filename, comment_char='#'):
         """
         reads AeroX file and splits into comments and body
         the body text is returned and comments stored
         """
         with open(filename, 'r') as f:
             lines = f.readlines()
             
         self.comments = []; body = []
         for line in lines:
             line = line.strip() # remove white spaces on either end
             if line[0]==comment_char:
                 line = line.rstrip(',') # remove multiple commas from excel
                 self.comments.append(line)          
             else:
 #                body.append(line+',') # fudge to allow reading extra column as a tag
                 body.append(line)
         # return body but store comments in instance        
         return body 
     
    
    def _set_minmaxmean_x(self):
        """
        compute min, max and mean of columns of x 
        """
        if self.x_nd>0:
            self.x_min =  np.min(self.x, axis=0)
            self.x_max =  np.max(self.x, axis=0)
            self.x_mean = np.mean(self.x, axis=0)
         
      
    def _set_minmaxmean_y(self):
        """
        compute min, max and mean of columns of y
        """       
        self.y_min =  np.min(self.y, axis=0)
        self.y_max =  np.max(self.y, axis=0)
        self.y_mean = np.mean(self.y, axis=0)
         
      
    def filter_keep(self, **kwargs):
        """
        filter rows based on values of x
        keep rows that match keyword and value
        can be any number of keyword= value and a logical and is used to combine
        keyword will be matched against x_names - cannot filter on y values
        """

        mask = self._set_mask(**kwargs)
                       
        # mask out array (not sure if view or copy)
        self.x =  self.x[mask]
        self.y =  self.y[mask]
        self.id = self.id[mask]
        
        # reset min, max and means
        self._set_minmaxmean_x()
        self._set_minmaxmean_y()


    def filter_remove(self, **kwargs):
       """
       filter rows based on values of x
       remove rows that match keyword and value
       can be any number of keyword= value and a logical and is used to combine
       keyword will be matched against x_names - cannot filter on y values
       """
       
       mask = self._set_mask(**kwargs)
       
       # mask out inverse of array array (not sure if view or copy)
       self.x =  self.x[np.logical_not(mask)]
       self.y =  self.y[np.logical_not(mask)]
       self.id = self.id[np.logical_not(mask)]

       # reset min, max and means
       self._set_minmaxmean_x()
       self._set_minmaxmean_y()


    def _set_mask(self, **kwargs):
       """ convenience function to set mask based on input values """
       # initialise True mask of length matching number of rows
       mask = np.full(self.x.shape[0], True)
       
       # go through keyword arguments and build up mask
       # test against x names followed by y names
       # handle case of NaN
       for keyword, value in kwargs.items():
           try:
               # find column index of input for keyword argument
               xcol = self.x_names.index(keyword)
               if np.isnan(value):
                   mask = np.logical_and(mask, np.isnan(self.x[:,xcol]))
               else:
                   mask = np.logical_and(mask, np.isclose(self.x[:,xcol],value))
           except:
               # find column index of output for keyword argument
               ycol = self.y_names.index(keyword)
               if np.isnan(value):
                   mask = np.logical_and(mask, np.isnan(self.y[:,ycol]))
               else:
                   mask = np.logical_and(mask, np.isclose(self.y[:,ycol],value))
              
           
       return mask

        
    def get_constant(self, name):
       """ special case return value of constant with name"""
       if self.constants:
           # find column index of output for required name
           ycol = self.y_names.index(name)
           return self.y[0,ycol]
       else:
           return 0.0 # really need to throw an exception


    def get_x(self, name):
        """ return a column of input x with name """              
        # look for name in x only
        col = self.x_names.index(name)
        return self.x[:,col]


    def get_y(self, name):              
        """ return a column of output y with name """              
        # look for name in y only
        col = self.y_names.index(name)
        return self.y[:,col]


    def get_x_index(self, name):              
        """ return the column index of input x with name """              
        # look for name in x only
        return self.x_names.index(name)


    def get_y_index(self, name):              
        """ return the column index of output y with name """              
        return self.y_names.index(name)


    def get_column(self, name):
        """ return a column with name trying inputs followed by outputs """              
        try: # look for name in x
            col = self.x_names.index(name)
            return self.x[:,col]
        except: # then look for name in x
            col = self.y_names.index(name)
            return self.y[:,col]


    def replace_y(self, name, column ):
        """ replace column of output with name """
        idx = self.y_names.index(name)
        self.y[:,idx] = column 
        # reset min, max and means
        self._set_minmaxmean_y()
        return


    def insert_y(self, name, longname, unit, column, before=None, after=None):
        """ add a new column of output, default at end
        optionally before or after a named column """
        
        if self.y.size == 0: 
            # case for empty need to set the number of rows to append axis=1
            self.y = np.empty((column.size,0))
            col_idx = 0
        elif before is not None:
            col_idx = self.y_names.index(before)
        elif after is not None:
            col_idx = self.y_names.index(after) + 1
        else:
            col_idx = self.y.shape[1]  # at end

        self.y = np.insert( self.y, col_idx, column, axis=1 )
        self.y_names.insert(col_idx, name)
        self.y_longnames.insert(col_idx, longname)
        self.y_units.insert(col_idx, unit)
        # need to increase y_nd
        self.y_nd = self.y_nd + 1
        # reset min, max and means
        self._set_minmaxmean_y()
        return


    def delete_y(self,name):
        """ delete named output """
        idx = self.y_names.index(name)
        self.y = np.delete(self.y, idx, axis=1)    
        del self.y_names[idx]    
        del self.y_longnames[idx] 
        del self.y_units[idx] 
        self.y_min =  np.delete(self.y_min,  idx)
        self.y_max =  np.delete(self.y_max,  idx)
        self.y_mean = np.delete(self.y_mean, idx)
        # need to reduce y_nd
        self.y_nd = self.y_nd - 1
        # reset min, max and means
        self._set_minmaxmean_y()     
        return


    def insert_x(self, name, longname, unit, column, before=None, after=None):
        """ add a new column of output, default at end 
        optionally before or after a named column """
        
        if self.x.size == 0: 
            # case for empty need to set the number of rows to append axis=1
            self.x = np.empty((column.size,0))
            col_idx = 0
        elif before is not None:
            col_idx = self.x_names.index(before)
        elif after is not None:
            col_idx = self.x_names.index(after) + 1
        else:
            col_idx = self.x.shape[1]  # at end

        self.x = np.insert( self.x, col_idx, column, axis=1 )
        self.x_names.insert(col_idx, name)
        self.x_longnames.insert(col_idx, longname)
        self.x_units.insert(col_idx, unit)       # reset min, max and means
        # need to increase x_nd
        self.x_nd = self.x_nd + 1
        # reset min, max and means
        self._set_minmaxmean_x()
        return


    def delete_x(self,name):
        """ delete input column with name """
        # dangerous to delete inputs, but may be case where column has 
        # identical values due to filtering and so is superfluous
        idx = self.x_names.index(name)
        self.x = np.delete(self.x, idx, axis=1)    
        del self.x_names[idx]     
        del self.x_longnames[idx] 
        del self.x_units[idx] 
        self.x_min =  np.delete(self.x_min,  idx)
        self.x_max =  np.delete(self.x_max,  idx)
        self.x_mean = np.delete(self.x_mean, idx)
        # need to reduce x_nd
        self.x_nd = self.x_nd - 1
        # reset min, max and means
        self._set_minmaxmean_x()     
        return


    def delete_comments(self):
        """ delete all comments """
        self.comments.clear()
        return
    
    
    def add_comment(self, comment, comment_char='#'):
        """ add one line of comment to the existing comments """
        # comment does not contain the # character so need to add and include extra space
        self.comments.append(comment_char+' '+comment)
        return


    def _normalize(self, x): 
        """ normalize input x by min max of stored x (not of argument x) """
        denom = self.x_max - self.x_min
        denom[denom==0.0] = 1.0 # avoid divide by zero
        x_norm = (x - self.x_min)/denom
        return x_norm
 
        
    def add_interpolator(self, interpolator='nearest' ):
        """ create private interpolator """
        if not self.constants:
            # normalize inputs, important for RBF
            x_norm = self._normalize(self.x)
            if interpolator == 'RBF':                
                self._interp = RBFInterpolator(x_norm,self.y)
            elif interpolator == 'linear':
                self._interp = LinearNDInterpolator(x_norm,self.y)
            else:
                # default is guaranteed to work
                self._interp = NearestNDInterpolator(x_norm,self.y)
            return
        else:
            return # really need to throw an exception
    
        
    def interpolate(self,x):
        """ interpolate the outputs y based on array of inputs """
        # interpolator works on normalised inputs
        x_norm = self._normalize(x)
        y = self._interp(x_norm) 
        return y
 
    
    def interpolate_y(self, name, **kwargs):
        """ find single value of y with name based on series of input values
        any undefined inputs are set to the mean"""
        # find column index of output for required name
        ycol = self.y_names.index(name)
 
        # set default inputs for interpolation as the means
        x = self.x_mean.copy() # avoid having a view that over-writes x_mean
        x = np.reshape(x, (1,-1))
 
        # go through keyword arguments
        for keyword, value in kwargs.items():
            # find column index of input for keyword argument
            xcol = self.x_names.index(keyword)
            # ensure inputs are within allowable range of data
            minval = self.x_min[xcol]; maxval = self.x_max[xcol]
            x[0,xcol] = np.clip(value, minval, maxval)
                       
        # use interpolator set up previously
        y = self.interpolate(x)
        
        # y contains all outputs, just need to return value for name           
        return y[0,ycol]
 
       
    def plot(self, xname, yname, interpolate=False, resolution=50, **kwargs):
        """ line plotting of xname vs yname, use input values to downselect
        default is discrete points, if interpolation available will show smooth
        line with resolution points """
        # extract columns
        x_i = self.get_x(xname);  y_i = self.get_y(yname)
        
        # find indices
        x_index = self.get_x_index(xname);  y_index = self.get_y_index(yname)
        
        # use indices to extract units
        x_unit = self.x_units[x_index];     y_unit = self.y_units[y_index]
        
        # mask to keep rows corresponding to keyword arguments
        mask = self._set_mask(**kwargs)
        # default mode store for points, may be empty!
        x_i_points = x_i[mask];    y_i_points = y_i[mask]
         
        if interpolate:
            # set default inputs for interpolation as the means
            x = self.x_mean.copy() # avoid having a view that over-writes x_mean
            x = np.reshape(x, (1,-1))
     
            # go through keyword arguments
            for keyword, value in kwargs.items():
                # find column index of input for keyword argument
                xcol = self.x_names.index(keyword)
                # ensure inputs are within allowable range of data
                minval = self.x_min[xcol]; maxval = self.x_max[xcol]
                x[0,xcol] = np.clip(value, minval, maxval)
                           
            # replicate this row resolution times
            x = np.repeat(x, resolution, axis=0)
     
            # create resolution points in the range of x
            x_min = self.x_min[x_index]; x_max = self.x_max[x_index];       
            x_i = np.linspace(x_min, x_max, resolution)
    
            # replace the column with this new range of x        
            x[:,x_index] = x_i       
    
            # use interpolator set up previously
            y = self.interpolate(x)
           
            # y contains all outputs,  need to extract required column          
            y_i = y[:,y_index]
 
        # use matplotlib
        fig, ax = plt.subplots()
        plt.grid(True)
        ax.set_xlabel(xname+' ['+x_unit+']'); ax.set_ylabel(yname+' ['+y_unit+']')
        if x_i_points.size != 0: # only if we have valid point data
            ax.scatter(x_i_points, y_i_points)
        if interpolate: # plot continuous line
            ax.plot(x_i, y_i)
        plt.show()
 
        
    def plot_2d(self, x1name, x2name, yname, interpolate=False, resolution=50, **kwargs):
        """ contour plotting with 2 inputs and 1 output, use input values to downselect
        default is to triangulate points, if interpolation available will use
        that function with resolution points """
        # extract columns
        x1_i = self.get_x(x1name);  x2_i = self.get_x(x2name)
        y_i = self.get_y(yname)
        
        # find indices
        x1_index = self.get_x_index(x1name);  x2_index = self.get_x_index(x2name); 
        y_index = self.get_y_index(yname)
        
        # use indices to extract units
        x1_name = self.x_names[x1_index];  x2_name = self.x_names[x2_index];    
        y_name = self.y_names[y_index]
        x1_unit = self.x_units[x1_index];  x2_unit = self.x_units[x2_index];    
        y_unit = self.y_units[y_index]
        
        if interpolate:
            # set default inputs for interpolation as the means
            x = self.x_mean.copy() # avoid having a view that over-writes x_mean
            x = np.reshape(x, (1,-1))
     
            # go through keyword arguments
            for keyword, value in kwargs.items():
                # find column index of input for keyword argument
                xcol = self.x_names.index(keyword)
                # ensure inputs are within allowable range of data
                minval = self.x_min[xcol]; maxval = self.x_max[xcol]
                x[0,xcol] = np.clip(value, minval, maxval)
                           
            # replicate this row resolution times
            x = np.repeat(x, resolution*resolution, axis=0)
     
            # create resolution points in the range of x1 and x2
            x_min = self.x_min[x1_index]; x_max = self.x_max[x1_index];       
            x1_i = np.linspace(x_min, x_max, resolution)

            x_min = self.x_min[x2_index]; x_max = self.x_max[x2_index];       
            x2_i = np.linspace(x_min, x_max, resolution)
            
            x1g, x2g = np.meshgrid(x1_i,x2_i)
            
            # replace the columns with this new range of x        
            x[:,x1_index] = x1g.flatten()       
            x[:,x2_index] = x2g.flatten()       
    
            # use interpolator set up previously
            y = self.interpolate(x)
           
            # y contains all outputs,  need to extract required column          
            y_i = y[:,y_index]
            
            yg = y_i.reshape(resolution,resolution)

        if interpolate:
            # use matplotlib separate figures
            fig, ax = plt.subplots()
            ax.set_xlabel(x1_name+' ['+x1_unit+']'); 
            ax.set_ylabel(x2_name+' ['+x2_unit+']')
            ax.contour(x1g, x2g, yg, colors='k')
            cont = ax.contourf(x1g, x2g, yg)
            fig.colorbar(cont)
            ax.set_title(y_name+' ['+y_unit+']')            
            plt.show()
            
        else:
            # mask to keep rows corresponding to keyword arguments
            mask = self._set_mask(**kwargs)
            # default mode store for points, may be empty!
            x1_i_points = x1_i[mask];   x2_i_points = x2_i[mask];   
            y_i_points = y_i[mask]
                  
            # use matplotlib separate figures
            fig, ax = plt.subplots()
            ax.set_xlabel(x1_name+' ['+x1_unit+']'); 
            ax.set_ylabel(x2_name+' ['+x2_unit+']')
            ax.plot(x1_i_points, x2_i_points, 'x', markersize=8, color='k')
            tcf= ax.tricontourf(x1_i_points, x2_i_points, y_i_points)
            fig.colorbar(tcf)
            ax.tricontour(x1_i_points, x2_i_points, y_i_points, colors='k')
            ax.set_title(y_name+' ['+y_unit+']')
            plt.show()
            

        return