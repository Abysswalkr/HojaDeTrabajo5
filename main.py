import random

import rango as rango
import simpy
import numpy

texto = "---Course simulation---"
ancho = 100
texto_cent = texto.center(ancho)
print(texto_cent)

Interval = 10
RamCapacity = 100
ProcessMemory = 10
CpuSpeed = 3
NumProcesses = 50 #[25, 50, 100, 150, 200]
AmountProcess = 10
StartTime = 0
Time = []

def process(Env, Operation, Ram, CPU,  ID, Memory, Instructions, StTime, Processor):
    global StartTime

    yield Env.timeout(StTime)
    Begginingtime = Env.now

    print(
        f"{ID}, in queue, Status:NEW. Time: {Env.now:.1f}. Amount of RAM required: {Ram}. Amount of RAM available: {Memory.level}"
    )
    yield Memory.get(Ram)
    print(
        f"{ID}, in queue, Status:READY. Time: {Env.now:.1f}. Amount of instructions in queue: {Instructions}"
    )

    while Instructions > 0:
        with Processor.request() as request:
            yield request
            Instructions -= CPU
            yield Env.timeout(Operation)
            print(
                f" {ID} process in queue Status:READY on time {Env.now:.1f}. Amount of instructions in queue: {Instructions}"
            )

        if Instructions > 0 and random.randint(1, 2) == 1:
            print(
                f" {ID}, has entered to the queue Status:WAITING "
            )
            yield Env.timeout(random.randint(1, 5))

    yield Memory.put(Ram)
    Time.append(Begginingtime)
    print(
        f" {ID}, process Status:TERMINATED on time {Env.now:.1f}. Amount of RAM returned: {Ram}. Amount of MEMORY available: {Memory.level}"
    )

Env = simpy.Environment()
Memory = simpy.Container(Env, RamCapacity, RamCapacity)
Processor = simpy.Resource(Env, AmountProcess)

for c in range(NumProcesses):
    TimeStarted = random.expovariate(
        1.0 / Interval)
    Instructions = random.randint(1, 10)
    RAM = random.randint(1, 10)
    Env.process(
        process(Env=Env, Ram=RAM, Instructions=Instructions,
                ID=f"Process {c}", CPU=CpuSpeed, Operation=AmountProcess,
                Memory=Memory, Processor=Processor, StTime=StartTime)
    )

Env.run()
promed = numpy.mean(Time)
Desviation = numpy.std(Time)
print(
    f" The El tiempo promedio de finalización de los procesos es de {promed} segundos con una desviacion estandar de {Desviation}\n"
)