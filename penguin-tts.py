# Only use with single tournament server

import websocket
import _thread
import time
import rel
import json
from gtts import gTTS
from playsound import playsound
import pyttsx3

prev_len = 0
engine = pyttsx3.init()
engine.setProperty('rate', engine.getProperty('rate')-70)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def teamNameToSpeech(teamName):
    teamNameLetterByLetter = ' '.join(teamName)
    speech = gTTS(text = teamNameLetterByLetter)
    speech.save('team_name.mp3')
    playsound('team_name.mp3')

def pytts(teamName, engine = engine):
    teamNameLetterByLetter = ' '.join(teamName)
    # engine.say("Please report to skills: ")
    engine.say(teamNameLetterByLetter)
    engine.runAndWait()

def on_message(ws, message):
    global prev_len

    print(message)
    data = json.loads(message)
    now_serving = data["nowServing"]
    length = len(now_serving)
    print(prev_len)

    if length > prev_len:
        # new team is now serving
        now_serving_team = now_serving[length - 1]["number"]
        print(f"Now Serving Team: {now_serving_team}")
        playsound("airport.wav")
        pytts(now_serving_team)
    
    prev_len = length
    

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://10.0.0.142:4000/queue",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()

# # Sample JSON data
# json_data = '{"nowServing": [{"number": "886V"}, {"number": "2748A"}, {"number": "22862A"}] }'
# # Convert JSON to dictionary
# my_dict = json.loads(json_data)

# # Access elements in the dictionary
# nowServing = my_dict['nowServing']
# teamName = nowServing.pop()['number']
# print(teamName)
# teamNameToSpeech(teamName)