# TODO: code structure is here but need to rework asyncio stuff for multi-server

import asyncio
import websockets
import json
import os
import re
from gtts import gTTS
from playsound import playsound

tts_lock = asyncio.Lock()
def team_name_tts(team_name):
    # team_name_text = " ".join(re.split(r'(\d+)', team_name))
    team_name_text = " ".join(team_name)
    # team_name_text = team_name
    # speech = gTTS(text = team_name_text)
    file_name = f"team_name.mp3"
    # speech.save(file_name)
    playsound("airport.wav")
    # playsound(file_name)
    # os.remove(file_name)
    # try:
    #     speech.save(file_name)
    #     playsound("airport.wav")
    #     playsound(file_name)
    #     os.remove(file_name)
    # except:
    #     print(f"Issue handling audio for {team_name}: {file_name}")

now_serving_uri_map = {}

async def websocket_handler(uri):
    async with websockets.connect(uri) as websocket:
        now_serving_uri_map[uri] = 0
        while True:
            message = await websocket.recv()
            print(f"Received message from {uri}: {message}")
            data = json.loads(message)
            now_serving = data["nowServing"]
            length = len(now_serving)
            
            if length > now_serving_uri_map[uri]:
                # new team is now serving
                now_serving_team = now_serving[length - 1]["number"]
                print(f"Now Serving Team: {now_serving_team}")
                async with tts_lock:
                    team_name_tts(now_serving_team)
                # team_name_tts(now_serving_team)
            
            now_serving_uri_map[uri] = length

async def main():
    base_uri = "ws://10.0.0.142"
    ports = ["3000", "4000"]

    uris = map(lambda port: f"{base_uri}:{port}/queue", ports)

    tasks = map(lambda uri: asyncio.create_task(websocket_handler(uri)), uris)
    await asyncio.gather(*tasks)    # * is spread operation

if __name__ == "__main__":
    asyncio.run(main())