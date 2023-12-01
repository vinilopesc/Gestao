from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import firebase_admin
from firebase_admin import credentials, auth, firestore
import re


class CadastroPage(Screen):
    erro_mensagem = StringProperty('')
    erro_usuario = StringProperty('')
    erro_nome = StringProperty('')
    erro_email = StringProperty('')
    erro_telefone = StringProperty('')
    erro_cpf = StringProperty('')
    erro_senha = StringProperty('')
    largura_caixa_texto = 0.35
    altura_caixa_texto = 0.05
    altura_btn = 0.05
    largura_btn = 0.15
    altura_label = 0.2
    largura_label = 0.2

    def tratar_nome(self, nome):
        nome = ' '.join(word.capitalize() for word in nome.split())
        if not nome:
            return None, "Nome é obrigatório."
        if not re.match(r'^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ ]+$', nome):
            return None, "Nome inválido. Use apenas letras e espaços."
        if len(nome) > 50:
            return None, "Nome muito longo. Máximo de 50 caracteres."
        return nome, ''
    def tratar_email(self, email):
        if not email:
            return None, "Email é obrigatório."
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$'
        if not re.fullmatch(email_regex, email):
            return None, "Formato de email inválido."
        if self.verificar_email_existente(email):
            self.mostrar_popup_erro("O e-mail informado já está em uso")
        return email, ''

    def verificar_email_existente(self, email):
        try:
            user = auth.get_user_by_email(email)
            if user:
                return True
        except auth.UserNotFoundError:
            return False
        except Exception as e:
            self.mostrar_popup_erro(f"Erro ao verificar o e-mail: {e}")
            return False
    def tratar_usuario(self, usuario):
        if not usuario:
            return None, "Nome de usuário é obrigatório."
        min_length = 4
        max_length = 20
        if len(usuario) < min_length or len(usuario) > max_length:
            return None, f"Nome de usuário deve ter entre {min_length} e {max_length} caracteres."
        if not re.match(r'^\w+$', usuario):
            return usuario, "Nome de usuário pode conter apenas letras, números e underscores."
        return usuario, ''

    def tratar_telefone(self, telefone):
        if not telefone:
            return None, "Número de telefone é obrigatório."
        telefone_limpo = re.sub(r'[^0-9]', '', telefone)
        if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
            return None, "Número de telefone deve ter 10 ou 11 dígitos."
        return telefone_limpo, ''

    def tratar_cpf(self, cpf):
        cpf = re.sub(r'[\s.-]', '', cpf)
        if not cpf.isdigit() or len(cpf) != 11:
            return None, "CPF deve ter 11 dígitos."
        if cpf in ['00000000000', '11111111111', '22222222222', '33333333333','44444444444', '55555555555', '66666666666', '77777777777','88888888888', '99999999999']:
            return None, "CPF inválido."
        for i in range(9, 11):
            soma = sum(int(cpf[num]) * (i + 1 - num) for num in range(0, i))
            digito = (soma * 10) % 11
            if digito == 10:
                digito = 0
            if str(digito) != cpf[i]:
                return None, "CPF inválido."
        return cpf, ''

    def tratar_senha(self, senha, confirm_senha):
        if not senha:
            return None, "Senha é obrigatória."
        if len(senha) < 6:
            return None, "Senha deve ter mais de 6 caracteres."
        if senha != confirm_senha:
            return None, "Senhas não coincidem."
        return senha, ''

    def mostrar_popup_erro(self, mensagem):
        popup = Popup(title='Erro',content=Label(text=mensagem),size_hint=(None, None), size=(400, 400))
        popup.open()

    def validar_dados(self, usuario, nome, email, telefone, cpf, senha, confirm_senha):
        self.usuario_tratado, self.erro_usuario = self.tratar_usuario(usuario)
        if self.erro_usuario:
            self.mostrar_popup_erro(self.erro_usuario)
            return False

        self.nome_tratado, self.erro_nome = self.tratar_nome(nome)
        if self.erro_nome:
            self.mostrar_popup_erro(self.erro_nome)
            return False

        self.email_tratado, self.erro_email = self.tratar_email(email)
        if self.erro_email:
            self.mostrar_popup_erro(self.erro_email)
            return False

        self.telefone_tratado, self.erro_telefone = self.tratar_telefone(telefone)
        if self.erro_telefone:
            self.mostrar_popup_erro(self.erro_telefone)
            return False

        self.cpf_tratado, self.erro_cpf = self.tratar_cpf(cpf)
        if self.erro_cpf:
            self.mostrar_popup_erro(self.erro_cpf)
            return False

        self.senha_tratada, self.erro_senha = self.tratar_senha(senha, confirm_senha)
        if self.erro_senha:
            self.mostrar_popup_erro(self.erro_senha)
            return False

        return True

    def cadastrar_usuario(self, usuario, nome, email, telefone, cpf, senha, confirm_senha):
        if not self.validar_dados(usuario, nome, email, telefone, cpf, senha, confirm_senha):
            return
        try:
            user_record = auth.create_user(
                email=self.email_tratado,
                password=self.senha_tratada
            )
            user_id = user_record.uid

            db = firestore.client()
            user_data = {
                "usuario": self.usuario_tratado,
                "nome": self.nome_tratado,
                "email": self.email_tratado,
                "telefone": self.telefone_tratado,
                "cpf": self.cpf_tratado,
                "senha": self.senha_tratada
            }
            db.collection("Usuarios").document(user_id).set(user_data)
            self.mostrar_popup_erro("Usuário cadastrado com sucesso.")
        except Exception as e:
            self.mostrar_popup_erro(f"Erro ao criar usuário no Firebase: {e}")

