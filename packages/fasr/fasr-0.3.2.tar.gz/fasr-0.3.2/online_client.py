import websockets
import asyncio
import json
from loguru import logger


async def record_microphone():
    import pyaudio

    FORMAT = pyaudio.paInt16
    RATE = 16000
    chunk_size = 200
    CHUNK = int(RATE / 1000 * chunk_size)

    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    while True:
        data = stream.read(CHUNK)
        await websocket.send(data)
        await asyncio.sleep(0.005)


async def message():
    try:
        while True:
            meg = await websocket.recv()
            meg = json.loads(meg)
            logger.info(meg)

    except Exception as e:
        print("Exception:", e)


async def ws_client(id):
    global websocket
    uri = "ws://wpaiv2.k8s.ingress.58dns.org/hdp-lbg-huangye/dev/debug-fasr/66735copz2/ide/proxy/8867/asr/realtime"
    # uri = "ws://localhost:27000/asr/realtime?model=paraformer"
    # uri = "ws://workspace.featurize.cn:15730/asr/realtime?model=paraformer"
    print("connect to", uri)
    async with websockets.connect(uri) as websocket:
        task = asyncio.create_task(record_microphone())
        task3 = asyncio.create_task(message())
        await asyncio.gather(task, task3)
    exit(0)


if __name__ == "__main__":
    asyncio.run(ws_client(0))
