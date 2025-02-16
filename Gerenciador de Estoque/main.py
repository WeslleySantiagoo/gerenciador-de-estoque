from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.filechooser import Screen
from kivy.clock import Clock
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

config = {
    "apiKey": "SUA_API_KEY",
    "authDomain": "SEU_PROJETO.firebaseapp.com",
    "databaseURL": "https://SEU_PROJETO.firebaseio.com",
    "storageBucket": "SEU_PROJETO.appspot.com",
    'messagingSenderId': "SEU_SENDER_ID",
    'appId': "SUA_APP_ID",
    'easurementId': "SEU_EASUREMENT_ID"
}


fb = pyrebase.initialize_app(config)
db = fb.database()


class LoginScreen(Screen):
    def clear_fields(self):
        self.ids.email_input.text='@ufrpe.br'
        self.ids.password_input.text=''


    def verify_dominion_email(self, email_field):
            if email_field.text != "":
                email_field.error = not email_field.text.endswith('@ufrpe.br')


    def invalid_password(self, password):
        if len(password) < 6:
            return True
        return False
        

    def verify_password(self, password_field):
        password_field.error = self.invalid_password(password_field.text) != False


    def sign_in_button(self, email, password):
        sign_in = functions.sign_in_db(email.lower(), password)
        if sign_in == "Logado com sucesso":           #TEST MODE A
            self.manager.current='Tela de Estoque'    #TEST MODE A
            self.clear_fields()                       #TEST MODE A
        # self.manager.current='Tela de Estoque'      #TEST MODE B
        # self.clear_fields()                         #TEST MODE B
        return functions.open_snackbar(sign_in)
    

    def sign_up_button(self, email, password):
        sign_up = functions.sign_up_db(email.lower(), password)
        return functions.open_snackbar(sign_up)


class EstoqueScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.add_items, 0.1)
        Clock.schedule_once(self.update_list_estoque, 0.2)


    def add_items(self, a=None):
        lista = self.ids.main_scroll
        estoque = functions.get_db_estoque()
        if estoque != 'Estoque Vazio':
            estoque = estoque.items()
            for k, v in estoque:
                item = MDListItem(radius=[10,10,10,10])
                item.add_widget(MDListItemTrailingIcon(icon='hammer-screwdriver'))
                item.add_widget(MDListItemHeadlineText(text=k))
                item.add_widget(MDListItemSupportingText(text=f"Código: {v['codigo']}"))
                item.add_widget(MDListItemTertiaryText(text=f"Quantidade em Estoque: {v['qtEstoque']}"))
                lista.add_widget(item)
        else:
            functions.open_snackbar('Estoque Vazio')


    def update_list_estoque(self, a=None):
        try:
            lista = self.ids.main_scroll
            lista.clear_widgets()
            self.add_items()
        except:
            pass


class AnaliseScreen(Screen):
    def shortly(self):
        functions.open_snackbar('EM BREVE - 3a V.A')


class MovimentacoesScreen(Screen):
    pass


class ConfiguracoesScreen(Screen):
    def logout(self):
        functions.open_snackbar('Seção encerrada')
        Clock.schedule_once(self.exit_sreen, 0.5)


    def exit_sreen(self,a=None):
        self.manager.current='Tela de Login'


    def close_app(self, a=None):
        app = MDApp.get_running_app()
        app.stop()


class CadastroProdutoScreen(Screen):
    def on_enter(self):
        try:
            self.estoque = functions.get_db_estoque()
            print(self.estoque)             #VIEW MODE
            print(self.estoque.keys())      #VIEW MODE
        except:
            pass
        

    def existing_name_check(self, text_field):
        try:
            if functions.check_name_product((text_field.text).title(), self.estoque) == 'Erro':
                text_field.error = True
                functions.open_snackbar('O produto já existe')
                return 'ERRO'
        except:
            pass


    def save_and_continue(self, name, code, qt, unit, report):
        if name != '':
            if code != '':
                if qt != '':
                    if unit != '':
                        if report != '':
                            if self.ids.product_name_input.error != True:
                                functions.add_new_product(name, code, qt, unit, report)
                                functions.open_snackbar('Produto Adicionado com sucesso')
                                self.ids.product_name_input.text = ''
                                self.ids.product_code_input.text = ''
                                self.ids.product_qt_input.text = ''
                                self.ids.product_unit_input.text = ''
                                self.ids.product_report_input.text = ''
                            else:
                                functions.open_snackbar('O produto já existe')
                        else:
                            functions.open_snackbar('Insira o motivo')
                    else:
                        functions.open_snackbar('Insira a unidade')
                else:
                    functions.open_snackbar('Insira a quantidade')
            else:
                functions.open_snackbar('Insira o código')
        else:
            functions.open_snackbar('Insira o nome')


    def save_and_exit(self, name, code, qt, unit, report):
        if name != '':
            if code != '':
                if qt != '':
                    if unit != '':
                        if report != '':
                            if self.ids.product_name_input.error != True:
                                functions.add_new_product(name, code, qt, unit, report)
                                functions.open_snackbar('Produto Adicionado com sucesso')
                                self.ids.product_name_input.text = ''
                                self.ids.product_code_input.text = ''
                                self.ids.product_qt_input.text = ''
                                self.ids.product_unit_input.text = ''
                                self.ids.product_report_input.text = ''
                                self.manager.current = 'Tela de Estoque'
                            else:
                                functions.open_snackbar('O produto já existe')
                        else:
                            functions.open_snackbar('Insira o motivo')
                    else:
                        functions.open_snackbar('Insira a unidade')
                else:
                    functions.open_snackbar('Insira a quantidade')
            else:
                functions.open_snackbar('Insira o código')
        else:
            functions.open_snackbar('Insira o nome')
        

class EntradaProdutoScreen(Screen):
    pass


class SaidaProdutoScreen(Screen):
    pass


class MainApp(MDApp):
    def build(self):
        Window.size = (360, 640)
        self.title = "Genciador de Estoque"
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('telas.kv')
    
        


MainApp().run()