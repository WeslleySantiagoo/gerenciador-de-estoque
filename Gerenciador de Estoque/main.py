from kivy.uix.gridlayout import product
from kivy.uix.actionbar import Label
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.filechooser import Screen
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivymd.uix.list import (
    MDListItem,
    MDListItemHeadlineText,
    MDListItemSupportingText,
    MDListItemTertiaryText,
    MDListItemTrailingIcon
)


import functions
import pyrebase

global db

config = {}

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
        # if sign_in == "Logado com sucesso":           #TEST MODE
        #     self.manager.current='Tela de Estoque'    #TEST MODE
        self.manager.current='Tela de Estoque'
        return self.open_popup_sign_in(sign_in)
    

    def sign_up_button(self, email, password):
        sign_up = functions.sign_up_db(email, password)
        return self.open_popup_sing_up(sign_up)
    
    
    def open_popup_sign_in(self, msg):
        return functions.open_popup_sign_in(msg)
    

    def open_popup_sing_up(self, msg):
        return functions.open_popup_sign_up(msg) 


class EstoqueScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.add_items, 1)


    def add_items(self, a=None):
        lista = self.ids.main_scroll
        for k, v in functions.get_db_estoque().items():
            item = MDListItem(radius=[10,10,10,10])
            item.add_widget(MDListItemTrailingIcon(icon='hammer-screwdriver'))
            item.add_widget(MDListItemHeadlineText(text=k))
            item.add_widget(MDListItemSupportingText(text=f"Código: {v['codigo']}"))
            item.add_widget(MDListItemTertiaryText(text=f"Quantidade em Estoque: {v['qtEstoque']}"))
            lista.add_widget(item)


    def update_list_estoque(self):
        lista = lista = self.ids.main_scroll
        lista.clear_widgets()
        self.add_items()

class MainApp(MDApp):
    dialog = None
    def build(self):
        Window.size = (360, 640)
        self.title = "Genciador de Estoque"
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('telas.kv')
    
        


MainApp().run()