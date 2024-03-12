# TEST WSS

import asyncio
import websockets
import time
import random
import json

async def generate_message():
    # json_data = '{"nowServing": [{"number": "886V"}, {"number": "2748A"}, {"number": "22862A"}] }'
    sample_team_list = [{"number": "1010X"}, {"number": "9181B"}, {"number": "88969A"}]
    now_serving_count = random.randint(0,3)
    return {"nowServing": sample_team_list[0:now_serving_count]}

async def send_message(websocket, interval):
    while True:
        message = await generate_message();
        await websocket.send(json.dumps(message))
        await asyncio.sleep(interval)

async def echo(websocket, path):
    send_task = asyncio.create_task(send_message(websocket, 8))  # Send a message every 10 seconds
    try:
        async for message in websocket:
            print("Received:", message)
            # You can handle incoming messages here if needed
    finally:
        send_task.cancel()

async def main():
    async with websockets.serve(echo, "localhost", 8766):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())