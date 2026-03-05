import os
from matplotlib.patches import Circle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path
from cmcrameri import cm # Crameri, F. (2018). Scientific colour maps. Zenodo. https://doi.org/10.5281/zenodo.1243862


# Plot style configuration
plt.style.use('seaborn-v0_8-white')
plt.rcParams['figure.figsize'] = (89/25.4, 45/25.4)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

plt.rcParams.update({
    # Font settings
    'font.size': 5,
    'xtick.labelsize': 6,
    'ytick.labelsize': 6,
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

# Get Current Working Directory
here = Path(__file__).parent
sys.path.append(str(here.parent))
parent = here.parent
os.chdir(parent)


from load_data import download_from_zenodo

# Load ECS data
tcrecs_file = Path("data/tcrecs.txt")
if not tcrecs_file.exists():
    download_from_zenodo(filename="tcrecs.txt")
else:
    print(f"{tcrecs_file} exists already, skipping download.")

tcrecs = np.loadtxt("data/tcrecs.txt", delimiter=",")

# Load Risk Data
risk_file = Path("data/risks_data.npy")
if not risk_file.exists():
    download_from_zenodo(filename="risks_data.npy")
else:
    print(f"{risk_file} exists already, skipping download.")
    
risk = np.load("data/risks_data.npy")

#%%
scenarios = np.array((309, 344, 382, 424, 523, 646, 798))
myhre = 2.9 


y = risk[:,0] #ECS
x = risk[:,1] #scenario / ppm
r = risk[:,2]

#%%
# Create a grid for contour plotting
# Determine grid resolution
xi = np.linspace(300, 800, 100)
yi = np.linspace(y.min(), y.max(), 100)
Xi, Yi = np.meshgrid(xi, yi)

# Interpolate r values onto the grid
from scipy.interpolate import griddata
Ri = griddata((x, y), r, (Xi, Yi), method='linear')

# Fill NaN values (outside convex hull) using nearest-neighbor extrapolation
Ri_nn = griddata((x, y), r, (Xi, Yi), method='nearest')
Ri = np.where(np.isnan(Ri), Ri_nn, Ri)

#%%%
# Create the contour plot
fig, ax = plt.subplots()

# Filled contour plot (heatmap-like)
contourf = ax.contourf(Xi, Yi, Ri, levels=100, cmap='YlOrRd')
ax.tick_params(axis='both', which='major', width=0.5, length=2)

# Add colorbar
cbar = plt.colorbar(contourf, ax=ax)
cbar.set_label('Tipping risk (%)')
ticks = np.linspace(0.0, 1.0, 11)
cbar.set_ticks(ticks)
cbar.set_ticklabels([f"{int(t*100)}" for t in ticks])
from matplotlib.ticker import FuncFormatter
# Format colorbar to show percentages (multiply by 100)
cbar.ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'{x*100:.0f}'))
cbar.ax.tick_params(axis='both', which='major', width=0.5, length=2)

# ECS Constraints
plt.axhspan(0.5, 2.9, color='lightgrey', alpha=0.5, zorder=1, lw=0)
plt.axhspan(0.5, 1.8, color='grey', alpha = 0.4, zorder=1, lw=0) 
plt.axhspan(5.6, 6.0, color='grey', alpha=0.4, zorder=1, lw=0)
plt.axhline(2.9, color="black", zorder=1, lw=0.2)
plt.axhline(5.6, color="black", zorder=1, lw=0.2)
plt.annotate("CMIP6\nconstraint", xy=(0.01, 0.02), xycoords='axes fraction', ha='left', color="dimgray")
plt.annotate("Myhre 2025\nconstraint", xy=(0.01, 0.22), xycoords='axes fraction', ha='left', color="gray")

# Iso Lines
iso_r = [0.1, 0.5, 0.9]
cs = ax.contour(Xi, Yi, Ri, levels=iso_r, colors='black', linewidths=0.5)
ax.clabel(cs, inline=True, fmt=lambda v: f"{v*100:.0f}%")

#424
# Target coordinates
target_ppm = 424
target_ecs = 2.9

# Calculate the interpolated risk value at the point (424, 2.9)
risk_at_point = griddata((x, y), r, (target_ppm, target_ecs), method='linear')

# Convert to percentage
risk_percentage = risk_at_point * 100

print(f"The tipping risk at {target_ppm} ppm and {target_ecs}°C ECS is: {risk_percentage:.2f}%")

# 424
plt.axvline(x=424, linestyle="--", color="white", lw=0.3)  # axhline zu axvline geändert
plt.text(433, 3.9, "2025: ~424 ppm", color="white", va="top", size=6)  # Koordin aten und Alignment angepasst
plt.text(433, 3.6, f"Tipping risk > {risk_percentage:.1f}%", color="white", va="top", size=6)  # Koordin aten und Alignment angepasst

from matplotlib.patches import Ellipse

ellipse = Ellipse((424, 2.9), width=20, height=0.3,  # Adjust these values
                  fill=False, edgecolor='black', linewidth=1)
ax.add_patch(ellipse)

plt.xlabel("Atmospheric equilibrium CO$_2$ concentration (ppm)")  
plt.ylabel("Equilibrium Climate Sensitivity (°C)")    
plt.ylim(0.8, 5.79)  
plt.xlim(300,800)

plt.subplots_adjust( top=0.92, bottom=0.2)

plt.savefig("Fig3.pdf")
print("Figure saved as Fig3.pdf")


# --- Find minimum CMIP6 constrained risk
# Target coordinates
target_ppm = 424
target_ecs = 1.8

# Calculate the interpolated risk value at the point (424, 2.9)
risk_at_point = griddata((x, y), r, (target_ppm, target_ecs), method='linear')

# Convert to percentage
risk_percentage = risk_at_point * 100

print(f"The tipping risk at {target_ppm} ppm and {target_ecs}°C ECS is: {risk_percentage:.2f}%")

# --- Find ppm values for specific set risks
from scipy.interpolate import interp1d

# 1. Find the index of the ECS value closest to 3°C in your 'yi' array
target_ecs = 3.0
ecs_idx = np.abs(yi - target_ecs).argmin()

# 2. Get the risk profile at this ECS
risks_at_3deg = Ri[ecs_idx, :]  # Risk values across different PPMs at 3°C

# 3. Create an interpolation function: input risk -> output PPM
# We use xi (the ppm axis) as the values we want to find
ppm_finder = interp1d(risks_at_3deg, xi)

# 4. Calculate the PPM for 10% risk (0.10)
ppm_at_10_risk = ppm_finder(0.10)
print(f"The PPM value for 10% tipping risk at 3°C ECS is approximately: {ppm_at_10_risk:.1f} ppm")

# 4. Calculate the PPM for 50% risk (0.50)
ppm_at_50_risk = ppm_finder(0.50)

print(f"The PPM value for 50% tipping risk at 3°C ECS is approximately: {ppm_at_50_risk:.1f} ppm")
