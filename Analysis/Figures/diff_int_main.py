import os
import numpy as np
import matplotlib.pyplot as plt
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

def set_axis_style(ax, labels):
    ax.set_xticks(np.arange(1, len(labels) + 1), labels=labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    ax.set_xlabel('Stabilization Level (ppm CO2)')


# need to make figure with 2 axis
fig, (ax) = plt.subplots(1, 1)

### subfig 
all_data = []
for i, s in enumerate(reversed(scenarios)):
    data = risk[risk[:, 1].astype(int) == s]
    x = data[:, 0].astype(float)
    y = data[:, 2].astype(float)
    color = scenario_colors[::-1][i]
    
    no_interactions_data = risk_no_interactions[risk_no_interactions[:, 1].astype(int) == s]
    no_interactions_x = no_interactions_data[:, 0].astype(float)
    no_interactions_y = no_interactions_data[:, 2].astype(float)

    dif = np.sqrt((y-no_interactions_y)**2)
    all_data.append(dif)
    print(np.max(all_data))

    #ax.scatter(x, y, color=color, zorder=4,  linewidth=0.3, s=7, label=f"{s} ppm")
    #ax.scatter(no_interactions_x, no_interactions_y, linewidth=0.1, alpha = 0.4, s=5, color=color, zorder=3)
    #ax.plot(x,dif, color=color, zorder=4, alpha = 0.7,  label=f"{s} ppm")    
parts = ax.violinplot(all_data, showmedians=True)    
for body, color in zip(parts['bodies'], scenario_colors):
    body.set_facecolor(color)
    body.set_edgecolor(color)
    body.set_alpha(0.5)


if 'cmedians' in parts:
    parts['cmedians'].set_color('black')
    parts['cmedians'].set_linewidth(0.8)

# Extrema lines (min/max and center bars)
for key in ['cmins', 'cmaxes', 'cbars']:
    if key in parts:
        parts[key].set_color('black')
        parts[key].set_linewidth(0.5)

set_axis_style(ax, scenarios)
ax.set_ylabel("$\Delta$ Tipping Risk (%)")
ax.set_yticks(np.arange(0, 0.151, 0.05))
ax.set_yticklabels([f"{int(tick * 100)}" for tick in np.arange(0, 0.151, 0.05)])
ax.tick_params(axis='both', which='major', width=0.5, length=2)
#ax.axhline(y=0.13, color="black",linestyle = "--", lw=0.5, zorder=-1)
#ax.text(6.15, 0.133, "13% Difference", color="black", ha="left")
for i, data in enumerate(all_data, start=1):
    ymax = max(data)
    display_text = max(data)*100

    ax.text(
        i,                  # x-position
        ymax,               # y-position
        f'{display_text:.2f}',      # displayed text
        ha='center',
        va='bottom'
    )
plt.subplots_adjust(right=0.95, left=0.13, top=0.93, bottom=0.19)
#plt.tight_layout()
#plt.show()

plt.savefig("Fig2_diff_violins.pdf")
