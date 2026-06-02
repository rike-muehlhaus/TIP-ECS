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

# Current folder
here = Path(__file__).resolve().parent
sys.path.append(str(here.parent))
parent = here.parent
os.chdir(parent)

from load_data import download_from_zenodo
from load_data import download_and_extract


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

zip_folder = Path("data/Temperature")  
if not zip_folder.exists():
    print("Downloading Temperature Data.")
    download_and_extract(
        record_id="17860768",
        zipname="Temperature.zip"
    )
else:
    print(f"{zip_folder} exists already, skipping download.")

print("Loading Temperature Data.")

T15 = np.load("data/Temperature/T15.npy")
T1 = np.load("data/Temperature/T1.npy")
T3 = np.load("data/Temperature/T3.npy")
T05 = np.load("data/Temperature/T05.npy")
T5 = np.load("data/Temperature/T5.npy")
T4 = np.load("data/Temperature/T4.npy")
T2 = np.load("data/Temperature/T2.npy")

Ts = [T05,T1, T15,T2,T3,T4,T5]
ppms = [309, 344, 382, 424, 523, 646, 798] 

from cmcrameri import cm
n_colors = 7
scenario_colors = [cm.roma_r(i) for i in np.linspace(0, 1, n_colors)]

threshold = 0.0001
tt = Ts
all_steps =[]

for T in tt:
    steps = []

    for i in range(len(tcrecs)):
        temp = T[:, i]
        # Berechne die Differenzen zwischen aufeinanderfolgenden Zeitpunkten
        diffs = np.abs(np.diff(temp))

        # Finde den Zeitpunkt, an dem die Änderung unter dem Schwellenwert bleibt
        stable_point = np.where(diffs < threshold)[0]

        # Wenn der stabile Punkt gefunden wurde, speichere den ersten Zeitpunkt
        if stable_point.size > 0:
            steps.append(stable_point[0] + 1)  # +1 weil `np.diff` einen Index verschiebt
        else:
            steps.append(nt)  # Falls keine Stabilisierung gefunden wurde, gehe bis zum Ende
        
    all_steps.append(steps)

# Deistinguish them again
#steps_T05, steps_T1, steps_T15, steps_T2, steps_T3, steps_T4, steps_T5 = all_steps

all_step = np.array(all_steps)
plt.figure() 

for i, p in enumerate(ppms):
    plt.scatter(tcrecs[:,1], all_step[i,:], s = 0.5, alpha=0.4, label=f"{p} ppm", color=scenario_colors[i])
plt.xlabel('Equilibrium Climate Sensitivity (°C)')
plt.ylabel('Time until Equilibrium reached (Years)')
plt.legend()
plt.savefig("Time-Equilibrium.pdf")
plt.savefig("Time-Equilibrium.svg")
plt.show()
