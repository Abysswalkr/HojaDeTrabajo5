import random
import simpy
import numpy

texto = "---Course simulation---"
ancho = 100
texto_cent = texto.center(ancho)
print(texto_cent)

Interval = 10
RamCapacity = 100
PROCESS_MEMORY = 10
CpuSpeed = 3
NumProcesses = [25, 50, 100, 150, 200]
AmountProcess = 10
StartTime = 0
Time = []