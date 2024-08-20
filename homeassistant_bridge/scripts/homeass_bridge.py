#!/usr/bin/python3
import rospy
from std_srvs.srv import Trigger
from std_srvs.srv import Empty
import asyncio
import websocket, json
import http.server
import socketserver
import threading
from requests import get, post
from time import sleep
import signal

my_id=1
only_once = False

class ServiceCaller():
    def __init__(self):
        self.request_water_client = rospy.ServiceProxy('reset', Empty)

    def call_request_water(self):
        #rospy.wait_for_service('Request_Water')
        try:
            request = Empty._request_class()
            response = self.request_water_client(request)
            rospy.loginfo('Request_Water service called successfully')
        except rospy.ServiceException as e:
            rospy.loginfo('Failed to call Request_Water service')
        return

def on_message(ws, message):
    global my_id
    global only_once
    my_id += 1
    print("mm", message)
    data = json.loads(message)
    if data['type'] == 'auth_required':
        response = json.dumps({'type': 'auth', 'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIwYjc3YjkxZTg1YTk0ODRlOWJiMmI1ZDYyMGZlMWM1NyIsImlhdCI6MTcyMzEwMzc3MiwiZXhwIjoyMDM4NDYzNzcyfQ.SIDN0LdshqDTSynvuP1qmJLdP9NEr9yEhP5TUyiEJ1A'})
        ws.send(response)
    elif data['type'] == 'auth_ok':
        #auth successful
        print("auth_ok")
        response = json.dumps({
            'id': my_id,
            'type': 'subscribe_trigger',
            'trigger': {
                'platform': 'state',
                'entity_id': 'input_button.start_service',
            }
        })
        #print(response)
        ws.send(response)
    elif data['type'] == 'result':
        if not only_once:
            response = json.dumps({
                'id': my_id,
                'type': 'subscribe_trigger',
                'trigger': {
                    'platform': 'state',
                    'entity_id': 'input_button.whill',
                    }
                })
            #print(response)
            ws.send(response)
        only_once = True
    elif data['type'] == 'event':
        if data['event']['variables']['trigger']['entity_id'] == 'input_button.start_service':
            rospy.loginfo("Turtlebot")
            service_caller.call_request_water()


def on_close(ws):
    print("Closed")

def main(args=None):
    
    ws = websocket.WebSocketApp("ws://faye.livinglab.lan:8123/api/websocket", on_message=on_message, on_close=on_close)
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()
    
    global service_caller
    service_caller = ServiceCaller()

    rospy.init_node('service_caller', anonymous=True)
    rate = rospy.Rate(10)
    rospy.spin()


if __name__ == '__main__':
    main()
