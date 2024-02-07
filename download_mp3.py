import subprocess
import os

#Import it in main.py
class Mp3_Class:
    def __init__(self, download_path):
        self.download_path = download_path

        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)


    def download_video(self, video_url):
        command = [
            'youtube-dl',
            '--extract-audio',
            '--audio-format', 'mp3',
            '--ffmpeg-location', r'C:\Users\your_username\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin',
            '-o', os.path.join(self.download_path, '%(title)s.%(ext)s'),
            video_url
        ]

        try:
            subprocess.run(command, shell=True)


        except:
            print('An Error Occurred while downloading!')