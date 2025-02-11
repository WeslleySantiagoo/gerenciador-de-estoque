#pendente
import pyrebase
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

config = {}
global fb, auth, user, db
fb = pyrebase.initialize_app(config)
db = fb.database()


def sign_in_db(email, password):
    if len(email) > 9:
        if email[-9:] == '@ufrpe.br':
            if len(password) >= 6:
                auth = fb.auth()
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    return "Logado com sucesso"
                except:
                    print(Exception)
                    return 'Email ou senha incorreto.'
            else:
                return 'Senha deve conter mais de 6 dígitos'
        else:
            return 'Dominio incorreto'
    else:
        return 'Email pequeno demais'
    

def sign_up_db(email, password):
    if len(email) > 9:
        if email[-9:] == '@ufrpe.br':
            if len(password) >= 6:
                auth = fb.auth()
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                    return "Conta criada com sucesso"
                except:
                    return "O email já está cadastrado"
            return 'Senha deve conter mais de 6 dígitos'
        else:
            return 'Dominio incorreto'
    else:
        return 'Email pequeno demais'
        

def open_popup_sign_in(msg):
        popup = Popup(
            title="Sign In",
            size_hint=(None, None),
            size=(300, 150),
            background_color=(1,1,1,1)
        )
        fechar_btn = Button(text="Fechar")
        fechar_btn.bind(on_press=popup.dismiss)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text=msg))
        layout.add_widget(fechar_btn)
        popup.add_widget(layout)
        popup.open()


def open_popup_sign_up(msg):
        popup = Popup(
            title="Sign Up",
            size_hint=(None, None),
            size=(300, 150),
            background_color=(1,1,1,1)
        )

        fechar_btn = Button(text="Fechar")
        fechar_btn.bind(on_press=popup.dismiss)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text=msg))
        layout.add_widget(fechar_btn)
        popup.add_widget(layout)
        popup.open()


def get_db_estoque():
    lista = dict()
    estoque = db.child('Estoque').get()
    for i in estoque.val():
        description = {
            'codigo': str(estoque.val()[i]['codigo']),
            'qtEstoque': str(estoque.val()[i]['qtEstoque'])
        }
        lista[str(i)] = description

    return lista