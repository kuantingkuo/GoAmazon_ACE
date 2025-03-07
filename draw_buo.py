import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import os

cases = ['no-mf-diff', 'no-mf-diff_less-qc', 'weak-mf-diff']
# List of .mat files
mat_files = [
    'GoAmazon_idp=314_kknw25cin_6aces-dynamic_means.02.mat',
    'GoAmazon_idp=314_kknw25cin_6aces-dynamic_means.04.mat',
    'GoAmazon_idp=314_kknw25cin_6aces-dynamic_means.06.mat',
    'GoAmazon_idp=314_kknw25cin_6aces-dynamic_means.08.mat',
    'GoAmazon_idp=314_kknw25cin_6aces-dynamic_means.10.mat',
    'GoAmazon_idp=314_kknw25cin_6aces-dynamic_means.12.mat',
    'GoAmazon_idp=314_kknw25cin_6aces-dynamic_means.14.mat',
    'GoAmazon_idp=314_kknw25cin_6aces-dynamic_means.16.mat',
    'GoAmazon_idp=314_kknw25cin_6aces-dynamic_means.18.mat',
    'GoAmazon_idp=314_kknw25cin_6aces-dynamic_means.20.mat',
    'GoAmazon_idp=314_kknw25cin_6aces-dynamic_means.22.mat',
    'GoAmazon_idp=314_kknw25cin_6aces-dynamic_means.24.mat'
]

for case in cases:
    path = f'/data/W.eddie/GoAmazon_ACE/ACE-control-runs/{case}/'

    #---------------------------------------------------------------------
    # 1. Load MATLAB file and extract variables
    #---------------------------------------------------------------------
    for mat_file in mat_files:
        mat_data = scipy.io.loadmat(os.path.join(path, mat_file))

        # Adjust the variable names below to match those in your .mat file
        B = mat_data['B'][:,:,0]        # Buoyancy array, shape e.g. (nz, nt)
        qc = mat_data['qc'][:,:,0]      # Cloud water (liquid)
        qi = mat_data['qi'][:,:,0]      # Cloud water (ice)
        time = mat_data['tspan'].squeeze()/3600.   # 1D time array
        z = mat_data['z'].squeeze()/1000.          # 1D height array (same dimension as B's first axis)

        # Combine liquid and ice for total cloud
        cloud = qc + qi          # shape (nz, nt)

        #---------------------------------------------------------------------
        # 2. Basic shape checks (optional debugging)
        #---------------------------------------------------------------------
        print("B shape:", B.shape)
        print("cloud shape:", cloud.shape)
        print("time shape:", time.shape, "z shape:", z.shape)

        #---------------------------------------------------------------------
        # 3. Prepare the figure
        #---------------------------------------------------------------------
        fig, ax = plt.subplots(figsize=(8, 5))

        # We assume B has shape (nz, nt). If it’s (nt, nz), transpose it.
        # We want x-axis = time, y-axis = height.
        # Double-check which dimension is time vs. height and transpose if needed:
        if B.shape[0] == time.size and B.shape[1] == z.size:
            B = B.T
            cloud = cloud.T

        #---------------------------------------------------------------------
        # 4. Plot the shading for buoyancy
        #---------------------------------------------------------------------
        # Define the exponential levels for the color bar
        exp_levels = np.concatenate([
            -np.logspace(np.log10(0.01), np.log10(0.08), num=5),
            np.array([0]),
            np.logspace(np.log10(0.01), np.log10(0.08), num=5)
        ])

        # Adjust the pcolormesh to use the new levels
        pcm = ax.pcolormesh(time, z, B,
                            cmap='RdBu_r',
                            shading='auto',
                            norm=plt.Normalize(vmin=-0.08, vmax=0.08))

        # Add colorbar with the new levels
        cbar = plt.colorbar(pcm, ax=ax, orientation='vertical', ticks=exp_levels)
        cbar.set_label(r'Buoyancy [m s$^{-2}$]')
        cbar.ax.set_yticklabels([f'{level:.3f}' for level in exp_levels])

        #---------------------------------------------------------------------
        # 5. Contour for cloud water
        #---------------------------------------------------------------------
        # Define contour levels (e.g. 1e-5, 1e-4, 1e-3, 1e-2, etc.)
        levels = [1e-5, 1e-4, 1e-3, 1e-2]
        cont = ax.contour(time, z, cloud,
                        levels=levels,
                        colors='k', linewidths=1)
        # Label the contours
        ax.clabel(cont, inline=True, fmt='%.0e', fontsize=8)

        #---------------------------------------------------------------------
        # 6. Axes labeling, title, and formatting
        #---------------------------------------------------------------------
        ax.set_xlabel('Time [hr]')
        ax.set_ylabel('Height [km]')
        ax.set_title('Buoyancy & Cloud')  # Adjust as desired

        # Example: if your z is in meters, convert to km
        # If you want a more direct approach, do something like:
        ax.set_ylim([0, 15])  # if z is up to 15 km
        ax.set_yticks(np.arange(0, 16, 2))
        # ax.set_yticklabels(np.arange(0, 16, 2))

        # For time, if it's in hours from 0 to 2, adjust as needed:
        ax.set_xlim([0, 2])
        ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
        ax.set_xticklabels(['00:00', '00:30', '01:00', '01:30', '02:00'])

        # Grid lines (optional)
        ax.grid(True, linestyle=':')

        # Tight layout
        plt.tight_layout()

        #---------------------------------------------------------------------
        # 7. Save or show the figure
        #---------------------------------------------------------------------
        file_number = mat_file.split('.')[-2]
        output_figure = f'/data/W.eddie/GoAmazon_ACE_Figs/Buo_evo_{case}_{file_number}.png'
        plt.savefig(output_figure, dpi=150)
