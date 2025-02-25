import pyrebase
from kivymd.uix.snackbar import MDSnackbar,MDSnackbarText
from kivymd.uix.list import (
    MDListItem,
    MDListItemHeadlineText,
    MDListItemSupportingText,
    MDListItemTertiaryText,
    MDListItemTrailingIcon
)

config = {
    "apiKey": "SUA_API_KEY",
    "authDomain": "SEU_PROJETO.firebaseapp.com",
    "databaseURL": "https://SEU_PROJETO.firebaseio.com",
    "storageBucket": "SEU_PROJETO.appspot.com",
    'messagingSenderId': "SEU_SENDER_ID",
    'appId': "SUA_APP_ID",
    'measurementId': "SEU_EASUREMENT_ID"
}

global fb, auth, user, db
fb = pyrebase.initialize_app(config)
db = fb.database()
auth = fb.auth()

def sign_in_db(email, password):
    if len(email) > 9:
        if email[-9:] == '@ufrpe.br':
            if len(password) >= 6:
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    return "Logado com sucesso"
                except:
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
        

def open_snackbar(msg):
    MDSnackbar(
        MDSnackbarText(
            text=msg,
            pos_hint= {'center_x': 0.5,'center_y': 0.5},
        ),
        orientation="horizontal",
        pos_hint={"center_x": 0.5, "center_y":0.06},
        size_hint_x=0.9,
        duration=1,
    ).open()


def get_db_estoque():
    lista = dict()
    estoque = db.child('Estoque').get()
    try:
        for i in estoque.val():
            description = {
                'motivo': str(estoque.val()[i]['Motivo']),
                'unit': str(estoque.val()[i]['UnDeMed']),
                'codigo': str(estoque.val()[i]['codigo']),
                'qtEstoque': str(estoque.val()[i]['qtEstoque'])
            }
            lista[str(i).lower().title()] = description
        return lista
    except:
        return 'Estoque Vazio'


def check_name_product(text_field,estoque):
    produtos = estoque.keys()
    if text_field.lower().title() in produtos:
        return 'Erro'

def check_code_product(code_field,estoque):
    produtos = estoque.keys()
    codigos = []
    for k, v in estoque.items():
        codigos.append(v['codigo'])

    if code_field in produtos:
        return 'Erro'

def graphic_generate():
    entradas = 0
    saidas = 0
    log = db.child('Logs').get()
    log_time = log.val()
    try:
        for time in log_time:
            msg = log_time[time]['mensagem']
            if 'Entrou' in msg or 'Cadastro' in msg:
                entradas += int(log_time[time]['quantidade'])
            elif 'Saiu' in msg:
                saidas += int(log_time[time]['quantidade'])


        import matplotlib.pyplot as plt
        sizes = [entradas, saidas]
        colors = ['#2F47ED', '#ED3A3A']
        fig, ax = plt.subplots(figsize=(5, 5), dpi=100)

        wedges, _ = ax.pie(
            sizes,
            colors=colors,
            startangle=90,
            wedgeprops={'edgecolor': '#AED1C8'}
        )

        center_circle = plt.Circle((0, 0), 0.6, fc='#AED1C8', linewidth=2)
        ax.add_artist(center_circle)

        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        plt.axis('off')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        plt.savefig(
            "Gerenciador de Estoque/Images/ring_graphic.png",
            dpi=100,
            bbox_inches='tight',
            transparent=True,
            pad_inches=0
        )
        return entradas, saidas
    except:
        pass

def add_new_product(name, code, qt, unit, report):
    db.child('Estoque').update({
        name.lower().title():{
            'codigo': code,
            'qtEstoque': qt,
            'UnDeMed': unit,
            'Motivo': report
        }
    })


def add_items_list_stock(self):
    lista = self.ids.main_scroll
    estoque = get_db_estoque()
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
        open_snackbar('Estoque Vazio')


def add_items_list_moviments(self):
    lista = self.ids.main_scroll
    log = db.child('Logs').get()
    try:
        for time in reversed(log.val()):
            item = MDListItem(radius=[10,10,10,10])
            if "Entrou" in log.val()[time]['mensagem']:
                item.add_widget(MDListItemTrailingIcon(
                    icon='arrow-up-drop-circle',
                    icon_color= '#2F47ED'
                ))
            elif "Saiu" in log.val()[time]['mensagem']:
                item.add_widget(MDListItemTrailingIcon(
                    icon='arrow-down-drop-circle',
                    icon_color= '#2F47ED'
                ))
            elif "excluido" in log.val()[time]['mensagem']:
                item.add_widget(MDListItemTrailingIcon(
                    icon='trash-can-outline',
                    icon_color= '#2F47ED'
                ))
            elif "Cadastro" in log.val()[time]['mensagem']:
                item.add_widget(MDListItemTrailingIcon(
                    icon='database-arrow-up',
                    icon_color= '#2F47ED'
                ))


            item.add_widget(MDListItemHeadlineText(text=str(time)))
            item.add_widget(MDListItemSupportingText(text=str(log.val()[time]['mensagem'])))
            item.add_widget(MDListItemTertiaryText(text=str(log.val()[time]['motivo'])))
            lista.add_widget(item)
    except Exception as e:
        open_snackbar('ERRO!')


def enter_product(dict_p, report):
    for k, v in dict_p.items():
        from time import sleep
        sleep(0.2)
        db.child('Estoque').child(k).update({'qtEstoque': str(v[1])})
        add_log(k,v[1]-v[0],'entrada',report)
    open_snackbar('Entrada dos itens concluida')


def remove_product(dict_p, report):
    from time import sleep
    for k, v in dict_p.items():
        sleep(0.1)
        add_log(k,v[0]-v[1],'saida', report)
        sleep(0.5)
        if v[1] == 0:
            add_log(k,None,'exclusao',report)
            db.child('Estoque').child(k).remove()
        else:
            db.child('Estoque').child(k).update({'qtEstoque': str(v[1])})
    open_snackbar('Saída dos itens concluida')


def save_and_continue(self, name, code, qt, unit, report):
    text_input = self.ids.product_name_input
    code_input = self.ids.product_code_input
    name = name.strip().lower().title()
    code = code.strip()
    qt = qt.strip()
    unit = unit.strip()
    report = report.strip().capitalize()
    if name == '':
        open_snackbar('Insira o nome')
    elif code == '':
         open_snackbar('Insira o código')
    elif qt == '':
         open_snackbar('Insira a quantidade')
    elif unit == '':
         open_snackbar('Insira a unidade')
    elif report == '':
         open_snackbar('Insira o motivo')
    elif text_input.error != True:
        try:
            qt = int(qt)
            add_new_product(name, code, qt, unit, report)
            add_log(name,qt,'cadastro',report)
            open_snackbar('Produto adicionado com sucesso')
            self.ids.product_name_input.text = ''
            self.ids.product_code_input.text = ''
            self.ids.product_qt_input.text = ''
            self.ids.product_unit_input.text = ''
            self.ids.product_report_input.text = ''
        except:
            open_snackbar('Insira uma quantidade válida')
    else:
        open_snackbar('O produto já existe')


def save_and_exit(self, name, code, qt, unit, report,):
    text_input = self.ids.product_name_input
    code_input = self.ids.product_code_input
    name = name.strip().lower().title()
    code = code.strip()
    qt = qt.strip()
    unit = unit.strip()
    report = report.strip().capitalize()
    if name == '':
        open_snackbar('Insira o nome')
    elif code == '':
         open_snackbar('Insira o código')
    elif qt == '':
         open_snackbar('Insira a quantidade')
    elif unit == '':
         open_snackbar('Insira a unidade')
    elif report == '':
         open_snackbar('Insira o motivo')
    elif text_input.error != True:
        try:
            qt = int(qt)
            add_new_product(name, code, qt, unit, report)
            add_log(name,qt,'cadastro',report)
            open_snackbar('Produto adicionado com sucesso')
            self.ids.product_name_input.text = ''
            self.ids.product_code_input.text = ''
            self.ids.product_qt_input.text = ''
            self.ids.product_unit_input.text = ''
            self.ids.product_report_input.text = ''
            self.manager.current = 'Tela de Estoque'
        except:
            open_snackbar('Insira uma quantidade válida')
    else:
        open_snackbar('O produto já existe')


def add_log(name, qt, operation, report):
    from datetime import datetime
    data_hora = datetime.now().strftime("%d-%m-%Y - %H:%M:%S")
    estoque_ = get_db_estoque()
    unit = estoque_[name]['unit']
    code = estoque_[name]['codigo']
    
    match operation:
        case 'entrada':
            msg = f'Entrou {qt}{unit} de {name}.'
        case 'saida':
            msg = f'Saiu {qt}{unit} de {name}.'
        case 'cadastro':
            msg = f'Cadastro: {name} - Código: {code} - Quantidade: {qt}.'
        case 'exclusao':
            msg = f'O produto {name} foi excluido por não ter mais material no estoque'

    db.child('Logs').child(data_hora).set({
        'mensagem': msg,
        'motivo': report,
        'quantidade': qt
    })


dialog = None
report = None
callback_function = None
def open_dialog(callback, enter_exit):
    if enter_exit == 'enter':
        icon = 'database-arrow-up'
    else:
        icon = 'database-arrow-down'
    from kivymd.uix.button import MDButton,MDButtonText
    from kivymd.uix.widget import Widget
    from kivymd.uix.dialog import (
        MDDialog,
        MDDialogIcon,
        MDDialogHeadlineText,
        MDDialogContentContainer,
        MDDialogButtonContainer
    )
    from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
    global dialog, report, callback_function
    callback_function = callback
    report = MDTextField(
                MDTextFieldHintText(
                    text= "Motivo",
                    theme_font_name= 'Custom',
                    font_name= 'Fonts/Poppins-Regular.ttf'
                ),
                id= 'report',
                mode= 'outlined',
                pos_hint= {'center_x': 0.5,'center_y': 0.8},
                size_hint= (0.9, None),
                theme_line_color= "Custom",
                line_color_normal= (209/255, 209/255, 209/255, 1),
                padding= [0,10,0,10],
            )
    dialog = MDDialog(
        MDDialogIcon(
            icon=icon
        ),
        MDDialogHeadlineText(
            text='Confirmação'
        ),
        MDDialogContentContainer(
            report
        ),

        MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Cancelar"),
                    style="text",
                    on_release= close_dialog
                ),
                MDButton(
                    MDButtonText(text="Confirmar"),
                    style="text",
                    on_release=confirm
                ),
                spacing="8dp",
            ),
        size_hint_x= 0.9
    )
    dialog.open()
def close_dialog(instance=None):
    global dialog
    if dialog:
        dialog.dismiss()
def confirm(instance):
    global report, callback_function
    motivo = report.text
    close_dialog()
    if callback_function:
        callback_function(motivo)
