'''
MAKING THE CLIMATE SENSITIVITY REVIEW PLOT

Strcuture:
    Most Important to include ECS:
        IPCC (1.5 - 7.7) 7.7 is based on process understanding = the upper limit of the very likely range. Based on Table 7.13.
            or based on combined assessment(2-5)
        CMIP6
        Sherwood: 2.0–5.7 K
        Myhre
    Most Important ESS:
        Hansen 2008
        Previdi 2013 (Includes Lunt and Hansen)
    Optional: 
        ECS: 
            Cox 2018 (Temp. Variability)
            Ricard 2024 (Network Based)
        ESCS:
            Lunt 2010
            Wong 2021
 How to include: 
     Could do the whole range and either the mean
     /most likely valze or smth like 66% range = likely range
     It mostly depends on which values I get.
     CMIP6: ranges + 1 value
     IPCC: ranges + 1
     Myhre: think only 1 and no upper bound ??
     
     Hansen: 1 value anyway
     Previdi: nur 1 range anyway.. -> soo let's do a likely range
     
Code: kann ich das in listen definieren. So ub, lb, lm, um?
        
'''
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# Plot style configuration
plt.style.use('seaborn-v0_8-white')
plt.rcParams['figure.figsize'] = (180/25.4, 100/25.4)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

plt.rcParams.update({
    # Font settings
    'font.size':   7,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'axes.titlesize': 7,
    'axes.labelsize': 7,
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

##################################################

fig, ax = plt.subplots()


sens_labels = ('Arrhenius (1896)',
               'Callendar (1938)',
               'Charney et al. (1979)',

               'Hansen et al. (2008)',
               'Previdi et al. (2013)',

               'CMIP5',

               'CMIP6',

               'Sherwood et al. (2020)',

               'IPCC AR6',
               
               'Wong et al. (2021)',

               'Brown et al. (2025)',

               'Myhre et al. (2025)',

               'Cooper et al. (2026)'
               
               )
y_pos = np.arange(len(sens_labels))

# lower bound values
low_bounds = [5.4, 1.9, 1.5,
    5.9, 4.0, 
    2,
    1.8, 2.0, 2.0, 2.6, 
    1.24, 2.9, 2.1]
# upper bound values
upper_bounds = [5.6, 2.1, 4.5,
    6.1, 6.0, 
    4.5,
    5.6, 5.7, 5.0, 4.7, 
    2.89, 5.6, 4.0]
w = np.array(upper_bounds) - np.array(low_bounds)

likely_IPCC = 3


colors = ['royalblue','royalblue','royalblue','darkblue', 'darkblue',
          'royalblue', 'royalblue', 'royalblue','royalblue','darkblue',
           'royalblue','royalblue', 'royalblue'] 
legend_elements = [
    Patch(facecolor='darkblue', label='ESS'),
    Patch(facecolor='royalblue', label='ECS'),
    Line2D([0], [0], color='black', linestyle='--', label='Central Value (IPCC)')
]


ax.barh(y_pos, width = w,left = low_bounds, tick_label = sens_labels, color = colors)
#ax.set_yticks(y_pos, labels=sens_labels)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Climate Sensitivity (°C)')
ax.set_xlim(0,6.5)
ax.axvline(likely_IPCC, color='black', linestyle='--', label='Central Value (IPCC)')
ax.legend(handles=legend_elements, loc='upper left')
plt.tight_layout()
plt.savefig('cs_overview.pdf')


