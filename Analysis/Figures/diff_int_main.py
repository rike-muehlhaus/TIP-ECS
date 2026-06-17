import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import sys
from pathlib import Path
from cmcrameri import cm # Crameri, F. (2018). Scientific colour maps. Zenodo. https://doi.org/10.5281/zenodo.1243862
##############################

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
""" 
# Load Risk Data
risk_file = Path("data/risks_data_no_interactions.npy")
if not risk_file.exists():
    download_from_zenodo(
        filename="risks_data_no_interactions.npy"
    )
else:
    print(f"{risk_file} exists already, skipping download.")
 """
risk = np.load("data/risks_data.npy")
risk = risk[np.argsort(risk[:,0])]
risk_no_interactions = np.load("data/risks_data_no_interactions.npy")

ecs = np.round(tcrecs[:,1],6) 
scenarios = np.array((309, 344, 382, 424, 523, 646, 798))


#############################################################################

n_colors = 7
scenario_colors = [cm.roma_r(i) for i in np.linspace(0, 1, n_colors)]

myhre = 2.9

# need to make figure with 2 axis
fig, (ax) = plt.subplots(1, 1)

### subfig 
for i, s in enumerate(reversed(scenarios)):
    data = risk[risk[:, 1].astype(int) == s]
    x = data[:, 0].astype(float)
    y = data[:, 2].astype(float)
    color = scenario_colors[::-1][i]
    
    no_interactions_data = risk_no_interactions[risk_no_interactions[:, 1].astype(int) == s]
    no_interactions_x = no_interactions_data[:, 0].astype(float)
    no_interactions_y = no_interactions_data[:, 2].astype(float)

    dif = np.sqrt((y-no_interactions_y)**2)


    #ax.scatter(x, y, color=color, zorder=4,  linewidth=0.3, s=7, label=f"{s} ppm")
    #ax.scatter(no_interactions_x, no_interactions_y, linewidth=0.1, alpha = 0.4, s=5, color=color, zorder=3)
    #ax.plot(x,dif, color=color, zorder=4, alpha = 0.7,  label=f"{s} ppm")    
    ax.scatter(x,dif, color=color, zorder=4, alpha = 0.7, s = 5, linewidth=0.2, edgecolor = "white",  label=f"{s} ppm")    


    
ax.axhline(y=0.1, color="black", linestyle="--", lw=0.5)
ax.axhline(y=0.05, color="black", linestyle=":", lw=0.5)
ax.axhline(y=0, color="black", lw=0.2, zorder=-1)
ax.set_xlabel("Equilibrium Climate Sensitivity (°C)")
ax.set_ylabel("$\Delta$ Tipping Risk (%)")
ax.set_ylim(-0.01, 0.15)
#ax.set_xlim(0.5, 6)
ax.set_yticks(np.arange(0, 0.15, 0.05))
ax.set_yticklabels([f"{int(tick * 100)}" for tick in np.arange(0, 0.15, 0.05)])
ax.tick_params(axis='both', which='major', width=0.5, length=2)
#ax.axvline(x = np.median(tcrecs[:,1]), color = "gray", lw=0.6, linestyle="--")

# Custom legend
# First legend: colors (scenarios)
color_legend = ax.legend(loc='upper right',bbox_to_anchor=(1.34, 0.89), title="Scenarios", frameon=False, title_fontsize=6, labelspacing=0.5)

# Keep it when adding another legend
ax.add_artist(color_legend)

plt.subplots_adjust(right=0.78, left=0.13, top=0.93, bottom=0.19)
#plt.tight_layout()
#plt.show()

plt.savefig("Fig2_diff.pdf")
print("Figure saved as Fig2_compared.pdf")