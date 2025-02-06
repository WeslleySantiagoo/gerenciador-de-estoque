from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.screenmanager import ScreenManager
from kivy.uix.filechooser import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
import functions
import pyrebase

global db

config = {
    'apiKey': "AIzaSyAJlxRR9YogNG0Hnztn618x8I7pAQVoCZc",
'authDomain': "gerenciador-de-estoque-pisi-i.firebaseapp.com",
'databaseURL': "https://gerenciador-de-estoque-pisi-i-default-rtdb.firebaseio.com",
'projectId': "gerenciador-de-estoque-pisi-i",
'storageBucket': "gerenciador-de-estoque-pisi-i.firebasestorage.app",
'messagingSenderId': "148937568721",
'appId': "1:148937568721:web:95b0e583f8ee82538230f0",
'easurementId': "G-2001V6GRXW"
}
LabelBase.register(name='Poppins', fn_regular='Fonts/Poppins-Bold.ttf')
fb = pyrebase.initialize_app(config)
db = fb.database()


class LoginScreen(Screen):
    def verify_dominion_email(self, email_field):
            if email_field.text != "":
                email_field.error = not email_field.text.endswith('@ufrpe.br')

    def invalid_password(self, password: str) -> str:
        if len(password) < 6:
            return True
        return False
            
    def verify_password(self, password_field):
        password_field.error = self.invalid_password(password_field.text) != False


    def sign_in_button(self, email, password):
        sign_in = functions.sign_in_db(email, password)
        # if sign_in == "Logado com sucesso":
        #     self.manager.current='Tela de Estoque'
        self.manager.current='Tela de Estoque'
        return self.open_popup_sign_in(sign_in)
    

    def sign_up_button(self, email, password):
        sign_up = functions.sign_up_db(email, password)
        return self.open_popup_sing_up(sign_up)
    
    
    def open_popup_sign_in(self, msg):
        return functions.open_popup_sign_in(msg)
    

    def open_popup_sing_up(self, msg):
        return functions.open_popup_sign_up(msg) 
    pass

class EstoqueScreen(Screen):

    pass

class MainApp(MDApp):
    dialog = None
    def build(self):
        Window.size = (360, 640)
        self.title = "Genciador de Estoque"
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('telas.kv')
MainApp().run()