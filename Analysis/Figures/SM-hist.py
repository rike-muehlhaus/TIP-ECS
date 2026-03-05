import sys
import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt

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


# Plot style configuration
plt.style.use('seaborn-v0_8-white')
plt.rcParams['figure.figsize'] = (89/25.4, 65/25.4)
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

# Histogram with Consraints
data = tcrecs[:, 1]
bins = np.histogram_bin_edges(data, bins=10)
counts, _ = np.histogram(data, bins=bins)
lower, upper = 1.8, 5.6 # CMIP6 Constraints
# colors
bin_centers = (bins[:-1] + bins[1:]) / 2
colors = ['steelblue' if lower <= c <= upper else 'lightsteelblue' for c in bin_centers]
# Plot
plt.figure()
plt.bar(bins[:-1], counts, width=np.diff(bins), color=colors, align='edge', edgecolor='white')
# coloring out-of-cmip6 bins
for i in range(len(bins) - 1):
    if bins[i] < upper < bins[i+1]:
        plt.bar(upper, counts[i], width=bins[i+1]-upper, color='lightsteelblue', align='edge', edgecolor='white')
    if bins[i] < lower < bins[i+1]:
        plt.bar(bins[i], counts[i], width=lower-bins[i], color='lightsteelblue', align='edge', edgecolor='white')
# Constraints lines
plt.axvline(x=lower, color='black', linestyle='dashed')
plt.axvline(x=upper, color='black', linestyle='dashed')
plt.axvline(x = 2.9, color = "red", linestyle = ":", label = "Minimum Likely \nECS after Myhre \net al. 2025")
plt.axvline(x=np.median(tcrecs[:,1]), color='orange', linestyle='dashed', label = "Median ECS")
plt.xlabel("Equilibrium Climate Sensitivity (°C)")
plt.tight_layout()
plt.legend(bbox_to_anchor = (1.05, 0.98))
plt.savefig("ECS-Hist.pdf", bbox_inches='tight')