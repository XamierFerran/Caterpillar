import paho.mqtt.client as mqtt
from secrets import BrokerIP
import asyncio

def code():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("interrupted")


async def main():
    brain = mqtt.Client("Brain")
    brain.connect(BrokerIP)
    eyesQueue = asyncio.Queue()
    controlLoop = asyncio.create_task(control(eyesQueue, brain))
    updateLoop = asyncio.create_task(updates(eyesQueue, brain))
    await asyncio.gather(controlLoop, updateLoop)


async def control(eyesQueue: asyncio.Queue, brain):
    global pathClear
    pathClear = True

    # Updates state variables based on message recieved over mqtt from eyes
    async def eyesUpdate(queue):
        global pathClear
        msg = await queue.get()
        print(msg)
        if msg == "wall":
            pathClear = False
        elif msg == "clear":
            pathClear = True
    
    walkSequence = walkAlgorithm()
    stance = 0

    while True:
        await asyncio.sleep(0.1)
        if not eyesQueue.empty():
            await eyesUpdate(eyesQueue)
        
        if pathClear:
            brain.publish(walkSequence[stance][0],walkSequence[stance][1])
            await asyncio.sleep(walkSequence[stance][2])
            stance = (stance + 1)%len(walkSequence)

        
# Listens for updates from eyes over mqtt
async def updates(eyesQueue: asyncio.Queue, brain):

    # Future is what allows us to return values from a callback in an asynchronous environment
    future = asyncio.Future()
    def on_message(who,user,msg):
            print(msg.topic+" "+msg.payload.decode())
            if msg.topic == "eyes":
                future.set_result(msg.payload.decode())

    brain.subscribe("eyes")
    brain.on_message = on_message
    brain.loop_start()

    # Loop reads in mqtt data as it comes in, and puts it in a queue to be used in control coroutine
    while True:
        message = await future
        future = asyncio.Future()
        await eyesQueue.put(message)

# Returns an array of tuples which contain each step in the algorithm to walk forward.
# First value in the tuple is the topic to publish to (leg being commanded), second is the issued command,
# Third is the time before sending the next command in seconds
def walkAlgorithm():
    walkSequence = []
    walkSequence.append(("backLeft","swing",3))
    walkSequence.append(("frontLeft","swing",3))

    walkSequence.append(("backLeft","moveUnder",0))
    walkSequence.append(("backRight","moveBack",0))
    walkSequence.append(("frontLeft","moveUnder",0))
    walkSequence.append(("frontRight","moveBack",3))

    walkSequence.append(("backRight","swing",3))
    walkSequence.append(("frontRight","swing",3))

    walkSequence.append(("backLeft","moveBack",0))
    walkSequence.append(("backRight","moveUnder",0))
    walkSequence.append(("frontLeft","moveBack",0))
    walkSequence.append(("frontRight","moveUnder",3))

    return walkSequence

code()