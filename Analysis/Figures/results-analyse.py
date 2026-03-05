# -*- coding: utf-8 -*-

#Get the Numbers named in the Results:


import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path

os.chdir(os.path.dirname(__file__))

# Get Current Working Directory
here = Path(os.getcwd())
sys.path.append(str(here.parent))
parent = here.parent
os.chdir(parent)

from load_data import download_from_zenodo

# Load Risk Data
risk_file = Path("data/risks_data.npy")
if not risk_file.exists():
    download_from_zenodo(
        record_id="17474466",
        filename="risks_data.npy"
    )
else:
    print(f"{risk_file} exists already, skipping download.")
    
risk = np.load("data/risks_data.npy")

# Load ECS data
tcrecs_file = Path("data/tcrecs.txt")
if not tcrecs_file.exists():
    download_from_zenodo(
        filename="tcrecs.txt"
    )
else:
    print(f"{tcrecs_file} exists already, skipping download.")

tcrecs = np.loadtxt("data/tcrecs.txt", delimiter=",")

scenarios = np.array((309, 344, 382, 424, 523, 646, 798))

# ---- Start Analysis ---------
for i, s in enumerate(scenarios):
    print("\n**",s, "ppm Scenario**")
    data = risk[risk[:,1].astype(int)==s]
    data = np.sort(data,0)

    # ECS for Risk > 0%
    idx = np.argmax(data[:, 2] > 0)  
    value = data[idx, 0]
    print("Tipping Risk starts to increase at ECS =",data[idx, 0])
    
    # ECS for Risk > 50%
    if np.any(data[:, 2] > 0.5):
        idx = np.argmax(data[:, 2] > 0.5)
        print("Tipping Risk exceeds 50% at ECS =", data[idx, 0])
    else:
        print("No ECS with tipping risk > 50%")
        
    # ECS for Risk = 100%
    if np.any(data[:, 2] == 1):
        idx = np.argmax(data[:, 2] == 1)
        print("Tipping Risk is 100% at ECS =", data[idx, 0])
    else:
        print("No ECS with tipping risk of 100%")

    # ECS for Risk > 99%
    if np.any(data[:, 2] > 0.99):
        idx = np.argmax(data[:, 2] > 0.99)
        print("Tipping Risk exceeds 99% at ECS =", data[idx, 0])
    else:
        print("No ECS with tipping risk > 99%")
    
    # Maximum Risk
    print("Maximum Tipping Risk is", np.round(np.max(data[:,2]).astype(float)*100),"%.")

# ---- For the 2. Plot ----
for i, s in enumerate(scenarios):
    print("\n**",s, "ppm Scenario**")
    data = risk[risk[:,1].astype(int)==s]
    data = np.sort(data,0)

    # ECS for Risk > 0%
    idx = np.argmax(data[:, 2] >= 0.01)  
    value = data[idx, 0]
    print("Tipping Risk >= 1% start at ECS =",data[idx, 0])
    
    # ECS for Risk > 50%
    if np.any(data[:, 2] > 0.9):
        idx = np.argmax(data[:, 2] > 0.9)
        print("Tipping Risk exceeds 90% at ECS =", data[idx, 0])
    else:
        print("No ECS with tipping risk > 90%")
        
# --- Min, Mean, Max Risks
for i, s in enumerate(scenarios):
    print("\n**",s, "ppm Scenario**")
    data = risk[risk[:,1].astype(int)==s]
    data = np.sort(data,0)
    print(np.min(data[:,2]))
    print(np.mean(data[:,2]))
    print(np.max(data[:,2]))
    
#------------------- Getting the percentiles of the CMIP6 Range ------------------------------------------
# ---  
print("\n\nCMIP6")
ecs = np.sort(tcrecs[:,1])
ecs = ecs[(ecs > 1.8) & (ecs < 5.6)]
percs = [0,10,50,90]
#ecs_perc_array = np.percentile(ecs, percs)
# for uniform 
ecs_perc_array = np.percentile(np.linspace(ecs[0], ecs[-1], num=100), percs)

for i, s in enumerate(scenarios):
    print(f"\n** {s} ppm Scenario **")
    data = risk[risk[:,1].astype(int) == s]
    
    for d, p in enumerate(ecs_perc_array):
        print(percs[d], "Percentile")
        ind = np.argmin(np.abs(tcrecs[:,1] - p))
        val = data[ind, 2]
        print(f"ECS {p:.2f}: {val:.3f}")
    