
# Add modules directory to path
import os
import sys
import re

sys.path.append('')

# global imports
import numpy as np
import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=1.)
import itertools
import time
import glob

# private imports from sys.path
from core.evolve import evolve

from scipy.integrate import solve_ivp

#private imports for earth system
from earth_sys.timing_no_enso import timing
from earth_sys.functions_earth_system_no_enso import global_functions
from earth_sys.earth_no_enso import earth_system

#measure time
#start = time.time()
#############################GLOBAL SWITCHES#########################################
time_scale = True            # time scale of tipping is incorporated
plus_minus_include = True    # from Kriegler, 2009: Unclear links; if False all unclear links are set to off state and only network "0-0" is computed
######################################################################
duration = 50000 #actual real simulation years; OR EVEN 100000 years
ScenarioT = ["05",1,15,2,3,4,5]
ScenarioC = [309, 344, 382, 424, 523, 646, 798]


#Names to create the respective directories
long_save_name = "results"


#######################GLOBAL VARIABLES##############################
#drive coupling strength
coupling_strength = np.linspace(0.0, 1.0, 11, endpoint=True)
#temperature input (forced with generated overshoot inputs)
GMT_files = np.sort(glob.glob("temp_input/*.txt"))

########################Declaration of variables from passed values#######################
#Must sort out first and second value since this is the actual file and the number of nodes used
sys_var = np.array(sys.argv[1:], dtype=str) #low sample -3, intermediate sample: -2, high sample: -1

#####################################################################

GMT_files = GMT_files[int(sys_var[-2]):int(sys_var[-2])+50]

latin_ID = sys_var[-1]
####################################################################

#Tipping ranges from distribution
limits_gis, limits_thc, limits_wais, limits_amaz, limits_nino = float(sys_var[0]), float(sys_var[1]), float(sys_var[2]), float(sys_var[3]), float(sys_var[4])

#Probability fractions = in wie vielen Fällen kommt Cascade, also dass das eine das andere zum kippen bringt
# TO GIS
pf_wais_to_gis, pf_thc_to_gis = float(sys_var[5]), float(sys_var[6])
# TO THC
pf_gis_to_thc, pf_nino_to_thc, pf_wais_to_thc = float(sys_var[7]), float(sys_var[8]), float(sys_var[9])
# TO WAIS
pf_nino_to_wais, pf_thc_to_wais, pf_gis_to_wais = float(sys_var[10]), float(sys_var[11]), float(sys_var[12])
# TO NINO
pf_thc_to_nino, pf_amaz_to_nino = float(sys_var[13]), float(sys_var[14])
# TO AMAZ
pf_nino_to_amaz, pf_thc_to_amaz = float(sys_var[15]), float(sys_var[16])

#tipping time scales
tau_gis, tau_thc, tau_wais, tau_nino, tau_amaz = float(sys_var[17]), float(sys_var[18]), float(sys_var[19]), float(sys_var[20]), float(sys_var[21])


#Time scale
"""
All tipping times are computed in comparison to the Amazon rainforest tipping time. As this is variable now, this affects the results to a (very) level
"""
if time_scale == True:
    print("compute calibration timescale")
    #function call for absolute timing and time conversion
    time_props = timing(tau_gis, tau_thc, tau_wais, tau_amaz, tau_nino)
    gis_time, thc_time, wais_time, nino_time, amaz_time = time_props.timescales()
    conv_fac_gis = time_props.conversion()
else:
    #no time scales included
    gis_time = thc_time = wais_time = nino_time = amaz_time = 1.0
    conv_fac_gis = 1.0

#include uncertain "+-" links:
if plus_minus_include == True:
    plus_minus_links = np.array(list(itertools.product([-1.0, 0.0, 1.0], repeat=3)))

    #in the NO_ENSO case (i.e., the second link must be 0.0)
    plus_minus_data = []
    for pm in plus_minus_links:
        if pm[1] == 0.0:
            plus_minus_data.append(pm)
    plus_minus_links = np.array(plus_minus_data)

else:
    plus_minus_links = [np.array([1., 1., 1.])]

import time as timeModule

################################# MAIN #################################
#Create Earth System
earth_system = earth_system(gis_time, thc_time, wais_time, nino_time, amaz_time,
                            limits_gis, limits_thc, limits_wais, limits_nino, limits_amaz,
                            pf_wais_to_gis, pf_thc_to_gis, pf_gis_to_thc, pf_nino_to_thc,
                            pf_wais_to_thc, pf_gis_to_wais, pf_thc_to_wais, pf_nino_to_wais,
                            pf_thc_to_nino, pf_amaz_to_nino, pf_nino_to_amaz, pf_thc_to_amaz)

################################# MAIN LOOP #################################
for kk in plus_minus_links:
    print("Wais to Thc:{}".format(kk[0]))
    print("Amaz to Nino:{}".format(kk[1]))
    print("Thc to Amaz:{}".format(kk[2]))
    try:
        os.stat("{}".format(long_save_name))
    except:
        os.makedirs("{}".format(long_save_name), exist_ok = True)

    try:
        os.stat("{}/network_{}_{}_{}".format(long_save_name,  kk[0], kk[1], kk[2]))
    except:
        os.makedirs("{}//network_{}_{}_{}".format(long_save_name, kk[0], kk[1], kk[2]), exist_ok = True)

    for GMT_file in GMT_files:
        print(GMT_file)
        parts = re.split("ECS|.txt", GMT_file)
        ECS = float(parts[1])
        
        
        GMT_series = np.loadtxt(GMT_file) # read temperature -> 1D array
        for col in range(GMT_series.shape[1]):
            GMT = GMT_series[:,col]
            out_gmt = []
            print("ECS: {}°C".format(ECS))
            print("Scenario:", ScenarioT[col], "°C")
            print("Final CO2 concentration:", ScenarioC[col], "ppm")

                
            for strength in coupling_strength:
                print("Coupling strength: {}".format(strength), flush=True)
                currentTime=timeModule.process_time()

                output = []

                temp_func = lambda t: GMT[int(t)] if t < len(GMT) else GMT[-1]

                t_eval= np.linspace(0, duration, int(duration)+1)

                net = earth_system.dynamic_earth_network(temp_func, strength, kk[0], kk[2])

                atol= 1e-3
                rtol= 1e-3
                sol=solve_ivp(lambda t,x: net.f(x,t), [0,duration], [-1,-1,-1,-1], t_eval=t_eval, method='LSODA', atol=atol, rtol=rtol)
                sol = np.array(sol.y)
                for t in range(0, int(duration)):
                    output.append([ECS, 
                                   ScenarioC[col],
                                   strength,
                                   latin_ID,
                                   net.get_number_tipped(sol[:,t]),
                                   [net.get_tip_states(sol[:,t])[0]].count(True),
                                   [net.get_tip_states(sol[:,t])[1]].count(True),
                                   [net.get_tip_states(sol[:,t])[2]].count(True),
                                   [net.get_tip_states(sol[:,t])[3]].count(True)
                                   ])
                    
                endTime=timeModule.process_time()
                print(endTime-currentTime, flush=True)
                    
                
                if len(output) != 0:
                    #saving structure
                    data = np.array(output)
                    out_gmt.append(data[-1])

            #necessary for break condition
            if len(out_gmt) != 0:
                #saving structure
                output_data = np.array(out_gmt)
                np.savetxt("{}/network_{}_{}_{}/ECS{}_ID{}_Scenario{}_strngth{}.txt".format(long_save_name, 
                    kk[0], kk[1], kk[2], ECS, latin_ID,ScenarioC[col], strength), output_data, fmt = '%s')

print("Finish")

