import uuid
from abc import ABC, abstractmethod
import logging
import traceback
from requests.exceptions import ConnectionError
from qodex_cameras import settings
from qodex_cameras import functions
import os
import requests
from requests.auth import HTTPDigestAuth, HTTPBasicAuth
from qodex_recognition import main as recognition
import io
from PIL import Image
from qodex_cameras.video_saver import RTSPVideoWriterObject
import threading


class PicsSaver:
    pics_folder = None
    save_pics = False

    def set_pics_folder(self, folder: str):
        self.pics_folder = folder

    def set_test_mode(self, mode: bool = True):
        self.test_mode = mode

class CameraDB:
    sql_shell = None
    photo_type_name = None


class Camera(ABC, PicsSaver):
    schema = "http://"
    ip = None
    port = None
    rtsp_port = None
    cam_login = None
    cam_pass = None
    test_mode = None
    photo_type_name = None

    def start_record(self, rtsp_stream_link, output="output.avi"):
        print(f"Start recording from {rtsp_stream_link} to {output}")
        self.inst = RTSPVideoWriterObject(rtsp_stream_link, output)
        self.inst.start_record()

    def stop_record(self):
        try:
            self.inst.stop_record()
        except AttributeError:
            return {"error": "Not video writer found"}

    @abstractmethod
    def get_photo_rest(self):
        return

    def make_pic(self, name: str = None):
        # Сделать фото с именем name. Если имя не задано - использовать счетчик
        if not name:
            name = str(uuid.uuid4())
        if self.test_mode:
            with open(settings.TEST_PHOTO, 'rb') as fobj:
                photo_data = fobj.read()
        else:
            photo_data = self.take_shot()
            if not photo_data:
                return {"error": "no photo data", "photo_data": photo_data}
        result = {'photo_data': photo_data}
        if self.save_pics:
            if not self.pics_folder:
                self.pics_folder = settings.CUR_DIR
            photo_abs_name = os.sep.join((self.pics_folder, f"{name}.jpg"))
            functions.save_photo(photo_abs_name, photo_data)
            result['abs_path'] = photo_abs_name
        return result

    def take_shot(self):
        logging.info(f"{__name__}. Taking shot....")
        try:
            return self.get_photo_rest()
        except ConnectionError:
            logging.error(
                f"Connection error: {traceback.format_exc()}")


class HttpMakePic:
    auth_method = None
    cam_login = None
    cam_pass = None
    get_photo_url = None
    get_pic_timeout = 2

    def get_http_photo(self):
        if self.auth_method == "Basic":
            response = requests.get(
                self.get_photo_url,
                auth=HTTPBasicAuth(self.cam_login, self.cam_pass),
                timeout=self.get_pic_timeout)
        elif self.auth_method == "Digest":
            response = requests.get(
                self.get_photo_url,
                auth=HTTPDigestAuth(self.cam_login, self.cam_pass),
                timeout=self.get_pic_timeout)
        else:
            return
        return response.content
