from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.screenmanager import ScreenManager
from kivy.uix.filechooser import Screen
from functions import *

class JanelaGerenciadora(ScreenManager):
    pass

class LoginScreen(Screen):
    pass

class EstoqueScreen(Screen):
    pass

class MainApp(MDApp):
    def build(self):
        Window.size = (360, 640)
        self.title = "Genciador de Estoque"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('telas.kv')
            
    def verify_dominion_email(self, email_field):
            if email_field.text != "":
                email_field.error = not email_field.text.endswith('@ufrpe.br')

    def invalid_password(self, password: str) -> str:
        if len(password) < 6:
            return True
        return False
            
    def verify_password(self, password_field):
        password_field.error = self.invalid_password(password_field.text) != False
        

MainApp().run()