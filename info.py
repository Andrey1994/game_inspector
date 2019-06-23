import subprocess
import webbrowser

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen


usage_guide = \
'''
[size=40][b]Usage Guide:[b][/size]
[i]Run it with administrator priviligies![/i]
You are able to measure FPS, FlipRate and take screenshots for any running process,
you just need to pass PID param, which you can check using TaskManager.
Also you are able to pass 0 in PID field to take screenshots and record video of entire Desktop and measure FPS based on all events
[i]For PID mode game overlay is not supported[/i]

[size=30][b]Game Overlay (Experimental feature):[/b][/size]
To draw game overlay you need to specify full path to the executable and this system will run game for you
or you are able to set Attach Process Name option, press Start and run game process by yourself
For Steam games you also need to specify Steam App Id which you can get here: [u][ref=https://steamdb.info/search/]https://steamdb.info/search/[/ref][/u]

[size=25][b]Supported Graphical API:[/b][/size]
DX11
DX12
Vulkan

This application is based on:
[u][ref=https://github.com/Andrey1994/game_overlay_sdk]https://github.com/Andrey1994/game_overlay_sdk[/ref][/u]
[u][ref=https://github.com/Andrey1994/fps_inspector_sdk]https://github.com/Andrey1994/fps_inspector_sdk[/ref][/u]
[u][ref=https://github.com/Andrey1994/screen_recorder_sdk]https://github.com/Andrey1994/screen_recorder_sdk[/ref][/u]

Project page: [u][ref=https://github.com/Andrey1994/game_inspector]https://github.com/Andrey1994/game_inspector[/ref][/u]
'''

class Info(Screen):

    def __init__(self, screen_manager):
        super(Info, self).__init__(name='Info')
        self.screen_manager = screen_manager
        subprocess.Popen(['Taskmgr.exe'])
        self.layout = BoxLayout(orientation='vertical')

        self.docs = Label(text=usage_guide, markup=True, font_size='20sp')
        self.docs.bind(on_ref_press=self.open_link)
        self.layout.add_widget(self.docs)

        self.config_button = Button(text='Configure Session', font_size=20, size_hint=(1, .2))
        self.config_button.background_normal = ''
        self.config_button.background_color = [0.3, .4, .3, .85]
        self.config_button.bind(on_press=self.config_pressed)
        self.layout.add_widget(self.config_button)
        
        self.add_widget(self.layout)

    def open_link(self, instance, value):
        webbrowser.open(value)

    def config_pressed(self, instance):
        self.screen_manager.current = 'SessionSettings'