import os
from statistics import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path
from cmcrameri import cm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import r2_score # Crameri, F. (2018). Scientific colour maps. Zenodo. https://doi.org/10.5281/zenodo.1243862
##############################

# Plot style configuration
plt.style.use('seaborn-v0_8-white')
plt.rcParams['figure.figsize'] = (89/25.4, 60/25.4)
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

# to map tcr to the risk values. via ecs. because the risk data set has only ecs
risk_ids = risk[:, 0]
tcr_ids = tcrecs[:, 1]
tcr_values = np.round(tcrecs[:, 0], 6)
sorted_indices = np.argsort(tcr_ids)
bin_indices = np.searchsorted(tcr_ids, risk_ids, sorter=sorted_indices)
lookup_indices = sorted_indices[bin_indices] #map
aligned_tcr = tcr_values[lookup_indices]
risk = np.column_stack((risk, aligned_tcr))
print(risk[0,:])

scenarios = np.array((309, 344, 382, 424, 523, 646, 798))


#############################################################################

n_colors = 7
scenario_colors = [cm.roma_r(i) for i in np.linspace(0, 1, n_colors)]

myhre = 2.9
print("Median TCR: ", np.median(tcrecs[:,0]))
print("Min TCR: ", np.min(tcrecs[:,0]))
print("Max TCR: ", np.max(tcrecs[:,0]))
# need to make figure with 2 axis
fig, (ax_hist, ax) = plt.subplots(2, 1, sharex=True,
                                  gridspec_kw={'height_ratios': [1, 3], 'hspace': 0.1})


#### subfig 1
sns.kdeplot(tcrecs[:, 0], ax=ax_hist, color = 'dimgray', fill = True, lw=0.5)

ax_hist.set_ylabel("Density")
ax_hist.spines['top'].set_color('white')
ax_hist.spines['left'].set_color('black')
ax_hist.spines['right'].set_color('black')
ax_hist.spines['bottom'].set_color('black')
ax_hist.yaxis.set_ticks([])
ax_hist.tick_params(axis='both', which='major', width=0.5, length=2)
ax_hist.axvline(x = np.median(tcrecs[:,0]), color = "gray", lw=0.6, linestyle="--")
#ax_hist.axvspan(0.5, 2.9, color='lightgrey', alpha=0.3, zorder=1, lw=0)
#ax_hist.axvspan(0.5, 1.8, color='grey', alpha = 0.2, zorder=1, lw=0)
#ax_hist.axvspan(5.6, 6.0, color='grey', alpha=0.2, zorder=1, lw=0)
#ax_hist.axvline(2.9, color="black", zorder=1, lw=0.2)
#ax_hist.axvline(5.6, color="black", zorder=1, lw=0.2)
ax_hist.legend(loc='upper right', bbox_to_anchor=(1.5, 0.97))
ax_hist.annotate("Median TCR", xy=(0.44, 1.07), xycoords='axes fraction')
#ax_hist.annotate("CMIP6\nconstraint", xy=(0.12, 0.68), xycoords='axes fraction', ha='center', color="dimgray")
#ax_hist.annotate("Myhre 2025\nconstraint", xy=(0.33, 0.67), xycoords='axes fraction', ha='center', color="gray")

### subfig 2
for i, s in enumerate(scenarios):
    data = risk[risk[:, 1].astype(int) == s]
    x = data[:, -1].astype(float)
    y = data[:, 2].astype(float)
    
    ax.scatter(x, y, edgecolor = "white",linewidth=0.3, s=7, color=scenario_colors[i], label=f"{s} ppm", zorder=3)
    
ax.axhline(y=0.5, color="black", linestyle="--", lw=0.5)
ax.axhline(y=0, color="black", lw=0.5, zorder=-1)
ax.text(0.4, 0.55, "50% tipping risk", color="black", ha="left")
ax.set_xlabel("Transient Climate Response (°C)")
ax.set_ylabel("Tipping Risk (%)")
ax.set_ylim(-0.1, 1.1)
ax.set_xlim(0.3, 3.0)
ax.set_yticks(np.arange(0, 1.1, 0.1))
ax.set_yticklabels([f"{int(tick * 100)}" for tick in np.arange(0, 1.1, 0.1)])
ax.tick_params(axis='both', which='major', width=0.5, length=2)
ax.axvline(x = np.median(tcrecs[:,0]), color = "gray", lw=0.6, linestyle="--")
#ax.axvline(2.9, color="black", zorder=1, lw=0.2)
#ax.axvline(5.6, color="black", zorder=1, lw=0.2)
#ax.axvspan(0.5, 2.9, color='lightgrey', alpha=0.3, zorder=4, lw=0)
#ax.axvspan(0.5, 1.8, color='grey', alpha = 0.2, zorder=4, lw=0)
#ax.axvspan(5.6, 6.0, color='grey', alpha=0.2, zorder=4, lw=0)
ax.legend(loc='center left', bbox_to_anchor=(1.11, 0.5), title="Scenarios", frameon=False, title_fontsize=6, labelspacing=0.5)
#ax.xaxis.grid()

ax.text(3.16, 0.27, 'Tipping less\nlikely than not',rotation = -90 , horizontalalignment='left', verticalalignment='center')
ax.annotate("", xytext=(1.04, 0.45), xy=(1.04, 0.1), xycoords='axes fraction', arrowprops=dict(arrowstyle="-|>", mutation_scale=10, facecolor="black"))

ax.text(3.16, 0.74, 'Tipping more\nlikely than not',rotation = -90, horizontalalignment='left', verticalalignment='center')
ax.annotate("", xytext=(1.04, 0.55), xy=(1.04, 0.9), xycoords='axes fraction', arrowprops=dict(arrowstyle="-|>", mutation_scale=10, facecolor="black"))

plt.subplots_adjust(right=0.70, left=0.13, top=0.92, bottom=0.13)
#plt.tight_layout()
#plt.savefig("Fig2_TCR.pdf")
#plt.show()
plt.close()
print("Figure saved as Fig2_TCR.pdf")

# -------------------------------
# ECS-TCR relation
X = tcrecs[:, 0].reshape(-1, 1)  # TCR
y = tcrecs[:, 1]                # ECS

# Linear Model Fit
model = LinearRegression().fit(X, y)
y_pred = model.predict(X)

# Stat. values
slope = model.coef_[0]
intercept = model.intercept_
r2 = r2_score(y, y_pred)

plt.scatter(X, y, s=1)
plt.plot(X, y_pred, color='red', label = f'R² = {r2:.2f}')
#plt.title('TCR - ECS Correlation')
plt.ylabel('Equilibrium Climate Sensitivity (ECS)')
plt.xlabel('Transient Climate Response (TCR)')
#plt.text(X.min(), y.max(), f'R² = {r2:.2f}', color='black')
plt.legend()
#plt.savefig("TCR_ECS_correlation.pdf")
#plt.show()
plt.close()
print("TCR-ECS correlation plotted.")
#  ---------------------------------
import string
from scipy.interpolate import griddata
plt.rcParams['figure.figsize'] = (180/25.4, 120/25.4)
y = risk[:,-1] #TCR
x = risk[:,1] #scenario / ppm
r = risk[:,2]

xi = np.linspace(300, 800, 100)
yi = np.linspace(y.min(), y.max(), 100)
Xi, Yi = np.meshgrid(xi, yi)

letters = string.ascii_lowercase
panel_idx = 0

fig = plt.figure() # Added figure size for better spacing
gs = fig.add_gridspec(2, 2, wspace=0.3, hspace=0.4)

# Loop 4 times to fill the 2x2 grid
for idx, r_idx in enumerate(reversed(range(-4, 0))):
    
    # 1. FIX: Calculate 2D row and column positions for the 2x2 grid
    row = idx // 2
    col = idx % 2
    ax = fig.add_subplot(gs[row, col])
    
    # Target column for current risk values (matches your definition)
    # idx=0 -> r_idx=-1 (2nd to last column via r_idx-1)
    current_risk_values = risk[:, r_idx-1]
    
    # Note: If you plan to plot the griddata contour/heatmap, 
    # you would insert ax.contourf(Xi, Yi, Ri) here.
    
    # 2. Plot scatter data for each scenario
    for i, s in enumerate(scenarios):
        data = risk[risk[:, 1].astype(int) == s]
        
        # -1 is the last column (TCR), r_idx-1 tracks the correct risk column
        x_vals = data[:, -1].astype(float) 
        y_vals = data[:, r_idx-1].astype(float) 

        ax.scatter(x_vals, y_vals, edgecolor="white", linewidth=0.3, 
                   color=scenario_colors[i], label=f"{s} ppm", zorder=3)
    
    # --- Styling and Aesthetics ---
    ax.text(0.02, 1.05, letters[panel_idx], transform=ax.transAxes, 
            fontsize=9, fontweight='bold', va='bottom', ha='left')
    panel_idx += 1
        
    ax.axhline(y=0.5, color="black", linestyle="--", lw=0.5)
    ax.axhline(y=0, color="black", lw=0.5, zorder=-1)
    
    ax.set_xlabel("Transient Climate Response (°C)", fontsize=7)
    ax.set_ylabel("Tipping Risk (%)", fontsize=7)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlim(0.3, 3)
    
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.set_yticklabels([f"{int(tick * 100)}" for tick in np.arange(0, 1.1, 0.1)])
    ax.tick_params(axis='both', which='major', width=0.5, length=2, labelsize=6)
    
    # 3. FIX: Move legend to a clean spot (e.g., top-left panel, or upper right corner)
    if idx == 0:
        ax.legend(loc='upper left', ncol=1, title="Scenarios", 
                  frameon=True, framealpha=0.65, fontsize=6, title_fontsize=7)        

plt.savefig("FigS2_TCR.pdf")
#plt.show()       
exit()



# -------------------------------
# Element Specific TCR Risk
plt.rcParams['figure.figsize'] = (180/25.4, 175/25.4)

y = risk[:,-1] #TCR
x = risk[:,1] #scenario / ppm
r = risk[:,2]

xi = np.linspace(300, 800, 100)
yi = np.linspace(y.min(), y.max(), 100)
Xi, Yi = np.meshgrid(xi, yi)

letters = string.ascii_lowercase
panel_idx = 0

fig = plt.figure()
gs = fig.add_gridspec(4, 2, wspace=0.3, hspace=0.4)

for idx, r_idx in enumerate(reversed(range(-4, 0))):
    current_risk_values = risk[:, r_idx-1]
    
    # Recalculate Ri for this specific column
    Ri = griddata((risk[:, 1], risk[:, -1]), current_risk_values, (Xi, Yi), method='linear')
    Ri_nn = griddata((risk[:, 1], risk[:, -1]), current_risk_values, (Xi, Yi), method='nearest')
    Ri = np.where(np.isnan(Ri), Ri_nn, Ri)

    # First plot for each
    ax = fig.add_subplot(gs[idx, 0])
    for i, s in enumerate(scenarios):
        data = risk[risk[:, 1].astype(int) == s]
        
        x = data[:, -1].astype(float) #tcr
        y = data[:, r_idx].astype(float)

        color = scenario_colors[i]

        # Plot scatter
        ax.scatter(x, y, edgecolor="white", linewidth=0.3, color=scenario_colors[i], label=f"{s} ppm", zorder=3)
    
    ax.text(0.02, 1.15, letters[panel_idx], transform=ax.transAxes, fontsize=7, fontweight='bold', va='top', ha='right')
    panel_idx += 1
        
    ax.axhline(y=0.5, color="black", linestyle="--", lw=0.5)
    ax.axhline(y=0, color="black", lw=0.5, zorder=-1)
    ax.set_xlabel("Transient Climate Response (°C)")
    ax.set_ylabel("Tipping Risk (%)")
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlim(0.3, 3)
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.set_yticklabels([f"{int(tick * 100)}" for tick in np.arange(0, 1.1, 0.1)])
    ax.tick_params(axis='both', which='major', width=0.5, length=2, labelsize=5)
    if idx == 0:
        ax.legend(loc='right', ncol=1, title="Scenarios", frameon=True, framealpha=0.65, fontsize = 5.5)



    # Second plot - HEATMAP
    
    #from scipy.ndimage import gaussian_filter
    y = risk[:,-1] #TCR
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
    

    # Iso Lines
    iso_r = [0.1, 0.5, 0.9]
    cs = ax.contour(Xi, Yi, Ri, levels=iso_r, colors='black', linewidths=0.5)
    ax.clabel(cs, inline=True, fmt=lambda v: f"{v*100:.0f}%")
    
    # 424
    plt.axvline(x=424, linestyle="--", color="black", lw=0.3)

    plt.xlabel("Atmospheric equilibrium CO$_2$ concentration (ppm)")  
    plt.ylabel("Transient Climate\nResponse (°C)")    
    plt.ylim(0.5, 2.84)  
    plt.xlim(300, 800)
        
    if idx == 0:
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
        

#plt.savefig("FigS2_TCR_with_heatmap.pdf")
