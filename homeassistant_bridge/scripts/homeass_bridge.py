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
        self.service_client = rospy.ServiceProxy('SERVICE_NAME (e.g., reset)', Empty) #Service type is important too, don't forget to change

    def call_sample_service(self):
        #Executing a service call. 
        try:
            request = Empty._request_class()
            response = self.service_client(request)
            rospy.loginfo('Sample service called successfully')
        except rospy.ServiceException as e:
            rospy.loginfo('Failed to call Sample service')
        return

def on_message(ws, message):
    global my_id
    global only_once
    my_id += 1
    print("mm", message)
    data = json.loads(message)
    if data['type'] == 'auth_required':
        response = json.dumps({'type': 'auth', 'access_token': 'ACCESS_TOKEN'})
        ws.send(response)
    elif data['type'] == 'auth_ok':
        #auth successful
        print("auth_ok")
        response = json.dumps({
            'id': my_id,
            'type': 'subscribe_trigger',
            'trigger': {
                'platform': 'state',
                'entity_id': 'HASS_ENTITY_ID (e.g., input_button.start_service)',
            }
        })
        #print(response)
        ws.send(response)
    elif data['type'] == 'result':
        pass
        #subscribe to other triggers if needed :) 
    elif data['type'] == 'event':
        if data['event']['variables']['trigger']['entity_id'] == 'HASS_ENTITY_ID (e.g.,input_button.start_service) ':
            rospy.loginfo("Calling Service")
            service_caller.call_sample_service()


def on_close(ws):
    print("Closed")

def main(args=None):
    
    ws = websocket.WebSocketApp("ws://HASS_ADDRESS:8123/api/websocket", on_message=on_message, on_close=on_close)
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
