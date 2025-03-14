import scipy.io
import xarray as xr
import os
import numpy as np
import h5py
import sys
import shutil

case = 'control13579' #'tweaked-linear13579'
path = f'/data/W.eddie/GoAmazon_ACE/ACE-runs/{case}/'
ref_ctl = '/data/W.eddie/GoAmazon_ACE/example.ctl'
ref_ctl_zm = '/data/W.eddie/GoAmazon_ACE/example_zm.ctl'

# Get list of .mat files dynamically
mat_files = [f for f in os.listdir(path) if f.endswith('.mat')]

# List of variables to include
include_vars = {'tspan', 'z', 'zm', 'B', 'theta_e', 'qt', 'mf', 'rho_mf', 'theta', 'RH', 'qsat', 'qv', 'qc', 'ql', 'qi', 'Tv', 'T', 'dtheta_e_pr_accum', 'pr_accum', 'D'}

for mat_file in mat_files:
    # Load the MATLAB .mat file
    print(mat_file)
    try:
        mat_dict = h5py.File(os.path.join(path, mat_file), 'r')
        opened_with_h5py = True
    except OSError:
        mat_dict = scipy.io.loadmat(os.path.join(path, mat_file))
        opened_with_h5py = False
    # Remove meta-keys (those starting with '__') and exclude variables not in the list
    data_vars = {key: np.squeeze(value) for key, value in mat_dict.items() if not key.startswith('__') and key in include_vars}

    # Extend the 'D' variable
    if 'D' in data_vars:
        data_vars['D'] = np.append(data_vars['D'], [11])

    # Add explicit dimension names
    data_vars_with_dims = {}
    for key, value in data_vars.items():
        value = value.squeeze()
        if key == 'mf':
            if opened_with_h5py:
                data_vars_with_dims[key] = (['lon', 't', 'zm'], value)
            else:
                data_vars_with_dims[key] = (['zm', 't', 'lon'], value)
        elif key == 'D':
            data_vars_with_dims['lon'] = (['lon'], value)
        elif key == 'z':
            data_vars_with_dims[key] = (['z'], value)
        elif key == 'zm' or key == 'rho_mf':
            data_vars_with_dims[key] = (['zm'], value)
        elif key == 'tspan':
            data_vars_with_dims['t'] = (['t'], value)
        else:
            if opened_with_h5py:
                data_vars_with_dims[key] = (['lon', 't', 'z'], value)
            else:
                data_vars_with_dims[key] = (['z', 't', 'lon'], value)

    # Convert to an xarray.Dataset
    ds = xr.Dataset(data_vars_with_dims).transpose('t', 'z', 'zm', 'lon')

    # Add attributes
    ds['t'].attrs = {'long_name': 'time', 'units': 'seconds since 2000-01-01 00:00:00', 'calendar': 'standard'}
    ds['z'].attrs = {'long_name': 'height', 'units': 'm'}
    ds['zm'].attrs = {'long_name': 'height', 'units': 'm'}
    ds['lon'].attrs = {'long_name': 'longitude', 'units': 'degrees_east'}

    # Calculate precipitation rate
    pr = ds.pr_accum.sum(dim='z')
    pr[1:] = pr[1:].values - pr[:-1].values
    pr.attrs = {'long_name': 'precipitation rate', 'units': 'mm/s'}
    pr.name = 'pr'
    ds['pr'] = pr/60.

    # Output to NetCDF file
    output_file = os.path.join(path, mat_file.replace('=', '').replace('.mat', '.nc'))
    ds.to_netcdf(output_file)

    # Copy and modify the .ctl file
    ctl_file = output_file.replace('.nc', '.ctl')
    shutil.copy(ref_ctl, ctl_file)
    with open(ctl_file, 'r') as file:
        ctl_content = file.read()
    ctl_content = ctl_content.replace('NCFILE', os.path.basename(output_file))
    ctl_content = ctl_content.replace('TIMESTEP', str(ds['t'].size))
    with open(ctl_file, 'w') as file:
        file.write(ctl_content)

    ctl_file = output_file.replace('.nc', '_zm.ctl')
    shutil.copy(ref_ctl_zm, ctl_file)
    with open(ctl_file, 'r') as file:
        ctl_content = file.read()
    ctl_content = ctl_content.replace('NCFILE', os.path.basename(output_file))
    ctl_content = ctl_content.replace('TIMESTEP', str(ds['t'].size))
    with open(ctl_file, 'w') as file:
        file.write(ctl_content)

    print(f"Dataset for {mat_file} saved to {output_file}")
    print(f"Control file for {mat_file} saved to {ctl_file} and {ctl_file.replace('_zm.ctl', '.ctl')}")
    if opened_with_h5py:
        mat_dict.close()
    else:
        mat_dict.clear()
    del ds
    del data_vars
    del data_vars_with_dims
