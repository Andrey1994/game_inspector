from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup    
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window


class Alert(Popup):

    def __init__(self, title, text, condition=None):
        super(Alert, self).__init__()
        self.condition = condition
        content = BoxLayout(orientation='vertical')
        content.add_widget(
            Label(text=text, size_hint=(1, .5))
        )
        ok_button = Button(text='Ok', size_hint=(1, .5))
        content.add_widget(ok_button)

        self.popup = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(Window.width / 3, Window.height / 3),
            auto_dismiss=True,
        )
        ok_button.bind(on_press=self.close)
        self.popup.open()

    def close(self, instance):
        if self.condition is None:
            self.popup.dismiss()
        else:
            if self.condition():
                self.popup.dismiss()
