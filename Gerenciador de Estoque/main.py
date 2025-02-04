from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.textfield import *
from kivymd.uix.toolbar import MDTopAppBar
from kivy.utils import get_color_from_hex


class JanelaGerenciadora(ScreenManager):
    pass

class LoginScreen(Screen):
    pass

class EstoqueScreen(Screen):
    pass

class MainApp(MDApp):
    def build(self):
        self.title = "Genciador de Estoque"
        custom_color_green = get_color_from_hex("#2E8B57")
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('telas.kv')
    
    def ir_tela_de_login(self):
        self.root.current = "Tela de Login"

MainApp().run()