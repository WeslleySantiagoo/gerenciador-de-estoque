from kivymd.app import MDApp
from kivy.uix.label import Label
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
    'measurementId': "SEU_EASUREMENT_ID"
}


fb = pyrebase.initialize_app(config)
db = fb.database()


class LoginScreen(Screen):
    def clear_fields(self):
        self.ids.email_input.text='@ufrpe.br'
        self.ids.password_input.text=''


    def verify_dominion_email(self, email_field):
            if email_field.text.strip().lower() != "":
                email_field.error = not email_field.text.strip().lower().endswith('@ufrpe.br')


    def invalid_password(self, password):
        if len(password) < 6:
            return True
        return False


    def verify_password(self, password_field):
        password_field.error = self.invalid_password(password_field.text) != False


    def sign_in_button(self, email, password):
        sign_in = functions.sign_in_db(email.lower().strip(), password)
        if sign_in == "Logado com sucesso":
            self.manager.current='Tela de Estoque'
            self.clear_fields()                     
        return functions.open_snackbar(sign_in)


    def sign_up_button(self, email, password):
        sign_up = functions.sign_up_db(email.lower().strip(), password)
        return functions.open_snackbar(sign_up)


class EstoqueScreen(Screen):
    def on_enter(self):
        self.count = 0
        if self.count == 0:
            Clock.schedule_once(self.add_items, 0.01)
            self.count += 1
        if self.count > 0:
            Clock.schedule_once(self.update_list_estoque, 0.02)
        try:
            self.entradas, self.saidas = functions.graphic_generate()
        except:
            pass


    def add_items(self, a=None):
        functions.add_items_list_stock(self)


    def update_list_estoque(self, a=None):
        try:
            lista = self.ids.main_scroll
            lista.clear_widgets()
            self.add_items()
        except:
            pass


class AnaliseScreen(Screen):
    def on_pre_enter(self):
        try:
            estoque_screen = self.manager.get_screen('Tela de Estoque')
            entradas = getattr(estoque_screen, "entradas", 0)
            saidas = getattr(estoque_screen, "saidas", 0)
            self.ids.entrada.text = f'Entradas: {entradas}'
            self.ids.saida.text = f'Saidas: {saidas}'
        except:
            self.ids.entrada.text = f'Entradas: -----'
            self.ids.saida.text = f'Saidas: ----'

        self.ids.image.reload()


    def shortly(self):
        functions.open_snackbar('EM BREVE - 3a V.A')


class MovimentacoesScreen(Screen):
    def on_enter(self):
        self.ids.main_scroll.clear_widgets()
        functions.add_items_list_moviments(self)


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
        except:
            pass


    def existing_name_check(self, text_field):
        try:
            if functions.check_name_product((text_field.text).title().strip(), self.estoque) == 'Erro':
                text_field.error = True
                functions.open_snackbar('O produto já existe')
                return 'ERRO'
        except:
            pass


    def existing_code_check(self, code_field):
        try:
            if functions.check_code_product(code_field.text, self.estoque) == 'Erro':
                code_field.error = True
                functions.open_snackbar('O código já existe')
                return 'ERRO'
        except:
            pass


    def save_and_continue(self, name, code, qt, unit, report):
        functions.save_and_continue(self, name, code, qt, unit, report)


    def save_and_exit(self, name, code, qt, unit, report):
        functions.save_and_exit(self, name, code, qt, unit, report)


class EntradaProdutoScreen(Screen):
    def on_enter(self):
        self.estoque = functions.get_db_estoque()
        self.produtos = self.estoque.keys()
        self.text = self.ids.product_name_input_enter.text
        self.ids.add_enter_list.disabled = True
        self.ids.product_name_input_enter.bind(focus=self.on_focus)
        self.list_enter = {}


    def on_focus(self, a, value):
        if not value:
            self.ids.suggestion_list.clear_widgets()
            self.ids.product_qt_input_enter.disabled = False
        else:
            self.ids.product_qt_input_enter.disabled = True

    
    def verify_name(self, a=None):
        if self.text in self.produtos:
            self.ids.suggestion_list.clear_widgets()
            self.ids.add_enter_list.disabled = False
        else:
            self.ids.add_enter_list.disabled = True


    def filter_suggestions(self, text):
        self.text = text
        suggestion_list = self.ids.suggestion_list
        suggestion_list.clear_widgets()
        self.verify_name()
        if text:
            filtered_items = [item for item in self.produtos if text.lower() in item.lower()]

            for item in filtered_items:
                label = Label(text=item, size_hint_y=None, height=40, color = [0,0,0,1])
                label.bind(on_touch_down= self.select_suggestion)
                suggestion_list.add_widget(label)
        

    def select_suggestion(self, instance, click):
        if instance.collide_point(*click.pos):
            self.ids.product_name_input_enter.text = instance.text
            self.ids.suggestion_list.clear_widgets()


    def add_list_enter(self, name, qt_entering):
        if name != '':
            if self.ids.product_name_input_enter.text in self.list_enter.keys():
                functions.open_snackbar('Produto ja adicionado a lista')
            else:
                qt = int(self.estoque[self.text]['qtEstoque'])
                try:
                    new_qt = qt + int(qt_entering)
                    lista = self.ids.main_scroll_enter
                    item = MDListItem(radius=[10,10,10,10])
                    item.add_widget(MDListItemTrailingIcon(icon='arrow-up-drop-circle'))
                    item.add_widget(MDListItemHeadlineText(text=name))
                    item.add_widget(MDListItemSupportingText(text=f"Quantidade antes: {qt}"))
                    item.add_widget(MDListItemTertiaryText(text=f"Quantidade após: {new_qt}"))
                    lista.add_widget(item)

                    self.list_enter[name]= [qt, int(new_qt)]

                    self.ids.product_name_input_enter.text = ''
                    self.ids.product_qt_input_enter.text = ''
                except:
                    functions.open_snackbar('Insira uma quantidade válida')


    def add_product_db(self):
        def continuar(motivo):
            if not motivo.strip():
                functions.open_snackbar('Digite um motivo antes de continuar')
                return
        
            if len(self.list_enter.keys()) == 0:
                functions.open_snackbar('Adicione algum item na lista primeiro')
            else:
                functions.enter_product(self.list_enter, motivo)
                self.ids.main_scroll_enter.clear_widgets()
                self.manager.current = 'Tela de Estoque'
        functions.open_dialog(continuar, 'enter')
    

    def back_button(self):
        self.manager.current='Tela de Estoque'
        self.ids.main_scroll_enter.clear_widgets()


class SaidaProdutoScreen(Screen):
    def on_enter(self):
        self.estoque = functions.get_db_estoque()
        self.produtos = self.estoque.keys()
        self.text = self.ids.product_name_input_exit.text
        self.ids.add_exit_list.disabled = True
        self.ids.product_name_input_exit.bind(focus=self.on_focus)
        self.ids.product_qt_input_exit.disabled = True
        self.list_exit = {}


    def on_focus(self, a, value):
        if not value:
            self.ids.suggestion_list.clear_widgets()
            self.ids.product_qt_input_exit.disabled = False
        else:
            self.ids.product_qt_input_exit.disabled = True

    
    def verify_name(self, a=None):
        if self.text in self.produtos:
            self.ids.suggestion_list.clear_widgets()
            self.ids.add_exit_list.disabled = False
        else:
            self.ids.add_exit_list.disabled = True


    def filter_suggestions(self, text):
        self.text = text
        suggestion_list = self.ids.suggestion_list
        suggestion_list.clear_widgets()
        self.verify_name()
        if text:
            filtered_items = [item for item in self.produtos if text.lower() in item.lower()]

            for item in filtered_items:
                label = Label(text=item, size_hint_y=None, height=40, color = [0,0,0,1])
                label.bind(on_touch_down= self.select_suggestion)
                suggestion_list.add_widget(label)
        

    def select_suggestion(self, instance, click):
        if instance.collide_point(*click.pos):
            self.ids.product_name_input_exit.text = instance.text
            self.ids.suggestion_list.clear_widgets()


    def add_list_exit(self, name, qt_exiting):
        if name != '':
            if self.ids.product_name_input_exit.text in self.list_exit.keys():
                functions.open_snackbar('Produto ja adicionado a lista')

            else:
                qt = int(self.estoque[self.text]['qtEstoque'])
                try:
                    qt_exiting = int(qt_exiting)
                    if qt_exiting <= 0:
                        functions.open_snackbar('Insira uma quantidade válida')
                    elif qt_exiting > qt:
                            functions.open_snackbar(f'Você tem apenas {qt} no estoque')
                    else:
                        new_qt = qt - int(qt_exiting)
                        lista = self.ids.main_scroll_exit
                        item = MDListItem(radius=[10,10,10,10])
                        item.add_widget(MDListItemTrailingIcon(icon='arrow-down-drop-circle'))
                        item.add_widget(MDListItemHeadlineText(text=name))
                        item.add_widget(MDListItemSupportingText(text=f"Quantidade antes: {qt}"))
                        item.add_widget(MDListItemTertiaryText(text=f"Quantidade após: {new_qt}"))
                        lista.add_widget(item)

                        self.list_exit[name]= [qt, int(new_qt)]

                        self.ids.product_name_input_exit.text = ''
                        self.ids.product_qt_input_exit.text = ''
                except:
                    functions.open_snackbar('Insira uma quantidade válida')


    def remove_product_db(self):
        def continuar(motivo):
            if not motivo.strip():
                functions.open_snackbar('Digite um motivo antes de continuar')
                return
            
            if len(self.list_exit.keys()) == 0:
                functions.open_snackbar('Adicione algum item na lista primeiro')
            else:
                functions.remove_product(self.list_exit, motivo)
                self.ids.main_scroll_exit.clear_widgets()
                self.manager.current = 'Tela de Estoque'

        functions.open_dialog(continuar, 'exit')
        

    def back_button(self):
        self.manager.current='Tela de Estoque'
        self.ids.main_scroll_exit.clear_widgets()

    
class MainApp(MDApp):
    def build(self):
        Window.size = (360, 640)
        self.title = "Genciador de Estoque"
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('telas.kv')


MainApp().run()
