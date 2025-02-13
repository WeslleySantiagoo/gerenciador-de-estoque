import pyrebase
from kivymd.uix.snackbar import MDSnackbar,MDSnackbarText

config = {
    "apiKey": "SUA_API_KEY",
    "authDomain": "SEU_PROJETO.firebaseapp.com",
    "databaseURL": "https://SEU_PROJETO.firebaseio.com",
    "storageBucket": "SEU_PROJETO.appspot.com",
    'messagingSenderId': "SEU_SENDER_ID",
    'appId': "SUA_APP_ID",
    'easurementId': "SEU_EASUREMENT_ID"
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
        

def open_snackbar_sign_in(msg):
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


def open_snackbar_sign_up(msg):
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
        

def open_snackbar_logout(msg):
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
    for i in estoque.val():
        description = {
            'codigo': str(estoque.val()[i]['codigo']),
            'qtEstoque': str(estoque.val()[i]['qtEstoque'])
        }
        lista[str(i)] = description
    return lista


def graphic_generate():
    import matplotlib.pyplot as plt

    sizes = [50, 50]
    colors = ['#2F47ED', '#ED3A3A']

    # Criar figura e eixos
    fig, ax = plt.subplots(figsize=(5, 5), dpi=100)  # 300x300px

    # Criar o gráfico de pizza
    wedges, _ = ax.pie(
        sizes, colors=colors,
        startangle=90,
        wedgeprops={'edgecolor': '#AED1C8'}
    )

    # Criar o círculo central (anel)
    center_circle = plt.Circle((0, 0), 0.6, fc='#AED1C8', linewidth=2)
    ax.add_artist(center_circle)

    # Remover margens
    ax.set_xlim(-1, 1)  # Ajusta os limites para ficar bem próximo da borda
    ax.set_ylim(-1, 1)
    plt.axis('off')  # Remove completamente os eixos

    # Ajustar a posição do gráfico para ocupar 100% da imagem
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Salvar imagem sem bordas extras
    plt.savefig(
        "Gerenciador de Estoque/Images/ring_graphic.png",
        dpi=100,
        bbox_inches='tight',
        transparent=True,
        pad_inches=0
    )

