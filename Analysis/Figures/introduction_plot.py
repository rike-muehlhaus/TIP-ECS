# %%
# D A T A 
import sys
import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt

# Current folder
here = Path(__file__).resolve().parent

# PyCascades folder
pycascades_folder = here.parent.parent / "PyCascades"

# Add paths to search path
sys.path.append(str(pycascades_folder))
os.chdir(pycascades_folder)

#%%
from load_data import download_from_zenodo, download_and_extract

tcrecs_file = Path("data/tcrecs.txt")
if not tcrecs_file.exists():
    download_from_zenodo(
        filename="tcrecs.txt"
    )
else:
    print(f"{tcrecs_file} exists already, skipping download.")

tcrecs = np.loadtxt("data/tcrecs.txt", delimiter=",")

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

# C O L O R S : Crameri, F. (2018). Scientific colour maps. Zenodo. https://doi.org/10.5281/zenodo.1243862
from cmcrameri import cm
n_colors = 7
scenario_colors = [cm.roma_r(i) for i in np.linspace(0, 1, n_colors)]

#%%

# Plot style configuration
plt.style.use('seaborn-v0_8-white')
plt.rcParams['figure.figsize'] = (180/25.4, 110/25.4)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

plt.rcParams.update({
    # Font settings
    'font.size': 7,
    'xtick.labelsize': 6,
    'ytick.labelsize': 6,
    'axes.titlesize': 7,
    'axes.labelsize': 7,
    'legend.fontsize': 7,
    
    # Spacing
    'axes.titlepad': 10,
    'axes.labelpad': 4,
    'xtick.major.pad': 3,
    'ytick.major.pad': 3,
    
    # Tick parameters
    'xtick.major.size': 3,
    'ytick.major.size': 3,
    'xtick.major.width': 1,
    'ytick.major.width': 1,
    
    'lines.linewidth': 1.0,
    'lines.markersize': 2,
    'axes.linewidth': 0.5,
})

numbering_panels=["b","c","d","e"]

###################################################################
# Plot 1 Prep
ppms = [309, 344, 382, 424, 523, 646, 798]
start_ppm = 278
nt = 5000
years = np.arange(1850, 1850 + nt)

conc_list = []
for i_p, p in enumerate(ppms):
    conc = np.full_like(years, p, dtype=float)
    conc[0] = 278
    j = 0
    slope = (p - start_ppm) / 200
    for i in range(1850, 2050):
        conc[years == i] = start_ppm + j * slope
        j = j + 1
    conc_list.append(conc)
conc_list = np.array(conc_list)

#%%
# Plot 3 prep: PyCascades
from PyCas_plot import run_example_simulation

ScenarioC = [382]
ScenarioT = [15]
temp = T15
GMT_series = temp[:1000, 334]  

sys_var = [1.5, 4.0, 1.5, 3.5, 4.5, 0.2, 1.0, 1.0, 0.2, 0.3, 0.5, 0.15, 1.0, 0.2, 0.15, 1.0, 0.4, 10000, 50, 2000, 100, 100, 0000]
time_scale = True

# Tipping ranges from distribution
limits_gis, limits_thc, limits_wais, limits_amaz, limits_nino = float(sys_var[0]), float(sys_var[1]), float(sys_var[2]), float(sys_var[3]), float(sys_var[4])

# Probability fractions
pf_wais_to_gis, pf_thc_to_gis = float(sys_var[5]), float(sys_var[6])
pf_gis_to_thc, pf_nino_to_thc, pf_wais_to_thc = float(sys_var[7]), float(sys_var[8]), float(sys_var[9])
pf_nino_to_wais, pf_thc_to_wais, pf_gis_to_wais = float(sys_var[10]), float(sys_var[11]), float(sys_var[12])
pf_thc_to_nino, pf_amaz_to_nino = float(sys_var[13]), float(sys_var[14])
pf_nino_to_amaz, pf_thc_to_amaz = float(sys_var[15]), float(sys_var[16])

# Tipping time scales
tau_gis, tau_thc, tau_wais, tau_nino, tau_amaz = float(sys_var[17]), float(sys_var[18]), float(sys_var[19]), float(sys_var[20]), float(sys_var[21])

from earth_sys.timing_no_enso import timing
if time_scale == True:
    print("compute calibration timescale")
    time_props = timing(tau_gis, tau_thc, tau_wais, tau_amaz, tau_nino)
    gis_time, thc_time, wais_time, nino_time, amaz_time = time_props.timescales()
    conv_fac_gis = time_props.conversion()
else:
    gis_time = thc_time = wais_time = nino_time = amaz_time = 1.0
    conv_fac_gis = 1.0

# Create Earth System
from earth_sys.earth_no_enso import earth_system
earth_system_pass = earth_system(gis_time, thc_time, wais_time, nino_time, amaz_time,
                            limits_gis, limits_thc, limits_wais, limits_nino, limits_amaz,
                            pf_wais_to_gis, pf_thc_to_gis, pf_gis_to_thc, pf_nino_to_thc,
                            pf_wais_to_thc, pf_gis_to_wais, pf_thc_to_wais, pf_nino_to_wais,
                            pf_thc_to_nino, pf_amaz_to_nino, pf_nino_to_amaz, pf_thc_to_amaz)

time, gis, thc, wais, amaz = run_example_simulation(earth_system_pass, GMT_series)

ec = 4
element_colors = [cm.batlow(i) for i in np.linspace(0, 1, ec)]



#%%

fig = plt.figure()#layout="tight")

sub = fig.add_subplot(2, 3, 1)
sub.set_xlim(-50,1200)
for ip, p in enumerate(ppms):
    sub.plot(np.arange(0,1000), conc_list[ip, :1000], label=f"{p} ppm", linewidth=1, color = scenario_colors[ip])
    sub.plot(np.arange(1000,1200), conc_list[ip, 1000:1200], linewidth=1, linestyle="--", color = scenario_colors[ip])
sub.set_ylabel('Atmospheric CO$_2$\nconcentration (ppm)')
sub.set_xlabel("Time (years)")
sub.set_xticks(np.arange(0,1201,200))
sub.set_xticklabels(["0","200","400","600","800","1000","50000"])
sub.axvline(1000, color="black", lw=0.5)
sub.legend(frameon=False, loc="upper left", ncol=1, bbox_to_anchor=[-0.1,-0.2])
sub.tick_params(axis='both', which='major', width=0.5, length=2)
sub.annotate(numbering_panels[0], xy=(-0.1, 1.05), xycoords='axes fraction', ha='left', size=7, color="black", weight="bold")

sub.annotate("", xy=(1.20, 0.8), xytext=(1.07, 0.8), xycoords='axes fraction', textcoords='axes fraction', arrowprops=dict(arrowstyle="-|>", color='black'))
sub.annotate("", xy=(1.20, 0.2), xytext=(1.07, 0.2), xycoords='axes fraction', textcoords='axes fraction', arrowprops=dict(arrowstyle="-|>", color='black'))
sub.set_title("Idealized CO2 scenarios", weight = "bold")

# Plot 2: Temperatures
sub = fig.add_subplot(2, 3, 2)
sub.set_xlim(-50,1000)
#sub.fill_between(np.arange(0,1200), np.max(T15[:1200, :], axis=1), np.min(T15[:1200, :], axis=1),  color=scenario_colors[3], alpha=0.3, edgecolor="none")
for i in range(1000):
    plt.plot(T15[:1200, i], color=scenario_colors[2], alpha=0.3, lw=0.5)                
sub.plot(np.arange(0,1200), T15[:1200, 334], color="gray", lw=1, label="382 ppm Scenario:\n$\Delta$GMT under\nmedian ECS")
sub.set_ylabel('$\Delta$GMST (°C)')
sub.set_xlabel("Time (years)")
sub.legend(frameon=False, loc="upper left", fontsize=6)
sub.tick_params(axis='both', which='major', width=0.5, length=2)
sub.annotate(numbering_panels[1], xy=(-0.1, 1.05), xycoords='axes fraction', ha='left', size=7, color="black", weight="bold")
 
sub.annotate("", xy=(1.20, 0.8), xytext=(1.07, 0.8), xycoords='axes fraction', textcoords='axes fraction', arrowprops=dict(arrowstyle="-|>", color='black'))
sub.annotate("", xy=(1.20, 0.2), xytext=(1.07, 0.2), xycoords='axes fraction', textcoords='axes fraction', arrowprops=dict(arrowstyle="-|>", color='black'))
sub.set_title("FaIR", weight="bold")

# Plot 3: PyCascades
sub = fig.add_subplot(2, 3, 3)
sub.set_ylim(-1.15,1.4)
sub.set_xlim(0,1000)
sub.plot(time, gis, label="GIS", color= element_colors[2])
sub.plot(time, thc, label="AMOC", color= element_colors[0])
sub.plot(time, wais, label="WAIS", color= element_colors[3])
sub.plot(time, amaz, label="AMAZ", color= element_colors[1])
sub.set_xlabel("Time (years)")
sub.set_ylabel("Tipping element\nstate")
sub.axhline(0, color="black", lw=0.5, zorder=-1)
sub.set_yticks([-1, 0, 1])
sub.legend(frameon=False, bbox_to_anchor=[0.6,0.07], fontsize=6)
sub.axhspan(1/np.sqrt(3),1.5, color="lightgray", alpha=0.5, lw=0, zorder=-1)
sub.axhspan(-1.5, -1/np.sqrt(3), color="lightgray", alpha=0.5, lw=0, zorder=-1)
sub.annotate("Initial stable\nstate", xy=(0.02, 0.12), xycoords='axes fraction', ha='left', size=7, color="dimgray")
sub.annotate("Alternative\nstable state", xy=(0.02, 0.83), xycoords='axes fraction', ha='left', size=7, color="dimgray")
sub.tick_params(axis='both', which='major', width=0.5, length=2)
sub.annotate(numbering_panels[2], xy=(-0.1, 1.05), xycoords='axes fraction', ha='left', size=7, color="black", weight="bold")
sub.set_title("PyCascades", weight="bold")

# Plot 4: Bifurcation ECS Plot
h = 1.6
r = 0

def f(x, h, r):
    return 2.5 * x**3 - h * x + r

x = np.linspace(-2, 2, 1000)
dxdt = f(x, h, r)

x2 = np.linspace(-np.sqrt(6/27), np.sqrt(6/27), 1000)
unstable = f(x2, h, r)

sub = fig.add_subplot(2, 3, 6)
sub.axhline(0, color='grey')
sub.plot(dxdt, x, color="black")
sub.plot(unstable, x2, color="white", linestyle="--", linewidth=1.5)

sub.set_xlabel("$\Delta$GMST")
sub.set_ylabel("Tipping element state")
sub.set_xticks([-0.4, -0.1, 0.25, np.sqrt(6.5/27), 0.6], 
               ["$T_0$", "$T_1$", "$T_2$", "$T_{crit}$", "$T_3$"])
xlabelcolor = ["grey", scenario_colors[0], scenario_colors[4], "black", scenario_colors[6]]
ymaxlabels = [0.125, 0.15, 0.86, 0.3, 0.9]
sub.tick_params(axis='both', which='major', width=0.5, length=2)

for i, lbl in enumerate(sub.get_xticklabels()):
    lbl.set_color("black") # of use black for the ticks 
    xpos = lbl.get_position()[0]
    sub.axvline(x=xpos, ymax=ymaxlabels[i], color=xlabelcolor[i], linewidth=1, linestyle="--")

sub.scatter(-0.1, -0.83, color= scenario_colors[0], s=12, zorder=5, label="low ECS")
sub.scatter(0.25, 0.87, color=scenario_colors[4], s=12, zorder=5, label="mid ECS")
sub.scatter(0.6, 0.95, color=scenario_colors[6], s=12, zorder=5, label="high ECS")
sub.legend(frameon=False, loc = "upper left", fontsize=6.8)

sub.set_yticks([-1, 0, 1])
sub.set_ylim(-1.2, 1.2)
sub.set_xlim(-0.9, 1.1)

#sub.axhspan(1/np.sqrt(3),1.5, color="lightgray", alpha=0.5, lw=0, zorder=-1)
#sub.axhspan(-1.5, -1/np.sqrt(3), color="lightgray", alpha=0.5, lw=0, zorder=-1)

# Arrows and text - Outside plot area using axis coordinates
sub.text(1.05, 0.25, 'Untipped\nState', transform=sub.transAxes,
         horizontalalignment='left', verticalalignment='center', fontsize=7)
sub.annotate("", xy=(1.03, 0.1), xytext=(1.03, 0.45),
             xycoords='axes fraction', textcoords='axes fraction',
             arrowprops=dict(arrowstyle="-|>", color='black'))

sub.text(1.05, 0.75, 'Tipped\nState', transform=sub.transAxes,
         horizontalalignment='left', verticalalignment='center', fontsize=7)
sub.annotate("", xy=(1.03, 0.9), xytext=(1.03, 0.55),
             xycoords='axes fraction', textcoords='axes fraction',
             arrowprops=dict(arrowstyle="-|>", color='black'))

sub.annotate("Coupling-induced\ntipping", xy=(0.56, 0.65), xycoords='axes fraction', ha='right', size=7, color="black")
sub.annotate(numbering_panels[3], xy=(-0.05, 1.05), xycoords='axes fraction', ha='left', size=7, color="black", weight="bold")

fig.subplots_adjust(wspace=0.35, hspace=0.3)
sub.set_position([0.285, 0.02, 0.45, 0.4])  # [left, bottom, width, height]
plt.savefig(here / "Fig1.pdf", bbox_inches='tight')
plt.show()

# %%
