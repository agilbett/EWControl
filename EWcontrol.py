from pynput import keyboard
from datetime import datetime
import os
import threading
import socket

from apscheduler.schedulers.blocking import BlockingScheduler


def tick():
    print('{"action":"heartbeat","requestrev":0}')
    client_socket.send('{"requestrev":0,"imagehash":"fbfab9026008c82840a6b429a1876ec6155f17ec","height":"633","action":"getCurrentImage"}\n')


def on_press(key):
    try:
        if key == keyboard.Key.page_down:
            print('{"action":"nextBuild","requestrev":0}')
            client_socket.send('{"action":"nextBuild","requestrev":0}\n')
        if key == keyboard.Key.page_up:
            print('{"action":"prevBuild","requestrev":0}')
            client_socket.send('{"action":"prevBuild","requestrev":0}\n')
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def sched():
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
def clearbuf():
    while 1:
        data = client_socket.recv(32768)
#        print(data)


t = threading.Thread(target=sched,)
t.start()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.52', 1050))
#client_socket.connect(('localhost', 1050))
print('{"device_type":2,"action":"connect","uid":"6BDBD0F7-DA1E-473F-8084-D63709AA10C8","device_name":"EWControl"}')
client_socket.send('{"device_type":2,"action":"connect","uid":"06249660-262d-4cec-b9f6-f67819465ed9","device_name":"Andrews iPad"}\n')
c = threading.Thread(target=clearbuf,)
c.start()


with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()
