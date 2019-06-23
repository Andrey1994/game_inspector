import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

import video_player
import fps_plot
import options
import screenshot

class GameInspector(Screen):

    def __init__(self):
        super(GameInspector, self).__init__(name='GameInspector')
        self.main_layout = BoxLayout(orientation='vertical')
        self.first_row = BoxLayout(orientation='horizontal')
        self.second_row = BoxLayout(orientation='horizontal')
        self.main_layout.add_widget(self.first_row)
        self.main_layout.add_widget(self.second_row)

        self.fps_plot = fps_plot.get_fps_plot()
        self.video = video_player.get_video_player()
        self.screenshot = screenshot.get_screenshot()
        self.config = options.get_config(self.fps_plot, self.video, self.screenshot)

        self.first_row.add_widget(self.config)
        self.first_row.add_widget(self.fps_plot)
        self.second_row.add_widget(self.video)
        self.second_row.add_widget(self.screenshot)

        self.add_widget(self.main_layout)
