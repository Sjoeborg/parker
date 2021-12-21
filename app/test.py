import requests
import json
import cv2,pickle

addr = 'http://localhost:5000'
test_url = addr + '/photo'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = cv2.imread('C:/Users/Martin/22_28_02.jpg')
img1 = pickle.dumps(img)
# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)
# send http request with image and receive response
#response = requests.post(test_url, data=img1, headers=headers)
response = requests.get(test_url, params={'id':'pCFfXANfJz8uDqFy7RS1n'}, headers=headers)
# decode response
resp = response.text.encode()
import numpy as np
img = pickle.loads(resp)
res = resp.encode()
cv2.imshow('nogga',np.fromstring(res, dtype=np.uint8).reshape(727,260))
cv2.waitKey(0)

