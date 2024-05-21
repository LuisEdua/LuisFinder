from kivymd.uix.screen import Screen
from kivy.lang import Builder


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        Builder.load_file('screens/home.kv')
