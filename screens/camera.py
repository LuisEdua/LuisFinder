import cv2
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDIconButton
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
import os

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt.xml")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(dir_path, 'model.xml')
        self.recognizer.read(model_path)
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def build(self):
        layout = MDBoxLayout(orientation='vertical')
        back_button = MDIconButton(icon='arrow-left', on_release=self.go_back)
        layout.add_widget(back_button)
        self.image = Image()
        layout.add_widget(self.image)
        self.add_widget(layout)

    def on_enter(self, *args):
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0 / 30.0)

    def load_video(self, *args):
        ret, frame = self.capture.read()
        if ret:

            faces = self.detector.detectMultiScale(frame, 1.3, 5)

            for (x, y, w, h) in faces:
                gray = cv2.cvtColor(frame[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
                label, confidence = self.recognizer.predict(gray)
                if label == 0 and confidence <= 60:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (10, 255, 0), 2)
                    cv2.putText(frame, 'Luis', (x, y+h+30), self.font, 1, (10, 255, 0), 2, cv2.LINE_AA)
                else:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame, 'Desconocido', (x, y+h+30), self.font, 1, (0, 0, 255), 2, cv2.LINE_AA)          

            frame = cv2.flip(frame, 0)

            buffer = frame.tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture

    def go_back(self, instance):
        self.manager.current = 'home'

    def on_leave(self, *args):
        self.capture.release()
        Clock.unschedule(self.load_video)