from secrets import BrokerIP
import asyncio
import asyncio_mqtt as aiomqtt
import paho.mqtt.client as mqtt
import time

def code():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # This is the only way I could figure out how to send a command to the controllers
        # on a keyboard interrupt. I coudn't figure out how to successfully catch an
        # interrupt from within a coroutine or the control loop, so we have to open another connection
        # with the mqtt boker once the control loop closes.
        cleanUp()



async def main():
    async with aiomqtt.Client(BrokerIP, client_id="Brain") as brain:
        startFunc = asyncio.create_task(waitForStart(brain))
        start = await startFunc
        start = True
        if start:
            eyesQueue = asyncio.Queue()
            controlLoop = asyncio.create_task(control(eyesQueue, brain))
            updateLoop = asyncio.create_task(updates(eyesQueue, brain))
            await asyncio.gather(controlLoop, updateLoop)
        else:
            raise Exception("Something went wrong")
        


# Waits for all legs to be connected
async def waitForStart(brain):
    frStatus = False
    brStatus = False
    flStatus = False
    blStatus = False
    async with brain.messages() as messages:
        await brain.subscribe("updates")

        while True:
            async for message in messages:
                
                print(message.payload.decode())
                if message.payload.decode() == "frontRight: Connected":
                    frStatus = True
                if message.payload.decode() == "frontLeft: Connected":
                    flStatus = True
                if message.payload.decode() == "backRight: Connected":
                    brStatus = True
                if message.payload.decode() == "backLeft: Connected":
                    blStatus = True
                if frStatus and brStatus and flStatus and blStatus:
                    return True
            

# main control loop which talks to the legs
async def control(eyesQueue: asyncio.Queue, brain):
    global pathClear
    pathClear = True

    # Updates state variables based on message recieved over mqtt from eyes
    async def eyesUpdate(queue):
        global pathClear
        msg = await queue.get()
        print(msg)
        if msg == "1":
            pathClear = False
        elif msg == "0":
            pathClear = True
    
    # put legs to expected starting positions
    await brain.publish("backLeft", payload="moveToStart swing")
    await brain.publish("frontLeft", payload="moveToStart swing")
    await brain.publish("backRight", payload="moveToStart moveBack")
    await brain.publish("frontRight", payload="moveToStart moveBack")
    await asyncio.sleep(3)

    # get order legs should walk in to move forward and check for updates from eyes
    walkSequence = walkAlgorithm()
    stance = 0
    while True:
        if not eyesQueue.empty():
            await eyesUpdate(eyesQueue)
        if pathClear:
            await brain.publish(walkSequence[stance][0], payload=walkSequence[stance][1])
            await asyncio.sleep(walkSequence[stance][2])
            stance = (stance + 1)%len(walkSequence)
        else:
            await asyncio.sleep(0.1)
    

        
# Listens for updates from eyes over mqtt
async def updates(eyesQueue: asyncio.Queue, brain):
    async with brain.messages() as messages:
        await brain.subscribe("eyes")

        while True:
            async for message in messages:
                if message.topic.matches("eyes"):
                    print(message.payload)
                    await eyesQueue.put(message.payload.decode())

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

def cleanUp():
    client = mqtt.Client("Brain")
    client.connect(BrokerIP)
    print("shutting down")
    client.publish("backLeft", payload="turnOff")
    client.publish("backRight", payload="turnOff")
    client.publish("frontLeft", payload="turnOff")
    client.publish("frontRight", payload="turnOff")
    time.sleep(3)



code()

