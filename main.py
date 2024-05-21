from kivymd.app import MDApp
from kivy.lang import Builder


class MyApp(MDApp):
    def build(self):
        self.title = 'Luis Finder'
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "200"
        self.theme_cls.theme_style = 'Dark'
        self.manager = Builder.load_file("my.kv")
        return self.manager

if __name__ == '__main__':
    MyApp().run()

