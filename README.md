# TIP-ECS

The project investigates the relationship between climate sensitivity and the risk of exceeding climate tipping points. It further assesses how observational constraints on equilibrium climate sensitivity (ECS) affect the probability of exceeding climate tipping points. All code is written in Python. This repository accompanies the paper: 

_"Observationally constrained climate sensitivity implies high climate tipping risk"_ 

_Rike Mühlhaus, Norman J. Steinert, Johan Rockström, Nico Wunderling_

Manuscript submitted.

Code version used for the paper submission: v1.0

All code is written in Python.

All data used in the analysis are available via the Zenodo project:
https://doi.org/10.5281/zenodo.18850220

## Workflow

The analysis consists of four main steps:

1. Generate temperature projections using FaIR (Smith et al. 2018).
2. Sample tipping system parameters using Latin Hypercube Sampling.
3. Simulate tipping cascades using PyCascades (Wunderling et al. 2021).
4. Post-process model outputs to calculate tipping risks.

## Requirements

Python ≥ 3.10

further: see requirements.txt

# Repository Structure

## 1. FaIR

`fair-get-temperatures.py` - Uses the FaIR simple climate model to:

- generate an ensemble of ECS values  
- construct CO₂ scenarios  
- compute global mean temperature time series

Outputs:

- temperature time series  
- ECS ensemble  

Files available in Zenodo:

- `Temperature.zip`
- `tcrecs.txt`

---

## 2. Latin Hypercube Sampling

`latin_probability_distribution.py` - Generates sampled input parameters for PyCascades using Latin Hypercube Sampling.  
Parameters include tipping thresholds and tipping timescales based on values from the Global Tipping Points Report (2025).

`latin_sh_file.txt` - Shell commands used to run PyCascades simulations with different parameter combinations.

---

## Preprocessing

`ECS-T Files in right format.py` - Formats and compresses ECS temperature time series into the format required by PyCascades.

Output:

`ecs-timeseries.zip` (available on Zenodo)

---

## 3. PyCascades

`MAIN-No_enso.py` - Main script used to run PyCascades simulations.

`PyCas_plot.py` - Used later to create a figure of one examplary tipping element state progression time series

Supporting modules:

`core/`

`earth_sys/` 

Running Pycascades requires:

`ecs-timeseries.zip` - Puts the contained files into a folder called `temp_input`

`latin_sh_file.txt`

---

## 4. Analysis

`pycas_out.py` - Collects PyCascades outputs and computes tipping risks.

Output:

`risks_data.npy` - Available in the Zenodo archive.

`load_data.py` - Necessary to load automatically the data from the Zenodo Project

`results-analyse.py` - Prints the Numbers named in the Results.

`introduction_plot.py` - Creates Fig. 1, b, c, d, and e. Needs PyCas_plot.py in the PyCascades folder.

`main-ECS-TR-plot.py` - Creates Fig. 2

`ECS-PPM_main-plot.py` - Creates Fig. 3

`Fig4.py` - Creates Fig. 4

`S_case_specific.py` - Creates Supplementary figures Fig.S3 and Fig.S4. 

`CS_review_plot.py` - Creates Supplementary figure Fig.S1. 

`SM-hist.py` - Creates Supplementary figure Fig.S2. 

---

# References

Smith, C. J., et al. (2018). FAIR v1.3: a simple emissions-based impulse response and carbon cycle model. Geoscientific Model Development, 11.

Wunderling, N., et al. (2021). Modelling nonlinear dynamics of interacting tipping elements on complex networks: the PyCascades package. The European Physical Journal Special Topics, 230(14).

