import os
import glob
import numpy as np

# --- Path Setup ---
base_path = "/p/projects/dominoes/rikemue/ecs-pycas-latin/"
results_path = os.path.join(base_path, "results/")

tcrecs = np.loadtxt(os.path.join(base_path, "tcrecs.txt"), delimiter=",")
ecs_unique = np.unique(np.round(tcrecs[:, 1], 6))
scenarios = np.array([309, 344, 382, 424, 523, 646, 798])

networks = ["0.0_0.0_0.0", "0.0_0.0_1.0", "0.0_0.0_-1.0",
            "1.0_0.0_0.0", "1.0_0.0_1.0", "1.0_0.0_-1.0",
            "-1.0_0.0_0.0", "-1.0_0.0_1.0", "-1.0_0.0_-1.0"]

all_compiled_results = []

print("Step 1: Loading and filtering columns...", flush=True)
for network in networks:
    network_dir = os.path.join(results_path, f"network_{network}")
    files = glob.glob(os.path.join(network_dir, "*.txt"))
    
    for f in files:
        if os.path.basename(f) in ["empirical_values.txt", "all_results.npy"]:
            continue
            
        data = np.loadtxt(f)
        if data.ndim == 1: data = data.reshape(1, -1)
        
        # New indexing 
        # 0:ECS, 1:Scenario, 4:TotalTipped, 5:GIS, 6:AMOC, 7:WAIS, 8:AMAZ
        extracted = data[:, [0, 1, 4, 5, 6, 7, 8]]
        all_compiled_results.append(extracted)

# Step 2: Merge into one giant array
print("Step 2: Merging data...", flush=True)
full_data = np.concatenate(all_compiled_results, axis=0)
del all_compiled_results 

# Step 3: Calculate Risk
print("Step 3: Calculating Risk Matrix...", flush=True)
risk_list = []

for s in scenarios:
    # Filter for scenario
    data_s = full_data[full_data[:, 1].astype(int) == s]
    
    for e in ecs_unique:
        # Filter for ECS
        data_e = data_s[np.isclose(data_s[:, 0], e)]
        n_samples = len(data_e)
        
        if n_samples == 0: continue
            
        # COLUMN MAP for data_e:
        # [0:ECS, 1:Scenario, 2:TotalTipped, 3:GIS, 4:AMOC, 5:WAIS, 6:AMAZ]
        
        total_tipped = data_e[:, 2]
        
        # Vectorized Risk Calculations
        r1 = np.sum(total_tipped >= 1) / n_samples
        r2 = np.sum(total_tipped >= 2) / n_samples
        r3 = np.sum(total_tipped >= 3) / n_samples
        r4 = np.sum(total_tipped >= 4) / n_samples
        
        # Individual Element Risks (sums of columns 3 through 6)
        element_sums = np.sum(data_e[:, 3:7], axis=0) / n_samples
        
        risk_list.append([
            e, s, 
            r1, r2, r3, r4, 
            element_sums[0], element_sums[1], element_sums[2], element_sums[3]
        ])

# To make a nice scatter plot I need to shuffle the data which is now ordered by ECS a bit
indices = np.arange(len(risk_list))
np.random.shuffle(indices)
risk_array = np.array(risk_list)[indices]

# Final Save
save_path = os.path.join(base_path, "risks_data.npy")
np.save(save_path, risk_array)
print("Done! Risk data saved to:", save_path, flush=True)
