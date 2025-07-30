from robobopy_videostream.my_socket import MySocket
import os
import time
import cv2
from datetime import datetime


class RoboboVideo:

    def __init__(self, ip, robot_id=0):
        self.port = 40405 + (robot_id * 10)
        self.ip = ip
        self.socket = MySocket()

    def connect(self):
        self.socket.connect(self.ip,self.port)
        self.socket.start_image_thread()

    def getImage(self):
        image, cv2_image,timestamp, sync_id, frame_id = self.socket.get_image()
        return cv2_image

    def getImageWithMetadata(self):
        image, cv2_image,timestamp, sync_id, frame_id = self.socket.get_image()
        return cv2_image, timestamp, sync_id, frame_id
    
    def takePictures(self, count=1, delay=0, interval=1, save_path=None):
        if save_path is None:
            save_path = os.getcwd()

        os.makedirs(save_path, exist_ok=True)

        time.sleep(delay)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        captured_images = []

        for i in range(count):
            img = self.getImage()
            if img is not None:
                img_filename = os.path.join(save_path, f"robobopic_{timestamp}_{i+1:03d}.jpg")
                cv2.imwrite(img_filename, img)
                captured_images.append(img)
            if i < count - 1:
                time.sleep(interval)

        return captured_images

    def disconnect(self):
        self.socket.disconnect()

