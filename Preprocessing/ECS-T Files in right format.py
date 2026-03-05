# -*- coding: utf-8 -*-
"""
To make PyCascades run smoothly and more computational efficient, I rearrange the Temperature data.
This code makes one data file per ECS and puts all of them in one zip-file. 
The zip file is ecs-timeseries.zip. U can find it here or in Zenodo. 
"""
import numpy as np

# adapt the path to the data
tcrecs = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/tcrecs.txt",delimiter = ",")
T05 = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/T_0.txt", delimiter = ",")
T1 = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/T_1.txt", delimiter = ",")
T15 = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/T_2.txt", delimiter = ",")
T2 = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/T_3.txt", delimiter = ",")
T3 = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/T_4.txt",delimiter = ",")
T4 = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/T_5.txt", delimiter = ",")
T5 = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/T_6.txt", delimiter = ",")

# put all loaded T series into a list
T = [T05, T1, T15, T2, T3, T4, T5]

import zipfile
import io

filenames = set()

with zipfile.ZipFile("C:/Users/LENOVO/Desktop/FAIR-PyCas/PyCascades/ecs_timeseries.zip", "w", compression=zipfile.ZIP_DEFLATED) as zipf:
    for i in range(len(tcrecs)):
        ecs_file = np.zeros((50000, 7))
        for c, S in enumerate(T):
            ecs_file[:10000, c] = S[:, i]
            ecs_file[10000:, c] = S[-1, i]

            #ecs_file[:, c] = S[:, i]
            
        name = f"ECS{np.round(tcrecs[i,1], 6)}.txt"
        if name in filenames:
            print(f"Doppelter Name gefunden: {name}")
        else:
            filenames.add(name)

        # In-Memory-Datei erzeugen
        buffer = io.StringIO()
        np.savetxt(buffer, ecs_file)
        zipf.writestr(f"ECS{np.round(tcrecs[i,1], 6)}.txt", buffer.getvalue())
        #print(f"added ECS {np.round(tcrecs[i,1], 6)} to zip")
        
print("Done! :)")