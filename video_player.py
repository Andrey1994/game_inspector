from kivy.uix.videoplayer import VideoPlayer


def get_video_player():
    return VideoPlayer(options={'allow_stretch': True})
