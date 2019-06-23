from kivy.uix.image import AsyncImage

def get_screenshot():
    return AsyncImage(source='no_screenshot.png', allow_stretch=False, nocache=True)
