import threading
import time
import os
import logging

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from fps_inspector_sdk import fps_inspector
from screen_recorder_sdk import screen_recorder
import game_overlay_sdk
import game_overlay_sdk.injector


class MessageThread(threading.Thread):

    def __init__(self):
        super(MessageThread, self).__init__()
        self.need_quit = False

    def run(self):
        while not self.need_quit:
            try:
                current_data = fps_inspector.get_last_fliprates(1)
                if len(current_data > 0):
                    game_overlay_sdk.injector.send_message('FPS %.1f FlipRate %.1f' % (current_data['FPS'][0], current_data['FlipRate'][0]))
                time.sleep (1)
            except game_overlay_sdk.injector.InjectionError as err:
                if err.exit_code == game_overlay_sdk.injector.CustomExitCodes.TARGET_PROCESS_IS_NOT_CREATED_ERROR.value:
                    logging.warning('target process is not created')
                    time.sleep (1)
                elif err.exit_code == game_overlay_sdk.injector.CustomExitCodes.TARGET_PROCESS_WAS_TERMINATED_ERROR.value:
                    logging.warning('target process was stopped')
                    time.sleep (1)
                else:
                    logging.error(str(err))
            except Exception as e:
                logging.error(str(e))


class Config(BoxLayout):

    def __init__(self, fps_plot, video_player, screenshot, **kwargs):
        super(Config, self).__init__(orientation = 'vertical')
        # pid, use_overlay are configured in config_session, bad design but it works 
        self.pid = 0
        self.use_overlay = False
        
        self.thread = None
        self.video_filename = None
        self.video_player = video_player
        self.fps_plot = fps_plot
        self.screenshot = screenshot

        self.start_video = Button(text='Start Video', font_size=20)
        self.start_video.background_normal = ''
        self.start_video.background_color = [.4, .3, .3, .85]
        self.start_video.bind(on_press=self.video_pressed)
        self.add_widget(self.start_video)

        self.take_screen = Button(text='Take ScreenShot', font_size=20)
        self.take_screen.background_normal = ''
        self.take_screen.background_color = [.3, .4, .3, .85]
        self.take_screen.bind(on_press=self.screen_pressed)
        self.add_widget(self.take_screen)

        self.start_fps = Button(text='Start FPS Measurement', font_size=20)
        self.start_fps.background_normal = ''
        self.start_fps.background_color = [.3, .3, .4, .85]
        self.start_fps.bind(on_press=self.fps_pressed)
        self.add_widget(self.start_fps)

    def fps_pressed(self, instance):
        try:
            if self.start_fps.text == 'Start FPS Measurement':
                fps_inspector.start_fliprate_recording(self.pid)
                self.start_fps.text = 'Stop FPS Measurement'
                if self.use_overlay:
                    game_overlay_sdk.injector.send_message('Start FPS Recording')
                    self.thread = MessageThread()
                    self.thread.start ()
                logging.info('Start FPS Recording')
            else:
                fps_inspector.stop_fliprate_recording()
                data = fps_inspector.get_all_fliprates()
                os.makedirs('data', exist_ok=True)
                filename = os.path.join('data', '%d.csv' % time.time())
                data.to_csv(filename)
                self.fps_plot.data = data
                if self.use_overlay:
                    game_overlay_sdk.injector.send_message('Stop FPS Recording, data saved to %s' % filename)
                    if self.thread is not None:
                        self.thread.need_quit = True
                        self.thread.join()
                        self.thread = None
                logging.info('Stop FPS Recording, data saved to %s' % filename)
                self.start_fps.text = 'Start FPS Measurement'
        except Exception as e:
            logging.error(str(e))

    def video_pressed(self, instance):
        try:
            if self.start_video.text == 'Start Video':
                os.makedirs('data', exist_ok=True)
                self.video_filename = os.path.join('data', '%d.mp4' % time.time())
                screen_recorder.start_video_recording(self.video_filename, 30, 8000000, True)
                logging.info('start video recording to %s' % self.video_filename)
                if self.use_overlay:
                    game_overlay_sdk.injector.send_message('start video recording to %s' % self.video_filename)
                self.start_video.text = 'Stop Video'
            else:
                logging.info('stop video recording')
                if self.use_overlay:
                    game_overlay_sdk.injector.send_message('stop video recording')
                self.start_video.text = 'Start Video'
                screen_recorder.stop_video_recording()
                self.video_player.source = self.video_filename
        except Exception as e:
            logging.error(str(e))

    def screen_pressed(self, instance):
        try:
            os.makedirs('data', exist_ok=True)
            filename = os.path.join('data', '%d.png' % time.time())
            screen_recorder.get_screenshot (5).save (filename)
            if self.use_overlay:
                game_overlay_sdk.injector.send_message('ScreenShot saved to %s' % filename)
            logging.info('ScreenShot saved to %s' % filename)
            self.screenshot.source = filename
            self.screenshot.reload()
        except Exception as e:
            logging.error(str(e))


def get_config(fps_plot, video_player, screenshot):
    return Config(fps_plot, video_player, screenshot)
