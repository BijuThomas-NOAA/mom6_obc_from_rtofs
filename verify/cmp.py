import sys 
import os
import numpy as np
from netCDF4 import Dataset
# import xarray as xr
import datetime

full_name = os.path.basename(sys.argv[3])
file_name = os.path.splitext(full_name)

with open(file_name[0]+'_butterfly_test.log', 'w') as f:
    with Dataset(sys.argv[1]) as nc1, Dataset(sys.argv[2]) as nc2, Dataset(sys.argv[3]) as nc3:
        f.write(str(datetime.datetime.now())+ '\n')
        f.write("\n"+ "control test directory: "+ str(sys.argv[1])+ '\n')
        f.write("butterfly test directory: "+ str(sys.argv[2])+ '\n')
        f.write("new test directory: "+ str(sys.argv[3])+ '\n\n')

        # Check if the list of variables are the same
        if nc1.variables.keys()!= nc2.variables.keys() or nc1.variables.keys()!= nc3.variables.keys():
            f.write("Variables are different"+ '\n')
            f.close()
            sys.exit(2)

        success = True
        for varname in nc1.variables.keys():
            if varname in ['tmp', 'ugrd', 'vgrd']:
                # First check if each variable has the same dimension
                if np.shape(nc1[varname][:])!=np.shape(nc2[varname][:]) or np.shape(nc1[varname][:])!=np.shape(nc3[varname][:]):
                    f.write(varname+" dimension is different"+ '\n')
                    f.close()
                    sys.exit(2)

                # If dimension is the same, compare data
                else:
                    f.write(varname+':\n\n')
                    for i in range(0,nc1.dimensions['pfull'].size,10):
                        f.write('pfull='+str(i)+':\n\n')
                        f.write("{:<25} {:<25} {:<25}".format('test name','mean', 'stdev')+'\n')
                        rows = [['control', nc1[varname][:,i,:,:].mean(), nc1[varname][:,i,:,:].std()],
                                ['butterfly', nc2[varname][:,i,:,:].mean(), nc2[varname][:,i,:,:].std()],
                                ['newtest', nc3[varname][:,i,:,:].mean(), nc3[varname][:,i,:,:].std()],
                                ['control-butterfly-diff', (nc1[varname][:,i,:,:]-nc2[varname][:,i,:,:]).mean(), (nc1[varname][:,i,:,:]-nc2[varname][:,i,:,:]).std()],
                                ['control-newtest-diff', (nc1[varname][:,i,:,:]-nc3[varname][:,i,:,:]).mean(), (nc1[varname][:,i,:,:]-nc3[varname][:,i,:,:]).std()],]
                        for row in rows:
                            t, m, s = row
                            f.write("{:<25} {:<25} {:<25}".format(t, m, s)+'\n')
                        ratio=(nc1[varname][:,i,:,:]-nc3[varname][:,i,:,:]).std()/(nc1[varname][:,i,:,:]-nc2[varname][:,i,:,:]).std()
                        f.write('\n   ratio='+str(ratio)+'\n\n\n')
                        if ratio>2:
                            success=False

            elif varname in ['pressfc', 'tmpsfc', 'tmp2m', 'ugrd10m', 'vgrd10m']:
                # First check if each variable has the same dimension
                if np.shape(nc1[varname][:])!=np.shape(nc2[varname][:]) or np.shape(nc1[varname][:])!=np.shape(nc3[varname][:]):
                    f.write(varname,"dimension is different"+ '\n')
                    f.close()
                    sys.exit(2)

                # If dimension is the same, compare data
                else:
                    f.write(varname+':\n\n')
                    f.write("{:<25} {:<25} {:<25}".format('test name','mean', 'stdev')+'\n')
                    rows = [['control', nc1[varname][:].mean(), nc1[varname][:].std()],
                            ['butterfly', nc2[varname][:].mean(), nc2[varname][:].std()],
                            ['newtest', nc3[varname][:].mean(), nc3[varname][:].std()],
                            ['control-butterfly-diff', (nc1[varname][:]-nc2[varname][:]).mean(), (nc1[varname][:]-nc2[varname][:]).std()],
                            ['control-newtest-diff', (nc1[varname][:]-nc3[varname][:]).mean(), (nc1[varname][:]-nc3[varname][:]).std()],]
                    for row in rows:
                        t, m, s = row
                        f.write("{:<25} {:<25} {:<25}".format(t, m, s)+'\n')
                    ratio = (nc1[varname][:]-nc3[varname][:]).std()/(nc1[varname][:]-nc2[varname][:]).std()
                    f.write('\n   ratio='+str(ratio)+'\n\n\n')
                    if ratio>2:
                        success=False   

        if success:
            f.write('butterfly test result was successful')
        else:
            f.write('butterfly test result was failed')

        f.close()
        sys.exit(2)
    
    
    
