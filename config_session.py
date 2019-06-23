import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.filebrowser import FileBrowser
from kivy.uix.textinput import TextInput

from fps_inspector_sdk import fps_inspector
from screen_recorder_sdk import screen_recorder
import game_overlay_sdk
import game_overlay_sdk.injector

import keyboard

from alert import Alert


class SessionSettings(Screen):

    def __init__(self, screen_manager, game_inspector):
        super(SessionSettings, self).__init__(name='SessionSettings')
        self.pid_value = None
        self.game_inspector = game_inspector
        self.default_video_hotkey = 'shift+i'
        self.default_screenshot_hotkey = 'shift+o'
        self.default_fps_hotkey = 'shift+p'
        self.screen_manager = screen_manager
        self.layout = BoxLayout(orientation='horizontal')
        self.first_col = BoxLayout(orientation='vertical')
        self.second_col = BoxLayout(orientation='vertical')

        self.filebrowser = FileBrowser()
        self.filebrowser.bind(
            on_success=self.fbrowser_success,
            on_canceled=self.fbrowser_canceled)
        self.first_col.add_widget(self.filebrowser)

        self.pid =TextInput(hint_text='PID e.g.13876 (without game overlay)', size_hint=(1, 0.1))
        self.pid.bind(text=self.on_pid)
        self.second_col.add_widget(self.pid)

        self.process_path =TextInput(hint_text='Path to Game e.g. D:\\Steam\\steamapps\\common\\Shadow of the Tomb Raider Trial\\SOTTR.exe (will enable game overlay)', size_hint=(1, 0.1))
        self.process_path.bind(text=self.on_path)
        self.second_col.add_widget(self.process_path)

        self.process_name =TextInput(hint_text='Process Name to Monitor e.g. SOTTR.exe (will enable game overlay)', size_hint=(1, 0.1))
        self.process_name.bind(text=self.on_process_name)
        self.second_col.add_widget(self.process_name)

        self.steam_app_id =TextInput(size_hint=(1, 0.1),
            hint_text='Optional: Steam App Id e.g 974630\nOnly for Steam Games and in case if you run it for the first time\nIt works only with Path to Game param\nhttps://steamdb.info/search/')
        self.second_col.add_widget(self.steam_app_id)

        self.video_hotkey =TextInput(hint_text='Optional: video recording hotkey, default is %s' % self.default_video_hotkey, size_hint=(1, 0.1))
        self.second_col.add_widget(self.video_hotkey)

        self.screenshot_hotkey = TextInput(hint_text='Optional: screenshot hotkey, default is %s' % self.default_screenshot_hotkey, size_hint=(1, 0.1))
        self.second_col.add_widget(self.screenshot_hotkey)

        self.fps_hotkey = TextInput(hint_text='Optional: fps recording hotkey, default is %s' % self.default_fps_hotkey, size_hint=(1, 0.1))
        self.second_col.add_widget(self.fps_hotkey)


        self.start_button = Button(text='Run Session', font_size=20, size_hint=(1, 0.3))
        self.start_button.background_normal = ''
        self.start_button.background_color = [0.3, .4, .3, .85]
        self.start_button.bind(on_press=self.run_pressed)
        self.second_col.add_widget(self.start_button)

        self.layout.add_widget(self.first_col)
        self.layout.add_widget(self.second_col)

        self.add_widget(self.layout)


    def fbrowser_canceled(self, instance):
        self.process_path.text = ''

    def fbrowser_success(self, instance):
        self.process_path.text = str(instance.selection[0])

    def on_pid(self, instance, value):
        if value:
            self.process_path.text = ''
            self.process_name.text = ''
            self.steam_app_id.text = ''

    def on_path(self, instance, value):
        if value:
            self.pid.text = ''
            self.process_name.text = ''

    def on_process_name(self, instance, value):
        if value:
            self.pid.text = ''
            self.process_path.text = ''
            self.steam_app_id.text = ''

    def run_pressed(self, instance):
        try:
            game_overlay_sdk.injector.enable_monitor_logger()
            screen_recorder.enable_log()
            fps_inspector.enable_fliprate_log()
            ready = True
            if self.pid.text:
                self.pid_value = int(self.pid.text)
                screen_recorder.init_resources(self.pid_value)
                self.game_inspector.config.pid = self.pid_value
                self.game_inspector.config.use_overlay = False
            elif self.process_path.text:
                if self.steam_app_id.text:
                    game_overlay_sdk.injector.run_process(self.process_path.text, '', int(self.steam_app_id.text))
                else:
                    game_overlay_sdk.injector.run_process(self.process_path.text, '', None)
                self.pid_value = game_overlay_sdk.injector.get_pid()
                screen_recorder.init_resources(self.pid_value)
                self.game_inspector.config.pid = self.pid_value
                self.game_inspector.config.use_overlay = True
            elif self.process_name.text:
                game_overlay_sdk.injector.start_monitor(self.process_name.text)
                # wait for process creation
                Alert(title='Waiting for process with name %s' % self.process_name.text, text = 'now you need to start target process manually', condition = self.check_pid)
            else:
                Alert(title='Invalid input', text = 'nor PID nor Process Name nor Process Path were specified')
                ready = False
            if ready:
                self.register_callbacks()
                self.screen_manager.current = 'GameInspector'
        except Exception as e:
            Alert(title='Excpetion occured', text = str(e))
            raise e

    def register_callbacks(self):
        if self.video_hotkey.text:
            video_hotkey = self.video_hotkey.text
        else:
            video_hotkey = self.default_video_hotkey
        if self.screenshot_hotkey.text:
            screenshot_hotkey = self.screenshot_hotkey.text
        else:
            screenshot_hotkey = self.default_screenshot_hotkey
        if self.fps_hotkey.text:
            fps_hotkey = self.fps_hotkey.text
        else:
            fps_hotkey = self.default_fps_hotkey

        keyboard.add_hotkey(video_hotkey, self.video_callback)
        keyboard.add_hotkey(screenshot_hotkey, self.screenshot_callback)
        keyboard.add_hotkey(fps_hotkey, self.fps_callback)

    def video_callback(self):
        self.game_inspector.config.start_video.trigger_action()

    def fps_callback(self):
        self.game_inspector.config.start_fps.trigger_action()

    def screenshot_callback(self):
        self.game_inspector.config.take_screen.trigger_action()

    def check_pid(self):
        try:
            self.pid_value = game_overlay_sdk.injector.get_pid()
            self.game_inspector.config.pid = self.pid_value
            self.game_inspector.config.use_overlay = True
            return True
        except game_overlay_sdk.injector.InjectionError as err:
            if err.exit_code != game_overlay_sdk.injector.CustomExitCodes.TARGET_PROCESS_IS_NOT_CREATED_ERROR.value:
                raise err
            else:
                return False
