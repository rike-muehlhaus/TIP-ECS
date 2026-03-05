import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import sys
from pathlib import Path
import matplotlib.patches as patches


# Plot style configuration
plt.style.use('seaborn-v0_8-white')
plt.rcParams['figure.figsize'] = (185/25.4, 170/25.4)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

plt.rcParams.update({
    # Font settings
    'font.size': 5,
    'xtick.labelsize': 5,
    'ytick.labelsize': 5,
    'axes.titlesize': 5,
    'axes.labelsize': 5,
    'legend.fontsize': 7,
    
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

from load_data import download_from_zenodo, download_and_extract

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

# Load Temperature Data
zip_folder = Path("data/Temperature")  
if not zip_folder.exists():
    download_and_extract(
        zipname="Temperature.zip"
    )
else:
    print(f"{zip_folder} exists already, skipping download.")

T15 = np.load("data/Temperature/T15.npy")
T1 = np.load("data/Temperature/T1.npy")
T3 = np.load("data/Temperature/T3.npy")
T05 = np.load("data/Temperature/T05.npy")
T5 = np.load("data/Temperature/T5.npy")
T4 = np.load("data/Temperature/T4.npy")
T2 = np.load("data/Temperature/T2.npy")

ppms = [309, 344, 382, 424, 523, 646, 798]

# C O L O R S : Crameri, F. (2018). Scientific colour maps. Zenodo. https://doi.org/10.5281/zenodo.1243862
from cmcrameri import cm
n_colors = 7
scenario_colors = [cm.roma_r(i) for i in np.linspace(0, 1, n_colors)]

# Calculate temperature range from arrays used in flows
temps_used_in_flows = [T5, T4, T3, T2, T15, T1, T05]
temp_min = min(np.min(temp_array[-1,:]) for temp_array in temps_used_in_flows)
temp_max = max(np.max(temp_array[-1,:]) for temp_array in temps_used_in_flows)

scenarios = [
    {
        "name": "798",
        "co2": {"min": 424, "max": 1000, "mean": 798},
        "temp": {"min": np.min(T5[-1,688]), "max": np.max(T5[-1,401]), "mean": np.median(T5[-1,:]), "ten": T5[-1,37], "ninety": T5[-1,135]},
        "risk": {"min": 99, "max": 100, "mean": 100, "ten": 100, "ninety": 100},
        "color": "indigo"
    },
    {
        "name": "646",
        "co2": {"min": 424, "max": 800, "mean": 646},
        "temp": {"min": np.min(T4[-1,688]), "max": np.max(T4[-1,401]), "mean": np.median(T4[-1,:]), "ten": T4[-1,37], "ninety": T4[-1,135]},
        #"risk": {"min": 100, "max": 100, "mean": 99, "ten": 100, "ninety": 100},
        "risk": {"min": 91, "max": 100, "mean": 100, "ten": 99, "ninety": 100},
        "color": "mediumvioletred"
    },
    {
        "name": "532",
        "co2": {"min": 424, "max": 800, "mean": 532},
        "temp": {"min": np.min(T3[-1,688]), "max": np.max(T3[-1,401]), "mean": np.median(T3[-1,:]), "ten": T3[-1,37], "ninety": T3[-1,135]},
        "risk": {"min": 75, "max": 100, "mean": 100, "ten": 90,"ninety": 100},
        "color": "red"
    },
    {
        "name": "424",
        "co2": {"min": 424, "max": 800, "mean": 424},
        "temp": {"min": np.min(T2[-1,688]), "max": np.max(T2[-1,401]), "mean": np.median(T2[-1,:]), "ten": T2[-1,37], "ninety": T2[-1,135]},
        "risk": {"min": 27, "max": 100, "mean": 90, "ten": 47, "ninety": 98},
        "color": "tab:orange"
    },
    {
        "name": "382",
        "co2": {"min": 382, "max": 382, "mean": 382},
        "temp": {"min": np.min(T15[-1,688]), "max": np.max(T15[-1,401]), "mean": np.median(T15[-1,:]), "ten": T15[-1,37], "ninety": T15[-1,135]},
        "risk": {"min": 2, "max": 98, "mean": 58, "ten": 25, "ninety": 90},
        "color": "green"
    },
    {
        "name": "344",
        "co2": {"min": 278, "max": 344, "mean": 344},
        "temp": {"min": np.min(T1[-1,688]), "max": np.max(T1[-1,401]), "mean": np.median(T1[-1,:]), "ten": T1[-1,37], "ninety": T1[-1,135]},
        "risk": {"min": 0, "max": 83, "mean": 19, "ten": 0,"ninety": 42},
        "color": "mediumaquamarine"
    },
    {
        "name": "309",
        "co2": {"min": 309, "max": 309, "mean": 309},
        "temp": {"min": np.min(T05[-1,688]), "max": np.max(T05[-1,401]), "mean": np.median(T05[-1,:]), "ten": T05[-1,37], "ninety": T05[-1,135]},
        "risk": {"min": 0, "max": 4, "mean": 0, "one": 0,"ten": 0, "ninety": 0},
        "color": "gold"
    }
]

# Calculate global ranges for consistent scaling
co2_values = []
for s in scenarios:
    co2_values.extend([s["co2"]["min"], s["co2"]["max"], s["co2"]["mean"]])
co2_global_min = min(co2_values)
co2_global_max = max(co2_values)

axis_ranges = [
    {"min": co2_global_min, "max": co2_global_max, "unit": "ppm"},
    #{"min": 0.1, "max": temp_max, "unit": "°C"},
    {"min": 0, "max": 10, "unit": "°C"},
    {"min": 0, "max": 100, "unit": "%"}
]

def normalize_value(value, data_min, data_max, target_min=1, target_max=10):
    """Normalize a single value to target range"""
    return target_min + (value - data_min) / (data_max - data_min) * (target_max - target_min)

def create_triangle_plot(scenario, axis_ranges, ax, colorinput="blue"):
    """Create the triangle flow plot"""
    x_positions = [0, 10, 20]
    axis_labels = ["CO$_2$ level (ppm)", "$\Delta$GMST (°C)", "Tipping risk (%)"]
    
    # Extract data for this scenario
    co2_data = scenario["co2"]
    temp_data = scenario["temp"]
    risk_data = scenario["risk"]
    
    color = colorinput
    
    # Normalize using global ranges
    y1_min = normalize_value(co2_data["min"], axis_ranges[0]["min"], axis_ranges[0]["max"])
    y1_max = normalize_value(co2_data["max"], axis_ranges[0]["min"], axis_ranges[0]["max"])
    y1_mean = normalize_value(co2_data["mean"], axis_ranges[0]["min"], axis_ranges[0]["max"])
    
    y2_min = normalize_value(temp_data["min"], axis_ranges[1]["min"], axis_ranges[1]["max"])
    y2_max = normalize_value(temp_data["max"], axis_ranges[1]["min"], axis_ranges[1]["max"])
    y2_mean = normalize_value(temp_data["mean"], axis_ranges[1]["min"], axis_ranges[1]["max"])
    y2_ninety = normalize_value(temp_data["ninety"], axis_ranges[1]["min"], axis_ranges[1]["max"])
    y2_ten = normalize_value(temp_data["ten"], axis_ranges[1]["min"], axis_ranges[1]["max"])
    
    y3_min = normalize_value(risk_data["min"], axis_ranges[2]["min"], axis_ranges[2]["max"])
    y3_max = normalize_value(risk_data["max"], axis_ranges[2]["min"], axis_ranges[2]["max"])
    y3_mean = normalize_value(risk_data["mean"], axis_ranges[2]["min"], axis_ranges[2]["max"])
    y3_ninety = normalize_value(risk_data["ninety"], axis_ranges[2]["min"], axis_ranges[2]["max"])
    y3_ten = normalize_value(risk_data["ten"], axis_ranges[2]["min"], axis_ranges[2]["max"])

    # Create fan polygon (CO2 to Temperature)
    fan_vertices = [(x_positions[0], y1_mean), (x_positions[1], y2_min), (x_positions[1], y2_max)]
    fan = patches.Polygon(fan_vertices, closed=True, color=color, alpha=0.4, lw=0)
    ax.add_patch(fan)
    
    # Create trapezoid polygon (Temperature to Risk)
    trap_vertices = [(x_positions[1], y2_min), (x_positions[1], y2_max), 
                     (x_positions[2], y3_max), (x_positions[2], y3_min)]
    trap = patches.Polygon(trap_vertices, closed=True, color=color, alpha=0.4, lw=0)
    ax.add_patch(trap)
    
    # 10% line
    x3s = [x_positions[0], x_positions[1], x_positions[2]]
    y3s = [y1_mean, y2_ten, y3_ten]
    ax.plot(x3s, y3s, color=color, linestyle=":", lw=0.8)
    #ax.text(x3s[-1] + 0.5, y3s[-1] - 0.755, f"{risk_data['ten']:.0f}%", va='center', ha='left')
    if scenario["name"] == "532": ax.text(x3s[-1] + 0.5, y3s[-1]-0.4, f"{risk_data['ten']:.0f}%", va='center', ha='left')
    elif scenario["name"] == "646": ax.text(x3s[-1] + 0.5, y3s[-1]-0.8, f"{risk_data['ten']:.0f}%", va='center', ha='left')
    elif scenario["name"] == "798": ax.text(x3s[-1] + 0.5, y3s[-1]-0.8, f"{risk_data['ten']:.0f}%", va='center', ha='left')
    else: ax.text(x3s[-1] + 0.5, y3s[-1], f"{risk_data['ten']:.0f}%", va='center', ha='left')
    ax.plot([x3s[-1], x3s[-1] + 0.2], [y3s[-1], y3s[-1]], 'k-', linewidth=0.5)

    # Mean line
    xs = [x_positions[0], x_positions[1], x_positions[2]]
    ys = [y1_mean, y2_mean, y3_mean]
    ax.plot(xs, ys, color=color, lw=0.8)
    #ax.text(xs[-1] + 0.5, ys[-1]+0.08, f"{risk_data['mean']:.0f}%", va='center', ha='left')
    if scenario["name"] == "309": ax.text(xs[-1] + 0.5, ys[-1]+0.72, f"{risk_data['mean']:.0f}%", va='center', ha='left')
    elif scenario["name"] == "532": ax.text(xs[-1] + 0.5, ys[-1]-0.5, f"{risk_data['mean']:.0f}%", va='center', ha='left')
    else: ax.text(xs[-1] + 0.5, ys[-1], f"{risk_data['mean']:.0f}%", va='center', ha='left')
    ax.plot([xs[-1], xs[-1] + 0.2], [ys[-1], ys[-1]], 'k-', linewidth=0.5)
    
    # 90% line
    x2s = [x_positions[0], x_positions[1], x_positions[2]]
    y2s = [y1_mean, y2_ninety, y3_ninety]
    ax.plot(x2s, y2s, color=color, linestyle="--", lw=0.8)
    #ax.text(x2s[-1] + 0.5, y2s[-1] + 0.95, f"{risk_data['ninety']:.0f}%", va='center', ha='left')
    if scenario["name"] == "309": ax.text(x2s[-1] + 0.5, y2s[-1]+1.29, f"{risk_data['ninety']:.0f}%", va='center', ha='left')
    elif scenario["name"] == "424": ax.text(x2s[-1] + 0.5, y2s[-1]+0.2, f"{risk_data['ninety']:.0f}%", va='center', ha='left')
    elif scenario["name"] == "532": ax.text(x2s[-1] + 0.5, y2s[-1]+0.2, f"{risk_data['ninety']:.0f}%", va='center', ha='left')    
    elif scenario["name"] == "646": ax.text(x2s[-1] + 0.5, y2s[-1]+0.8, f"{risk_data['ninety']:.0f}%", va='center', ha='left')
    elif scenario["name"] == "798": ax.text(x2s[-1] + 0.5, y2s[-1]+0.8, f"{risk_data['ninety']:.0f}%", va='center', ha='left')
    else: ax.text(x2s[-1] + 0.5, y2s[-1], f"{risk_data['ninety']:.0f}%", va='center', ha='left')
    ax.plot([x3s[-1], x2s[-1] + 0.2], [y2s[-1], y2s[-1]], 'k-', linewidth=0.5)

    # Add axis ticks
    def add_axis_ticks(x_pos, axis_range, custom_ticks=None):
        if custom_ticks is not None:
            tick_values = custom_ticks
            original_min = axis_range["min"]
            original_max = axis_range["max"]
            
            valid_ticks = []
            tick_positions = []
            for val in tick_values:
                if original_min <= val <= original_max:
                    norm_pos = 1 + (val - original_min) / (original_max - original_min) * (10 - 1)
                    tick_positions.append(norm_pos)
                    valid_ticks.append(val)
            
            tick_values = valid_ticks
        else:
            tick_positions = np.linspace(1, 10, 5)
            original_min = axis_range["min"]
            original_max = axis_range["max"]
            tick_values = np.linspace(original_min, original_max, 5)
        
        for tick_pos, tick_val in zip(tick_positions, tick_values):
            #ax.plot([x_pos - 0.2, x_pos + 0.2], [tick_pos, tick_pos], 'k-', linewidth=0)
            ax.plot([x_pos - 0.2, x_pos], [tick_pos, tick_pos], 'k-', linewidth=0.5)
            
            if axis_range["unit"] == "°C":
                label = f"{tick_val:.0f}"
            elif axis_range["unit"] == "ppm":
                label = f"{int(tick_val)}"
            else:
                label = f"{int(tick_val)}"
            
            ax.text(x_pos - 0.4, tick_pos, label, ha='right', va='center')
    
    # Draw axes with ticks
    for i, (x_pos, label) in enumerate(zip(x_positions, axis_labels)):
        ax.axvline(x=x_pos, color='black')#, alpha=0.8)
        ax.text(x_pos, -0.8, label, ha='center', va='top', 
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="white"))
        
        if i == 0:
            custom_co2_ticks = [300, 400, 500, 600, 700, 800, 900, 1000]
            add_axis_ticks(x_pos, axis_ranges[i], custom_co2_ticks)
        elif i == 1:
            custom_temp_ticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            add_axis_ticks(x_pos, axis_ranges[i], custom_temp_ticks)
        else:
            add_axis_ticks(x_pos, axis_ranges[i])
    
    # Layout
    ax.set_xlim(-3, 22)
    ax.set_ylim(0, 12)
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['bottom'].set_color('white')
    
    ax.set_xticks([])
    ax.set_yticks([])


def create_donut_plot(scenario, ax, colorinput="blue"):
    """Create the donut plot for risk range"""
    risk_data = scenario["risk"]
    temp_data = scenario["temp"]
    
    # Normalize risk values to 0-1 range
    riskmaxmin = np.array([[risk_data["min"]/100, risk_data["max"]/100]])
    tempmaxmin = np.array([[temp_data["min"]/10, temp_data["max"]/10]])     # normalize to 10°C
     
    colors_donut = ["grey", colorinput, "grey"]
    
    # Three segments: [0 to min], [min to max], [max to 1]
    vals = np.array([riskmaxmin[0][0], riskmaxmin[0][1] - riskmaxmin[0][0], 1 - riskmaxmin[0][1]])
    valst = np.array([tempmaxmin[0][0], tempmaxmin[0][1] - tempmaxmin[0][0], 1 - tempmaxmin[0][1]])
    
    #  Create pie chart starting at top (90 degrees)
    wedges, texts = ax.pie(vals,
                           radius=1,
                           colors=["grey", colorinput, "lightgray"],
                           wedgeprops=dict(width=0.5, edgecolor="w"),
                           startangle=90,
                           counterclock = False,
                           normalize=True)
    min_angle = 90 - (riskmaxmin[0][0] * 360)  # Start of orange segment
    max_angle = 90 - (riskmaxmin[0][1] * 360)  # End of orange segment
    plt.setp(wedges, width=0.4, edgecolor='white')
    
    # Outer ring annotations
    # Position for min value - on extension line, shifted right
    min_radius = 1.14
    min_x = min_radius * np.cos(np.radians(min_angle))
    min_y = min_radius * np.sin(np.radians(min_angle))
    if scenario["name"] == "309": ax.text(min_x - 0.5, min_y, f"{riskmaxmin[0][0]:.0%}", va='center', ha='left')
    elif scenario["name"] == "646": ax.text(min_x - 0.9, min_y-0.2, f"{riskmaxmin[0][0]:.0%}", va='center', ha='left')
    elif scenario["name"] == "798": ax.text(min_x - 1.3, min_y-0.3, f"{riskmaxmin[0][0]:.0%}", va='center', ha='left')
    else: ax.text(min_x, min_y, f"{riskmaxmin[0][0]:.0%}", 
           ha='left' if min_x > 0 else 'right', 
           va='center')

    # Position for max value - on extension line, shifted left
    max_radius = 1.2
    max_x = max_radius * np.cos(np.radians(max_angle))
    max_y = max_radius * np.sin(np.radians(max_angle))
    ax.text(max_x, max_y, f"{riskmaxmin[0][1]:.0%}", 
           ha='right' if max_x < 0 else 'left', 
           va='center')
    ax.set(aspect="equal")

    # inner ring
    wedges, texts = ax.pie(valst,
                           radius=1-0.4,
                           colors=["grey", "tab:red", "lightgrey"],
                           wedgeprops=dict(width=0.5, edgecolor="w"),
                           startangle=90,
                           counterclock = False,
                           normalize=True)
    plt.setp(wedges, width=0.4, edgecolor='white')
    






# Define custom legend entries
legend_lines = [
    Line2D([0], [0], color='black', linestyle='--', label='90. Percentile'),
    Line2D([0], [0], color='black', linestyle='-', label='Median'),
    Line2D([0], [0], color='black', linestyle=':', label='10. Percentile')
]

import string
letters = string.ascii_lowercase
scenario_names = ["309 ppm", "344 ppm", "382 ppm", "424 ppm", "532 ppm", "646 ppm", "798 ppm"]

fig = plt.figure()

for i, scenario in enumerate(scenarios):
    ax_triangle = fig.add_subplot(4, 2, i+1)
    create_triangle_plot(scenarios[(i+1)*-1], axis_ranges, ax_triangle, colorinput=scenario_colors[i])
    ax_triangle.text(0.02, 1.15, letters[i], transform=ax_triangle.transAxes, fontsize=7, fontweight='bold', va='top', ha='right')
    if i==0: 
        # line legend
        legend = ax_triangle.legend(frameon=True, handles=legend_lines, title="ECS", loc='lower right', bbox_to_anchor=(0.82, 0.6), prop={'size': 5})
        legend.get_frame().set_linewidth(0.5)

    ax_donut = ax_triangle.inset_axes([0.03, 0.6, 0.45, 0.45])
    create_donut_plot(scenarios[(i+1)*-1], ax_donut, colorinput=scenario_colors[i])
    ax_donut.annotate(scenario_names[i], xy=(0.15, 1.2), xycoords='axes fraction', ha='left', size=5, color="black", weight="bold")

    if i==0: 
        ax_label = ax_triangle.inset_axes([0, 0, 1, 1])
        ax_label.set_xlim(0,10)
        ax_label.set_ylim(0,10)

        ax_label.spines['left'].set_visible(False)
        ax_label.spines['top'].set_visible(False)
        ax_label.spines['bottom'].set_visible(False)
        ax_label.spines['right'].set_visible(False)
        ax_label.set_xticks([])
        ax_label.set_yticks([])
        ax_label.patch.set_alpha(0)
        ax_label.plot([2.1,2.45],[6,7.65], color="black", lw=0.5)
        ax_label.plot([3,2.8],[5.2,7], color="black", lw=0.5)
        ax_label.annotate("$\Delta$GMST\nrange", xy=(0.21, 0.45), xycoords='axes fraction', ha='center', size=5, color="black")
        ax_label.annotate("Tipping\nrisk", xy=(0.3, 0.39), xycoords='axes fraction', ha='center', size=5, color="black")

fig.subplots_adjust(wspace=0.15, hspace=0.5)

plt.savefig("Fig4.pdf", bbox_inches='tight')
