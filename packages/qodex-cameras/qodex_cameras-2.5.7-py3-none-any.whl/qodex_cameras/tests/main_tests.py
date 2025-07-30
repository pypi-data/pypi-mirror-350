import os
import threading
import time

from qodex_cameras import main
import unittest


class TestCase(unittest.TestCase):
    @unittest.SkipTest
    def test_hik_make_real_pic(self):
        inst = main.HikCamera(
            ip="192.168.60.107",
            port=80,
            login="admin",
            password="Assa+123",
            pics_folder="",
            auth_method="Digest")
        inst.make_pic("123")

    @unittest.SkipTest
    def test_hik_make_test_pic(self):
        inst = main.HikCamera(
            ip="192.168.60.107",
            port=80,
            login="admin",
            password="Assa+123",
            pics_folder="",
            auth_method="Digest",
        test_mode=True)
        inst.make_pic("123")

    def test_car_number_recognition(self):
        inst = main.HikCameraCarNumberRecognition(
            ip="127.0.0.1",
            port=80,
            login="admin",
            password="Assa+123",
            pics_folder="",
            auth_method="Digest",
            mail_token=os.environ.get("mail_token"),
            save_pics=True
        )
        res = inst.make_pic("1234")
        #threading.Thread(target=inst.start_record).start()
        #time.sleep(15)
        #print("Waiting 15")
        #inst.stop_record()
        #print(res)


if __name__ == '__main__':
    unittest.main()
