from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pyDOE import * #function name >>> lhs
from cmcrameri import cm

# SET SEEDS FOR REPRODUCIBILITY
SEED = 60
np.random.seed(SEED)

# Plot style configuration
plt.style.use('seaborn-v0_8-white')
plt.rcParams['figure.figsize'] = (88/25.4, 45/25.4)
plt.rcParams['font.family'] = 'sans-serif'

plt.rcParams.update({
    # Font settings
    'font.size': 5,
    'xtick.labelsize': 5,
    'ytick.labelsize': 5,
    'axes.titlesize': 5,
    'axes.labelsize': 5,
    'legend.fontsize': 5,
    
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
# colors
ec = 4
element_colors = [cm.batlow(i) for i in np.linspace(0, 1, ec)]


#Tipping limits, see Global Tipping Point Report 2025: # Armstrong McKay et a. 2022
limits_gis  = [0.8, 3.4]  #0.8-3.0 (central: 1.5)     
limits_thc  = [1.1, 3.9]  #1.4-8.0 (central: 4.0)     
limits_wais = [1.0, 3.0]  #1.0-3.0 (central: 1.5)      
limits_amaz = [1.5, 6.0]  #2.0-6.0 (central: 3.5)      
limits_nino = [3.0, 6.0]  #

#Time scale of tipping for the tipping elements (taken from the literature review of DA. McKay)
tau_gis  = [1000, 15000]         #1000-15000(central: 10.000)      old values: [1000, 15000] 
tau_thc  = [15, 300]             #15-120 (central: 50)             old values: [15, 300]     
tau_wais = [500, 13000]          #500-13000 (central: 2000)        old values: [1000, 13000] 
tau_nino = [25, 200]             #unclear (around 100)             old values: [25, 200]     
tau_amaz = [50, 200]             #50-200 (central: 100)            old values: [50, 200]     


"""
Latin hypercube sampling with seed for reproducibility
Note: These points need a rescaling according to the uncertainty ranges
This can be done by: x_new = lower_lim + (upper_lim - lower_lim) * u[0;1), where u[0;1) = Latin-HC
"""
points = np.array(lhs(10, samples=10))  # This will now be reproducible due to np.random.seed()

#rescaling function from latin hypercube
def latin_function(limits, rand):
    resc_rand = limits[0] + (limits[1] - limits[0]) * rand
    return resc_rand


#MAIN
array_limits = []
sh_file = []
for t in range(20):
    ecs = t*50
    print(t)
    for i in range(0, len(points)):
        #print(i)
        
        unique_id = i + 1  # Simple ID from 1-25

        #TIPPING RANGES
        rand_gis = latin_function(limits_gis, points[i][0])
        rand_thc = latin_function(limits_thc, points[i][1])
        rand_wais = latin_function(limits_wais, points[i][2])
        rand_amaz = latin_function(limits_amaz, points[i][3])
        rand_nino = latin_function(limits_nino, points[i][4])
        
        rand_tau_gis = latin_function(tau_gis, points[i][5])
        rand_tau_thc = latin_function(tau_thc, points[i][6])
        rand_tau_wais = latin_function(tau_wais, points[i][7])
        rand_tau_amaz = latin_function(tau_amaz, points[i][8])
        rand_tau_nino = latin_function(tau_nino, points[i][9])

        array_limits.append([rand_gis, rand_thc, rand_wais, rand_amaz, rand_nino,
                            rand_tau_gis, rand_tau_thc, rand_tau_wais, rand_tau_nino, rand_tau_amaz])

        sh_file.append(["python3 MAIN_no_enso.py {} {} {} {} {} 0.2 1.0 1.0 0.2 0.3 0.5 0.15 1.0 0.2 0.15 1.0 0.4 {} {} {} {} {} {} {}".format(
                                rand_gis, rand_thc, rand_wais, rand_amaz, rand_nino,
                                rand_tau_gis, rand_tau_thc, rand_tau_wais, rand_tau_nino, rand_tau_amaz,
                                ecs,
                                unique_id)]) 

# Save the seed used for this run
with open("run_parameters.txt", "w") as f:
    f.write(f"SEED used for this run: {SEED}\n")
    f.write(f"Number of parameter sets: {len(array_limits)}\n")
    f.write(f"LHS dimensions: 10\n")
    f.write(f"LHS samples: 25\n")

array_limits = np.array(array_limits)
#np.savetxt("latin_prob.txt", array_limits, delimiter=" ")

#Create .sh file to run on the cluster
sh_file = np.array(sh_file)
np.savetxt("latin_sh_file.txt", sh_file, delimiter=" ", fmt="%s")

print("Saved latin_sh_file.txt")

# Rest of your plotting code remains the same...
#tipping ranges and plots
gis = array_limits.T[0]
thc = array_limits.T[1]
wais = array_limits.T[2]
amaz = array_limits.T[3]
nino = array_limits.T[4]

plt.hist(gis, 25, facecolor= element_colors[2], alpha=0.8, label="GIS")
plt.hist(thc, 25, facecolor= element_colors[0], alpha=0.8, label="AMOC")
plt.hist(wais, 25, facecolor=element_colors[3], alpha=0.8, label="WAIS")
plt.hist(amaz, 25, facecolor=element_colors[1], alpha=0.8, label="AMAZ")
legend = plt.legend(loc='best', frameon=True)
legend.get_frame().set_facecolor('white')
legend.get_frame().set_edgecolor('white')   # optional
legend.get_frame().set_alpha(1)
plt.xlabel("Tipping Temperature [°C]")
#plt.ylabel("N")
plt.tight_layout()
plt.savefig("latin_prob_TR.png")
plt.savefig("latin_prob_TR.pdf")
plt.show()
plt.clf()
plt.close()

#feedbacks
rand_tau_gis = array_limits.T[5]
rand_tau_thc = array_limits.T[6]
rand_tau_wais = array_limits.T[7]
rand_tau_nino = array_limits.T[8]
rand_tau_amaz = array_limits.T[9]

plt.hist(rand_tau_gis,  100, facecolor= element_colors[2], alpha=0.8, label="GIS")
plt.hist(rand_tau_thc,  100, facecolor= element_colors[0],ec = element_colors[1], alpha=0.8, label="AMOC")
plt.hist(rand_tau_wais, 100, facecolor= element_colors[3], alpha=0.8, label="WAIS")
plt.hist(rand_tau_amaz, 100, color=element_colors[1],ec = element_colors[1], alpha=0.8, label="AMAZ")
legend = plt.legend(loc='best', frameon=True)
legend.get_frame().set_facecolor('white')
legend.get_frame().set_edgecolor('white')   # optional
legend.get_frame().set_alpha(.8)
plt.xlabel("Tipping time (Years)")
#plt.ylabel("N")
plt.tight_layout()
plt.savefig("latin_prob_tau.png")
plt.savefig("latin_prob_tau.pdf")
plt.show()
plt.clf()
plt.close()


print("Finish")
