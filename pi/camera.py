from time import sleep
import cv2
from datetime import datetime
import argparse

#parse arguments
parser = argparse.ArgumentParser(description='Take photos with the Raspberry Pi camera module.')
parser.add_argument('-i', '--iso', type=int, default=-1, help='ISO value to use for photos')
parser.add_argument('-s', '--sleep', type=int, default=5, help='Time in seconds to sleep between photos')
parser.add_argument('-wd', '--width', type=int, default=1280, help='Width of image')
parser.add_argument('-ht', '--height', type=int, default=720, help='Height of image')

parser.add_argument('-e', '--exposure', type=int, default=-5, help='Exposure value to use for photos. Lower is faster shutter speed')
parser.add_argument('-g', '--gain', type=int, default=0, help='Gain value to use for photos. Lower is brighter')
parser.add_argument('-b', '--brightness', type=int, default=50, help='Brightness of the image.')
parser.add_argument('-c', '--contrast', type=int, default=10, help='Contrast of the image.')
parser.add_argument('-wb', '--whitebalance', type=int, default=1, help='Auto Whitebalance. 0 is off 1 is on.')
args = parser.parse_args()

def take_photo(camera):
    return_value, image = camera.read()
    filename = '{timestamp:%H_%M_%S}.jpg'.format(timestamp=datetime.now())
    cv2.imwrite(filename,image)
    print(f'Captured {filename}')

#Function that changes the iso and shutter speed for VideoCapture using opencv
def change_settings(camera, width=1280, height=720, iso=200, exposure=-5, gain=0, brightness=0, contrast=32, whitebalance=1):
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    # 100 and 200 are reasonable values for daytime, while 400 and 800 are better for low light
    camera.set(cv2.CAP_PROP_ISO_SPEED, iso)
    # Wait for the automatic gain control to settle
    sleep(2)
    # Now fix the values
    camera.set(cv2.CAP_PROP_EXPOSURE,exposure)
    camera.set(cv2.CAP_PROP_BRIGHTNESS,brightness)
    camera.set(cv2.CAP_PROP_CONTRAST,contrast)
    camera.set(cv2.CAP_PROP_AUTO_WB, whitebalance)
    camera.set(cv2.CAP_PROP_GAIN, gain)
    return camera

if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    camera = change_settings(camera, args.width, args.height, args.iso, args.exposure,args.gain, args.brightness, args.contrast, args.whitebalance)
    take_photo(camera)
    camera.release()