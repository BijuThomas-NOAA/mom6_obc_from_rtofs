#! /usr/bin/env python3
################################################################################
# Script Name: hafs_mom6_obc_from_rtofs.py
# Authors: NECP/EMC Hurricane Project Team and UFS Hurricane Application Team
# Abstract:
#   This script prepares HAFS MOM6 coupling needed open boundary conditions.
# History:
#   05/13/2023: Added the script for MOM6 coulping in HAFS workflow
# Usage:
#    ./hafs_mom6_obc_from_rtofs.py ssh_file_in ts_file_in uv_file_in hgrid_out_file
################################################################################

import sys
import argparse
import time as Time
import numpy as np
from scipy import interpolate
import xarray as xr
import netCDF4 as nc
try:
    import esmpy as ESMF
except ImportError or ModuleNotFoundError:
    import ESMF as ESMF

from lib_obc_segments import obc_segment
from lib_obc_variable import obc_variable
from lib_obc_vectvariable import obc_vectvariable
from lib_ioncdf import write_obc_file

if __name__ == "__main__":
    #args = parser.parse_args()

    ssh_file_in = "rtofs.n00_ocean_ssh_obc.nc"
    ts_file_in = "rtofs.n00_ocean_ts_obc.nc"
    hgrid_out_file = "ocean_hgrid.nc"

    #print(args)

    st = Time.time()

    #############################################################
    # Open hgrid file
    hgrid_out = xr.open_dataset(hgrid_out_file,decode_times=False)

    # Read dimensions of super grid (ocean_hgrid.nc)
    Nx = hgrid_out.nxp.values[-1]
    Ny = hgrid_out.nyp.values[-1]

    print('Nx = ',Nx,' Ny= ', Ny) # Nx =  4826  Ny=  1928
    #############################################################
    # ---------- define segments on MOM grid -----------------------
    south = obc_segment('segment_002',hgrid_out_file,istart=0,iend=Nx,jstart=0,jend=0)
    print('south.lon:',south.lon)
    print('south.lat:',south.lat)
    ####sys.exit()
    # ---------- define variables on each segment ------------------
    temp_south = obc_variable(south,'temp',geometry='surface',obctype='radiation',use_locstream=True)
    ssh_south = obc_variable(south,'ssh',geometry='line',obctype='flather',use_locstream=True)
    #################################################################
    # Finding regridding weights
    interp_t2s_south_weight = temp_south.interpolate_from(ts_file_in,'pot_temp',frame=0,from_global=False,depthname='Depth',timename='MT',coord_names=['Longitude','Latitude'])
    #################################################################
    # Regridding
    ssh_south.interpolate_from(ssh_file_in,'ssh',frame=0,timename='MT',coord_names=['Longitude','Latitude'],interpolator=interp_t2s_south_weight)


    ##############################################
    # Writing obc ssh to netcdf files
    list_segments_south = [south]

    list_variables_south = [ssh_south]

    list_vectvariables_south = []

    #----------- time --------------------------------------------
    time = temp_south.timesrc
    time.calendar = nc.Dataset(ssh_file_in)['MT'].calendar

    # ---------- write to file -----------------------------------
    fileout_south = ssh_file_in.split('_')[0]+'_ssh_obc_south.nc'

    write_obc_file(list_segments_south,list_variables_south,list_vectvariables_south,time,output=fileout_south)

    et = Time.time()
    elapse_time = et - st
    print('Elapse_time = ', elapse_time, ' seconds')
