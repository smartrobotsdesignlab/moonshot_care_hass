#!/usr/bin/python3
import asyncio
import websocket, json
import http.server
import socketserver
import threading
from requests import get, post
from time import sleep
import signal
import rel

my_id=1
only_once = False

# Configuration variables
ACCESS_TOKEN = ""          # Input access token here
HASS_ENTITY_ID = ""        # Input entity_id here
HASS_ADDRESS = "127.0.0.1" # Input ip address or domain name of Home-assistant instance

def trigger_function():
    # Add your code here
    print("Function called!")

def on_message(ws, message):
    global my_id
    global only_once
    my_id += 1
    print("mm", message)
    data = json.loads(message)
    if data['type'] == 'auth_required':
        response = json.dumps({'type': 'auth', 'access_token': ACCESS_TOKEN})
        ws.send(response)
    elif data['type'] == 'auth_ok':
        #auth successful
        print("auth_ok")
        response = json.dumps({
            'id': my_id,
            'type': 'subscribe_trigger',
            'trigger': {
                'platform': 'state',
                'entity_id': HASS_ENTITY_ID,
            }
        })
        #print(response)
        ws.send(response)
    elif data['type'] == 'result':
        pass
        #subscribe to other triggers if needed :) 
    elif data['type'] == 'event':
        if data['event']['variables']['trigger']['entity_id'] == HASS_ENTITY_ID:
            service_caller.call_sample_service()
            trigger_function()


def on_close(ws):
    print("Closed")

def main(args=None):
    ws = websocket.WebSocketApp("ws://" + HASS_ADDRESS + ":8123/api/websocket", on_message=on_message, on_close=on_close)
    target=ws.run_forever(dispatcher=rel, reconnect=5)
    rel.signal(2, rel.abort)
    rel.dispatch()

if __name__ == '__main__':
    main()
