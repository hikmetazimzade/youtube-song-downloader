import subprocess
import os


class Mp3_Class:
    def __init__(self, download_path):
        self.download_path = download_path

        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)


    def download_video(self, video_url):
        ffmpeg_path = r'C:\Users\your_username\Downloads\ffmpeg-master-latest-win64-gpl-shared\ffmpeg-master-latest-win64-gpl-shared\bin'
        command = [
            'youtube-dl',
            '--extract-audio',
            '--audio-format', 'mp3',
            '--ffmpeg-location', ffmpeg_path, #Write it based on where you installed it
            '-o', os.path.join(self.download_path, '%(title)s.%(ext)s'),
            video_url
        ]


        try:
            subprocess.run(command)

        except:
            print('An Error Occurred while downloading!')
