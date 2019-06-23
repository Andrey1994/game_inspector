from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class Plot(BoxLayout):
    data = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Plot, self).__init__(**kwargs)
        plt.figure()
        plt.plot([])
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def on_data(self, instance, value):
        if self.data is not None:
            self.clear_widgets()
            plt.figure ()
            self.data[self.data.ScreenTime != 0][['FPS', 'FlipRate', 'ScreenTime']].plot (x='ScreenTime', subplots=True)
            self.add_widget (FigureCanvasKivyAgg(plt.gcf()))


def get_fps_plot():
    return Plot()
