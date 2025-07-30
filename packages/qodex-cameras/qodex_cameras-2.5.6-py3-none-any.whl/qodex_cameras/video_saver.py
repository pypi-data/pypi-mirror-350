import subprocess
import os
import time
import signal


class RTSPVideoWriterObject(object):
    def __init__(self, src=0, output_path_name="output.mp4"):
        self.record_in_progress = False
        self.rtsp_url = src
        self.output_path_name = output_path_name
        self.proc = None

    def start_record(self):
        cwd = os.getcwd()

        # Use ffmpeg's segment option to split output every 10 minutes (600 seconds)
        # The %03d format will number the files sequentially, starting from 000
        output_filepath_pattern = os.path.join(cwd, self.output_path_name)
        print(output_filepath_pattern)
        # Build the ffmpeg command
        command = [
            'ffmpeg',
            "-rtsp_transport", "tcp",
            '-i', self.rtsp_url,
            '-c:v', 'copy',
            '-c:a', 'aac',
            #'-f', 'segment',
            "-buffer_size", "10024",
            #'-segment_time', '600',  # 600 seconds = 10 minutes
            #'-reset_timestamps', '1',
            output_filepath_pattern
        ]

        # Try running the command
        try:
            print("Attempting to connect to RTSP stream...")
            self.proc = subprocess.Popen(
                command, stdout=subprocess.PIPE,
                shell=False, stdin=subprocess.DEVNULL)
            # self.proc = subprocess.run(command, check=True)
        except subprocess.CalledProcessError:
            print(
                "Failed to connect to RTSP stream or encountered an error during recording.")
        except KeyboardInterrupt:
            print("\nRecording interrupted by user.")

    def stop_record(self):
        print("Stopping video recording...")
        self.record_in_progress = False
        print(self.proc)
        if self.proc:
            os.kill(self.proc.pid, signal.SIGINT)


if __name__ == "__main__":
    d = RTSPVideoWriterObject(
        "rtsp://admin:Assa+123@192.168.60.108:554/Streaming/Channels/101")
    d.start_record()
    time.sleep(10)
    d.stop_record()
