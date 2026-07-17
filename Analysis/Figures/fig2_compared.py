'''
sort the ecs in ascending order, then i can likely do a lineplot
and do not have to fit (i hope). 
Then plot the no interactions as points. 
maybe no constraints needed? 
the analysis will be interesting.
'''
import os
from matplotlib.lines import Line2D
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path
from cmcrameri import cm # Crameri, F. (2018). Scientific colour maps. Zenodo. https://doi.org/10.5281/zenodo.1243862
##############################

# Plot style configuration
plt.style.use('seaborn-v0_8-white')
plt.rcParams['figure.figsize'] = (89/25.4, 55/25.4)
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

# Load Risk Data
risk_file = Path("data/risks_data.npy")
if not risk_file.exists():
    download_from_zenodo(
        filename="risks_data.npy"
    )
else:
    print(f"{risk_file} exists already, skipping download.")

risk = np.load("data/risks_data.npy")
risk = risk[np.argsort(risk[:,0])]

# Load Risk Data
risk_file_ni = Path("data/risks_data_no_interactions.npy")
if not risk_file_ni.exists():
    download_from_zenodo(
        filename="risks_data_no_interactions.npy"
    )
else:
    print(f"{risk_file_ni} exists already, skipping download.")

not_interactions_risk = np.load("data/risks_data_no_interactions.npy")

ecs = np.round(tcrecs[:,1],6) 
scenarios = np.array((309, 344, 382, 424, 523, 646, 798))

n_colors = 7
scenario_colors = [cm.roma_r(i) for i in np.linspace(0, 1, n_colors)]

myhre = 2.9

# need to make figure with 2 axis
fig, ax = plt.subplots()

### 
for i, s in enumerate(reversed(scenarios)):
    data = risk[risk[:, 1].astype(int) == s]
    x = data[:, 0].astype(float)
    y = data[:, 2].astype(float)
    color = scenario_colors[::-1][i]

    no_interactions_data = not_interactions_risk[not_interactions_risk[:, 1].astype(int) == s]
    no_interactions_x = no_interactions_data[:, 0].astype(float)
    no_interactions_y = no_interactions_data[:, 2].astype(float)
    
    ax.plot(x, y, color=color, zorder=2, alpha=0.4)
    ax.scatter(no_interactions_x, no_interactions_y, edgecolor="white", linewidth=0.3, s=7, color=color, label=f"{s} ppm", zorder=5)

ax.axhline(y=0.5, color="black", linestyle="--", lw=0.5)
ax.axhline(y=0, color="black", lw=0.5, zorder=-1)
ax.text(4.55, 0.42, "50% tipping risk", color="black", ha="left")
ax.annotate("CMIP6\nconstraint", xy=(0.12, 1.02), xycoords='axes fraction', ha='center', color="dimgray")
ax.annotate("Myhre 2025\nconstraint", xy=(0.33, 1.02), xycoords='axes fraction', ha='center', color="gray")
ax.set_xlabel("Equilibrium Climate Sensitivity (°C)")
ax.set_ylabel("Tipping Risk (%)")
ax.set_ylim(-0.08, 1.08)
ax.set_xlim(0.5, 6)
ax.set_yticks(np.arange(0, 1.1, 0.1))
ax.set_yticklabels([f"{int(tick * 100)}" for tick in np.arange(0, 1.1, 0.1)])
ax.tick_params(axis='both', which='major', width=0.5, length=2)
#ax.axvline(x = np.median(tcrecs[:,1]), color = "gray", lw=0.6, linestyle="--")
ax.axvline(2.9, color="black", zorder=1, lw=0.2)
ax.axvline(5.6, color="black", zorder=1, lw=0.2)
ax.axvspan(0.5, 2.9, color='lightgrey', alpha=0.3, zorder=3, lw=0)
ax.axvspan(0.5, 1.8, color='grey', alpha = 0.2, zorder=3, lw=0)
ax.axvspan(5.6, 6.0, color='grey', alpha=0.2, zorder=3, lw=0)
# Custom legend
# First legend: colors (scenarios)
color_legend = ax.legend(loc='center left', bbox_to_anchor=(1.12, 0.4), title="Scenarios", frameon=False, title_fontsize=6, labelspacing=0.5)

# Keep it when adding another legend
ax.add_artist(color_legend)
# Second legend: line vs point meaning
style_handles = [
    Line2D([0], [0], color="black", lw=1, label="Interactions"),
    Line2D(
        [0], [0],
        marker="o",
        linestyle="None",
        color="black",
        markersize=1,
        label="No interactions"
    )
]

ax.legend(handles=style_handles,loc="upper right",bbox_to_anchor=(1.59, 0.99), frameon=False, title_fontsize=6, labelspacing=0.5)

ax.text(6.32, 0.27, 'Tipping less\nlikely than not',rotation = -90 , horizontalalignment='left', verticalalignment='center')
ax.annotate("", xytext=(1.04, 0.45), xy=(1.04, 0.1), xycoords='axes fraction', arrowprops=dict(arrowstyle="-|>", mutation_scale=10, facecolor="black"))

ax.text(6.32, 0.74, 'Tipping more\nlikely than not',rotation = -90, horizontalalignment='left', verticalalignment='center')
ax.annotate("", xytext=(1.04, 0.55), xy=(1.04, 0.9), xycoords='axes fraction', arrowprops=dict(arrowstyle="-|>", mutation_scale=10, facecolor="black"))

plt.subplots_adjust(right=0.68, left=0.13, top=0.85, bottom=0.21)
#plt.tight_layout()
#plt.show()
plt.savefig("Fig2_compared.pdf")
plt.close()
print("Figure saved as Fig2_compared.pdf")