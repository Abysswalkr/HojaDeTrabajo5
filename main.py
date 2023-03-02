##############################
# Author: Jose L. Gramajo    #
# ID: 22907                  #
# Date: 1 - 03 - 2023        #
# ############################

import random
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
NumProcesses = 25  # [25, 50, 100, 150, 200]
AmountProcess = 10
StartTime = 0
Time = []

# This function simulates a process that requires a certain amount of RAM and CPU time to execute.
def process(Env: object, Operation: object, Ram: object, CPU: object, ID: object, Memory: object, Instructions: object,
            StTime: object, Processor: object) -> object:
    """

    :param Env: The simulation environment.
    :param Operation: The amount of CPU time required for each instruction.
    :param Ram: The amount of RAM required by the process.
    :param CPU: The CPU speed.
    :param ID: The process ID.
    :param Memory: The memory container.
    :param Instructions: The number of instructions that the process requires to execute.
    :param StTime: The starting time of the process.
    :param Processor: The resource that represents the CPU.
    """
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
# As long as the number of requests is greater than zero, the following will be executed
    while Instructions > 0:
        with Processor.request() as request:
            yield request
            Instructions -= CPU
            yield Env.timeout(Operation)
            print(
                f" {ID} process in queue Status:READY on time {Env.now:.1f}. Amount of instructions in queue: {Instructions}"
            )

# Moves pending processes to a waiting queue
        if Instructions > 0 and random.randint(1, 2) == 1:
            print(
                f" {ID}, has entered to the queue Status:WAITING "
            )
            yield Env.timeout(random.randint(1, 5))

# Information on the process that was performed, returns the time taken and the amount of memory
    yield Memory.put(Ram)
    Time.append(Begginingtime)
    print(
        f" {ID}, process Status:TERMINATED on time {Env.now:.1f}. Amount of RAM returned: {Ram}. Amount of MEMORY available: {Memory.level}"
    )

# Reports the amount of memory available for the operation
Env = simpy.Environment()
Memory = simpy.Container(Env, RamCapacity, RamCapacity)
Processor = simpy.Resource(Env, AmountProcess)

# Random request generator and informs on the arrival time of another process
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

# Displays the average time of operations
Env.run()
promed = numpy.mean(Time)
Deviation = numpy.std(Time)
print(
    f" The average time for all processes is: {promed} seconds and the standard deviation is: {Deviation}\n"
)
