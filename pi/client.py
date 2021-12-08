import cv2
import numpy as np
import socket
import sys
import pickle
import struct ### new code
from time import sleep
cap=cv2.VideoCapture(-1)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.10.229',5000))
video = cv2.VideoWriter('captured_video.avi', cv2.VideoWriter_fourcc(*'X264'),
                        2, (640, 480))
while True:
    ret,frame=cap.read()
    video.write(frame)
    data = pickle.dumps(frame) ### new code
    clientsocket.sendall(struct.pack("L", len(data))+data) ### new code