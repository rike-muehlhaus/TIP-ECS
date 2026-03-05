"""
FAIR Ramp Up-Stabilization Scenario

Here we will use the simple climate model/emulator FAIR (Finite Amplitude Impulse Response) model, running with a wide range of Equilibrium Climate Sensitivity (ECS) for 7 different ramp up scenarios, in order to gain global temperature time series.

Steps:
    Generate TCR-ECS Pairs
    Create Scenarios (finding Concentrations)
    Runing Model
    
"""

# import libraries
import fair
import numpy as np
# to run fair
from fair.forward import fair_scm
# to import tcrecs
from scipy import stats
from fair.tools.ensemble import tcrecs_generate
# form some stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

"""
1. Generate TCR-ECS Pairs
Identify median and index of median closest ECS
"""

# generate 1000 TCR and ECS pairs, using a normal distribution informed by CMIP5 models
ne = 1000 # number of ecs ensemble members
tcrecs = tcrecs_generate('cmip5', n=ne, dist='norm', correlated=True, seed=12)

# find median ecs (and its index), which will be used to find the stabilization vlaues of the scenarios
median = np.median(tcrecs[:,1])
median_index = np.abs(tcrecs[:,1] - median).argmin()
# check median closest ecs
print(tcrecs[median_index,1])

"""
2. Find ppm for Temperature Scenarios

We will now use this median in a "Ramp Up" scenario 
in FAIR. Ramp up means that we will increase CO2 concentrations 
continously for 200 years. Then we set the concentration 
to a constant value = Stabilization. 
We will try this for several CO2 concentrations to find,
 which ppm value corresponds to 0.5, 1.0, 1.5, 2, 3, 4, and 5°C global warming.

"""
start_ppm = 278 # preindustrial value 
test_ppm = 797 # here we insert different values and run the code below, to find the corresponding final Temperature
slope = (test_ppm - start_ppm) / 200

nt = 2000 # number of time steps (in years) = 200 years ramp up and 1800 years stabilization
years = np.arange(1850, 1850+nt) # to know which time we are referring to, we fill an array with numbers of years
conc = np.full_like(years, test_ppm, dtype=float)
conc[0] = 278
j = 0
for i in range(1850,2050):
    conc[years == i] = start_ppm+j*slope
    j = j+1

# running fair model
_, _, T = fair_scm(emissions_driven = False,
                        C = conc,
                        tcrecs = tcrecs[334,:],
                        useMultigas = False
                       )
# Final/Stabilization Temperature
print(T[nt-1])
"""
run the snippet above and insert some values in 'test_ppm'
to find the ppms corresponding to the wished temperatures
I found: ppms = [309, 344, 382, 424, 523, 646, 798]
"""

"""
3. Run Fair model von co2 scenarios
"""
ppms = [309, 344, 382, 424, 523, 646, 798]
start_ppm = 278
nt = 50000 # number of time steps (in years) 
years = np.arange(1850, 1850+nt)

conc_list = []
# creating co2 time series 
for i_p, p in enumerate(ppms):
    conc = np.full_like(years, p, dtype=float)
    conc[0] = 278
    j = 0
    slope = (p - start_ppm) / 200
    for i in range(1850,2050):
        conc[years == i] = start_ppm+j*slope
        j = j+1
    conc_list.append(conc)
# fun fair over all concentration scenarios and ecs
# save temperature files per scenario, containing all ecs
for ci,c in enumerate(conc_list):
    # initiate Temperature Array
    T = np.zeros((nt,len(tcrecs)))
    # model for for every ensemble
    for i in range(len(tcrecs)):
        _, _, T[:,i] = fair_scm(emissions_driven = False,
                                C = conc_list[ci],
                                tcrecs = tcrecs[i,:],
                                useMultigas = False
                               )
    np.savetxt(f"C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/T_{ci}.txt",T, delimiter = ",")    
"""
Done :)
"""
