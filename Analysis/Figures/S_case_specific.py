import os
import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path
from cmcrameri import cm # Crameri, F. (2018). Scientific colour maps. Zenodo. https://doi.org/10.5281/zenodo.1243862
##############################

# Plot style configuration
plt.style.use('seaborn-v0_8-white')
plt.rcParams['figure.figsize'] = (180/25.4, 175/25.4)
plt.rcParams['font.family'] = 'sans-serif'

plt.rcParams.update({
    # Font settings
    'font.size': 7,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'axes.titlesize': 6,
    'axes.labelsize': 6,
    'legend.fontsize': 6,
    
    # Spacing
    'axes.titlepad': 10,
    'axes.labelpad': 4,
    'xtick.major.pad': 3,
    'ytick.major.pad': 3,
    
    # Tick parameters
    'xtick.major.size': 2,
    'ytick.major.size': 2,
    'xtick.major.width': 1,
    'ytick.major.width': 1,
    
    'lines.linewidth': 1.0,
    'lines.markersize': 2,
    'axes.linewidth': 0.5,
})


#%%
# D A T A 

# Current folder
here = Path(__file__).resolve().parent
sys.path.append(str(here.parent))
parent = here.parent
os.chdir(parent)

from load_data import download_from_zenodo

# Load ECS data
tcrecs_file = Path("data/tcrecs.txt")
if not tcrecs_file.exists():
    download_from_zenodo(
        filename="tcrecs.txt"
    )
else:
    print(f"{tcrecs_file} exists already, skipping download.")

tcrecs = np.loadtxt("data/tcrecs.txt", delimiter=",")

# Load Risk Data
risk_file = Path("data/risks_data.npy")
if not risk_file.exists():
    download_from_zenodo(
        filename="risks_data.npy"
    )
else:
    print(f"{risk_file} exists already, skipping download.")
    
risk = np.load("data/risks_data.npy")

ecs = np.round(tcrecs[:,1],6) 
scenarios = np.array((309, 344, 382, 424, 523, 646, 798))

n_colors = 7
scenario_colors = [cm.roma_r(i) for i in np.linspace(0, 1, n_colors)]

myhre = 2.9


# labels = ['$\geq$ 1', '$\geq$ 2','$\geq$ 3','all 4', 'GIS', 'AMOC', 'WAIS', 'AMAZ']
###########################################################
# Prep Second Subfigure of each case
#rlabels = ['5 % Tipping Risk','10 % Tipping Risk', '25 % Tipping Risk','50 % Tipping Risk','75 % Tipping Risk', '90 % Tipping Risk', '95 % Tipping Risk']
#colors = scenario_colors

#from scipy.ndimage import gaussian_filter

y = risk[:,0] #ECS
x = risk[:,1] #scenario / ppm
r = risk[:,2]

# Create a grid for contour plotting
# Determine grid resolution
xi = np.linspace(300, 800, 100)
yi = np.linspace(y.min(), y.max(), 100)
Xi, Yi = np.meshgrid(xi, yi)

# Interpolate r values onto the grid
from scipy.interpolate import griddata
# Ri = griddata((x, y), r, (Xi, Yi), method='linear')

# # Fill NaN values (outside convex hull) using nearest-neighbor extrapolation
# Ri_nn = griddata((x, y), r, (Xi, Yi), method='nearest')
# Ri = np.where(np.isnan(Ri), Ri_nn, Ri)

#### Plot ######################################
import string
letters = string.ascii_lowercase
panel_idx = 0

fig = plt.figure()
gs = fig.add_gridspec(4, 2, wspace=0.3, hspace=0.4)

for idx, r_idx in enumerate(range(-8, -4)):
    # 1. Update the interpolation data for the CURRENT tipping element
    current_risk_values = risk[:, r_idx]

    # Recalculate Ri for this specific column
    Ri = griddata((risk[:, 1], risk[:, 0]), current_risk_values, (Xi, Yi), method='linear')
    Ri_nn = griddata((risk[:, 1], risk[:, 0]), current_risk_values, (Xi, Yi), method='nearest')
    Ri = np.where(np.isnan(Ri), Ri_nn, Ri)

    # First plot for each
    ax = fig.add_subplot(gs[idx, 0])
    for i, s in enumerate(scenarios):
        data = risk[risk[:, 1].astype(int) == s]
        
        x = data[:, 0].astype(float)
        y = data[:, r_idx].astype(float)

        color = scenario_colors[i]

        # Plot scatter
        ax.scatter(x, y, edgecolor="white", linewidth=0.3, color=scenario_colors[i], label=f"{s} ppm", zorder=3)
    
    ax.text(0.02, 1.15, letters[panel_idx], transform=ax.transAxes, fontsize=7, fontweight='bold', va='top', ha='right')
    panel_idx += 1
        
    ax.axhline(y=0.5, color="black", linestyle="--", lw=0.5)
    ax.axhline(y=0, color="black", lw=0.5, zorder=-1)
    ax.set_xlabel("Equilibrium Climate Sensitivity (°C)")
    ax.set_ylabel("Tipping Risk (%)")
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlim(0.5, 6)
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.set_yticklabels([f"{int(tick * 100)}" for tick in np.arange(0, 1.1, 0.1)])
    ax.tick_params(axis='both', which='major', width=0.5, length=2, labelsize=6)
    ax.axvline(2.9, color="black", zorder=1, lw=0.2)
    ax.axvline(5.6, color="black", zorder=1, lw=0.2)
    ax.axvspan(0.5, 2.9, color='lightgrey', alpha=0.3, zorder=4, lw=0)
    ax.axvspan(0.5, 1.8, color='grey', alpha=0.2, zorder=4, lw=0)
    ax.axvspan(5.6, 6.0, color='grey', alpha=0.2, zorder=4, lw=0)
    
    # Legend for first left plot
    if idx == 0:
        ax.legend(loc='right', ncol=1, title="Scenarios", frameon=True, framealpha=0.65, fontsize = 5.5)
        ax.annotate("CMIP6\nconstraint", xy=(0.12, 0.76), xycoords='axes fraction', ha='center', size=6, color="dimgray")
        ax.annotate("Myhre 2025\nconstraint", xy=(0.33, 0.76), xycoords='axes fraction', ha='center', size=6, color="gray")

        
    # Second plot - HEATMAP
    
    #from scipy.ndimage import gaussian_filter
    y = risk[:,0] #ECS
    x = risk[:,1] #scenario / ppm
    ri = current_risk_values

    # Create a grid for contour plotting
    # Determine grid resolution
    xi = np.linspace(300, 800, 100)
    yi = np.linspace(y.min(), y.max(), 100)
    Xi, Yi = np.meshgrid(xi, yi)

    # Interpolate r values onto the grid
    from scipy.interpolate import griddata
    Ri = griddata((x, y), ri, (Xi, Yi), method='linear')

    # Fill NaN values (outside convex hull) using nearest-neighbor extrapolation
    Ri_nn = griddata((x, y), ri, (Xi, Yi), method='nearest')
    Ri = np.where(np.isnan(Ri), Ri_nn, Ri)
    
    ax = fig.add_subplot(gs[idx, 1])
    
    # Filled contour plot (heatmap-like)
    contourf = ax.contourf(Xi, Yi, Ri, levels=100, cmap='YlOrRd')
    ax.text(0.02, 1.15, letters[panel_idx] , transform=ax.transAxes, fontsize=7, fontweight='bold', va='top', ha='right')
    panel_idx+=1
    ax.tick_params(axis='both', which='major')
    
    # ECS Constraints
    plt.axhspan(0.5, 2.9, color='lightgrey', alpha=0.5, zorder=1, lw=0)
    plt.axhspan(0.5, 1.8, color='grey', alpha=0.4, zorder=1, lw=0) 
    plt.axhspan(5.6, 6.0, color='grey', alpha=0.4, zorder=1, lw=0)
    plt.axhline(2.9, color="black", zorder=1, lw=0.2)
    plt.axhline(5.6, color="black", zorder=1, lw=0.2)

    # Iso Lines
    iso_r = [0.1, 0.5, 0.9]
    cs = ax.contour(Xi, Yi, Ri, levels=iso_r, colors='black', linewidths=0.5)
    ax.clabel(cs, inline=True, fmt=lambda v: f"{v*100:.0f}%")
    
    # 424
    plt.axvline(x=424, linestyle="--", color="black", lw=0.3)

    plt.xlabel("Atmospheric equilibrium CO$_2$ concentration (ppm)")  
    plt.ylabel("Equilibrium Climate\nSensitivity (°C)")    
    plt.ylim(0.79, 5.79)  
    plt.xlim(300, 800)
        
    if idx == 0:
        # ECS Constraints
        plt.axhspan(0.5, 2.9, color='lightgrey', alpha=0.5, zorder=1, lw=0)
        plt.axhspan(0.5, 1.8, color='grey', alpha=0.4, zorder=1, lw=0) 
        plt.axhspan(5.6, 6.0, color='grey', alpha=0.4, zorder=1, lw=0)
        plt.axhline(2.9, color="black", zorder=1, lw=0.2)
        plt.axhline(5.6, color="black", zorder=1, lw=0.2)
        plt.annotate("CMIP6\nconstraint", xy=(0.01, 0.02), xycoords='axes fraction', ha='left', size=6, color="dimgray")
        plt.annotate("Myhre 2025\nconstraint", xy=(0.01, 0.22), xycoords='axes fraction', ha='left', size=6, color="gray")

        # 424
        plt.axvline(x=424, linestyle="--", color="white", lw=0.3)
        plt.text(433, 4.5, "2025: ~424 ppm", color="white", va="top", size=7)
        
        
        # #Add colorbar inside plot (inset)
        from mpl_toolkits.axes_grid1.inset_locator import inset_axes
        axins = inset_axes(ax, width="4%", height="80%", loc='center right', 
                          bbox_to_anchor=(-0.13, 0, 1, 1), bbox_transform=ax.transAxes)
        cbar = plt.colorbar(contourf, cax=axins)
        cbar.set_label('Tipping risk (%)')
        ticks = np.linspace(0.0, 1.0, 6)
        cbar.set_ticks(ticks)
        cbar.set_ticklabels([f"{int(t*100)}" for t in ticks])
        cbar.ax.tick_params(axis='both', which='major', labelsize=6)
        

plt.savefig("FigS1.pdf")

####S2 Plot Elemet ######################################
import string
letters = string.ascii_lowercase
panel_idx = 0

fig = plt.figure()
gs = fig.add_gridspec(4, 2, wspace=0.3, hspace=0.4)

for idx, r_idx in enumerate(reversed(range(-4, 0))):
    current_risk_values = risk[:, r_idx]
    
    # Recalculate Ri for this specific column
    Ri = griddata((risk[:, 1], risk[:, 0]), current_risk_values, (Xi, Yi), method='linear')
    Ri_nn = griddata((risk[:, 1], risk[:, 0]), current_risk_values, (Xi, Yi), method='nearest')
    Ri = np.where(np.isnan(Ri), Ri_nn, Ri)

    # First plot for each
    ax = fig.add_subplot(gs[idx, 0])
    for i, s in enumerate(scenarios):
        data = risk[risk[:, 1].astype(int) == s]
        
        x = data[:, 0].astype(float)
        y = data[:, r_idx].astype(float)

        color = scenario_colors[i]

        # Plot scatter
        ax.scatter(x, y, edgecolor="white", linewidth=0.3, color=scenario_colors[i], label=f"{s} ppm", zorder=3)
    
    ax.text(0.02, 1.15, letters[panel_idx], transform=ax.transAxes, fontsize=7, fontweight='bold', va='top', ha='right')
    panel_idx += 1
        
    ax.axhline(y=0.5, color="black", linestyle="--", lw=0.5)
    ax.axhline(y=0, color="black", lw=0.5, zorder=-1)
    ax.set_xlabel("Equilibrium Climate Sensitivity (°C)")
    ax.set_ylabel("Tipping Risk (%)")
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlim(0.5, 6)
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.set_yticklabels([f"{int(tick * 100)}" for tick in np.arange(0, 1.1, 0.1)])
    ax.tick_params(axis='both', which='major', width=0.5, length=2, labelsize=5)
    ax.axvline(2.9, color="black", zorder=1, lw=0.2)
    ax.axvline(5.6, color="black", zorder=1, lw=0.2)
    ax.axvspan(0.5, 2.9, color='lightgrey', alpha=0.3, zorder=4, lw=0)
    ax.axvspan(0.5, 1.8, color='grey', alpha=0.2, zorder=4, lw=0)
    ax.axvspan(5.6, 6.0, color='grey', alpha=0.2, zorder=4, lw=0)
    
    # Legend for first left plot
    if idx == 0:
        ax.legend(loc='right', ncol=1, title="Scenarios", frameon=True, framealpha=0.65, fontsize = 5.5)
        ax.annotate("CMIP6\nconstraint", xy=(0.12, 0.76), xycoords='axes fraction', ha='center', size=6, color="dimgray")
        ax.annotate("Myhre 2025\nconstraint", xy=(0.33, 0.76), xycoords='axes fraction', ha='center', size=6, color="gray")

        
    # Second plot - HEATMAP
    
    #from scipy.ndimage import gaussian_filter
    y = risk[:,0] #ECS
    x = risk[:,1] #scenario / ppm
    ri = current_risk_values
    print(np.max(ri))

    # Create a grid for contour plotting
    # Determine grid resolution
    xi = np.linspace(300, 800, 100)
    yi = np.linspace(y.min(), y.max(), 100)
    Xi, Yi = np.meshgrid(xi, yi)

    # Interpolate r values onto the grid
    Ri = griddata((x, y), ri, (Xi, Yi), method='linear')

    # Fill NaN values (outside convex hull) using nearest-neighbor extrapolation
    Ri_nn = griddata((x, y), ri, (Xi, Yi), method='nearest')
    Ri = np.where(np.isnan(Ri), Ri_nn, Ri)
    
    ax = fig.add_subplot(gs[idx, 1])
    
    # Filled contour plot (heatmap-like)
    contourf = ax.contourf(Xi, Yi, Ri, levels=np.linspace(0, 1, 101), cmap='YlOrRd')
    ax.text(0.02, 1.15, letters[panel_idx] , transform=ax.transAxes, fontsize=7, fontweight='bold', va='top', ha='right')
    panel_idx+=1
    ax.tick_params(axis='both', which='major')
    
    # ECS Constraints
    plt.axhspan(0.5, 2.9, color='lightgrey', alpha=0.5, zorder=1, lw=0)
    plt.axhspan(0.5, 1.8, color='grey', alpha=0.4, zorder=1, lw=0) 
    plt.axhspan(5.6, 6.0, color='grey', alpha=0.4, zorder=1, lw=0)
    plt.axhline(2.9, color="black", zorder=1, lw=0.2)
    plt.axhline(5.6, color="black", zorder=1, lw=0.2)

    # Iso Lines
    iso_r = [0.1, 0.5, 0.9]
    cs = ax.contour(Xi, Yi, Ri, levels=iso_r, colors='black', linewidths=0.5)
    ax.clabel(cs, inline=True, fmt=lambda v: f"{v*100:.0f}%")
    
    # 424
    plt.axvline(x=424, linestyle="--", color="black", lw=0.3)

    plt.xlabel("Atmospheric equilibrium CO$_2$ concentration (ppm)")  
    plt.ylabel("Equilibrium Climate\nSensitivity (°C)")    
    plt.ylim(0.79, 5.79)  
    plt.xlim(300, 800)
        
    if idx == 0:
        # ECS Constraints
        plt.axhspan(0.5, 2.9, color='lightgrey', alpha=0.5, zorder=1, lw=0)
        plt.axhspan(0.5, 1.8, color='grey', alpha=0.4, zorder=1, lw=0) 
        plt.axhspan(5.6, 6.0, color='grey', alpha=0.4, zorder=1, lw=0)
        plt.axhline(2.9, color="black", zorder=1, lw=0.2)
        plt.axhline(5.6, color="black", zorder=1, lw=0.2)
        plt.annotate("CMIP6\nconstraint", xy=(0.01, 0.02), xycoords='axes fraction', ha='left', size=6, color="dimgray")
        plt.annotate("Myhre2025\nconstraint", xy=(0.01, 0.22), xycoords='axes fraction', ha='left', size=6, color="gray")

        # 424
        plt.axvline(x=424, linestyle="--", color="white", lw=0.3)
        plt.text(433, 4.5, "2025: ~424 ppm", color="white", va="top", size=7)
        
        
        # #Add colorbar inside plot (inset)
        from mpl_toolkits.axes_grid1.inset_locator import inset_axes
        axins = inset_axes(ax, width="4%", height="80%", loc='center right', 
                          bbox_to_anchor=(-0.13, 0, 1, 1), bbox_transform=ax.transAxes)
        cbar = plt.colorbar(contourf, cax=axins)
        cbar.set_label('Tipping risk (%)')
        ticks = np.linspace(0.0, 1.0, 6)
        cbar.set_ticks(ticks)
        cbar.set_ticklabels([f"{int(t*100)}" for t in ticks])
        cbar.ax.tick_params(axis='both', which='major', labelsize=6)
        

plt.savefig("FigS2.pdf")