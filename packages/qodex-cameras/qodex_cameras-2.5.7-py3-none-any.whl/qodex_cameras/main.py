import threading

from qodex_cameras import mixins
from qodex_recognition import main as recognition
from qodex_cameras.other.pyhik_mode import HikCamera as HikAPI
from qodex_cameras.video_saver import RTSPVideoWriterObject


class HikCamera(mixins.Camera, mixins.ABC, mixins.HttpMakePic,
                mixins.CameraDB):
    def __init__(self, ip, port, login, password,
                 pics_folder=None, rtsp_port=554, test_mode=False,
                 auth_method="Digest", save_pics=False, photo_type_name=None):
        self.ip = ip
        self.port = port
        self.rtsp_port = rtsp_port
        self.cam_login = login
        self.cam_pass = password
        self.pics_folder = pics_folder
        self.test_mode = test_mode
        self.auth_method = auth_method
        self.save_pics = save_pics
        self.api = HikAPI(host=ip, port=port, usr=login, pwd=password)
        self.get_photo_url = f"{self.schema}{self.cam_login}-{self.cam_pass}@" \
                             f"{self.ip}:{self.port}" \
                             f"/ISAPI/Streaming/channels/101/" \
                             f"picture?snapShotImageType=JPEG"
        self.photo_type_name = photo_type_name
        self.output = None
        self.start_record_thumb = None
        self.stop_record_thumb = None

    def get_photo_rest(self):
        return self.get_http_photo()

    def start_record(self, rtsp_stream_link=None, output="output.avi"):
        self.output = output
        pic_res = self.make_pic()
        self.start_record_thumb = pic_res
        rtsp_stream_link = f"rtsp://{self.cam_login}:{self.cam_pass}@{self.ip}:{self.rtsp_port}/Streaming/Channels/101"
        super(HikCamera, self).start_record(
            rtsp_stream_link=rtsp_stream_link, output=output)

    def stop_record(self):
        threading.Thread(target=self.make_stop_record_thumb).start()
        super(HikCamera, self).stop_record()
        return self.output

    def make_stop_record_thumb(self):
        pic_res = self.make_pic()
        self.start_record_thumb = pic_res


class HikCameraCarNumberRecognition(HikCamera,
                                    recognition.MailNumberRecognitionRus):
    def __init__(self, ip, port, login, password, mail_token,
                 pics_folder=None, rtsp_port=554, test_mode=False,
                 auth_method="Digest", save_pics=False, photo_type_name=None):
        super().__init__(ip, port, login, password,
                         pics_folder=pics_folder, rtsp_port=rtsp_port,
                         test_mode=test_mode,
                         auth_method=auth_method,
                         save_pics=save_pics, photo_type_name=photo_type_name)
        self.set_token(mail_token)

    def make_pic(self, name: str = None):
        res = super().make_pic(name=name)
        if not res:
            return {"error": "no data from camera",
                    "photo_data": res["photo_data"]}
        if 'error' in res:
            return {"error": "no data from camera",
                    "photo_data": res["photo_data"]}
        recognition_result = self.get_result(res['photo_data'])
        if not recognition_result:
            res["error"] = "no recognition result"
            return res
        if "error" in recognition_result:
            res["error"] = recognition_result
            return res
        res["car_number"] = recognition_result
        return res
