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

def process(Env, Operation, Ram, Inst,  ID, Memory, Instructions, StTime, Processor):
    global StartTime

    yield Env.timeout*(StTime)
    Begginingtime = Env.now

    print(
        f"{ID}, in queue, Status:NEW. Time: {Env.now:.1f}. Amount of RAM required: {Ram}. Amount of RAM available: {Memory.level}"
    )
    yield Memory.get(Ram)
    print(
        f"{ID}, in queue, Status:READY. Time: {Env.now:.1f}. Amount of instructions in queue: {Instructions}"
    )
