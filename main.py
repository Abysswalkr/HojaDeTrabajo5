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

    while Instructions > 0:
        with Processor.request() as request:
            yield request
            Instructions -= Inst
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

