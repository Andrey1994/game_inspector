from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '960')
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

import info
import config_session
import session


class GameInspector(App):

    def build(self):
        self.root = ScreenManager()
        self.root.add_widget(info.Info(self.root))
        self.game_inspector = session.GameInspector()
        self.session_settings = config_session.SessionSettings(self.root, self.game_inspector)
        self.root.add_widget(self.session_settings)
        self.root.add_widget(self.game_inspector)
        self.root.current = 'Info'
        return self.root


if __name__ == '__main__':
    GameInspector().run()
