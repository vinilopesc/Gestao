from kivy.uix.screenmanager import Screen
import mysql.connector
from mysql.connector import Error
import logging
from kivy.properties import StringProperty
import re


db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Abclopes1512vini!",
    database="sistema_login"
)
db_cursor = db_connection.cursor()

class CadastroPage(Screen):
    erro_mensagem = StringProperty('')
    erro_usuario = StringProperty('')
    erro_nome = StringProperty('')
    erro_email = StringProperty('')
    erro_telefone = StringProperty('')
    erro_cpf = StringProperty('')
    erro_cep = StringProperty('')
    erro_num_casa = StringProperty('')
    erro_senha = StringProperty('')
    largura_caixa_texto = 0.35
    altura_caixa_texto = 0.05
    altura_btn = 0.05
    largura_btn = 0.15
    altura_label = 0.2
    largura_label = 0.2

    def tratar_nome(self, nome):
        if not isinstance(nome,str):
            return "Digite apenas letras"
        if nome == "":
            return "Nome é obrigatorio"
        if len(nome) > 20:
            return "Limite de 20 caracteres."
        return None

    def tratar_email(self, email):
        if not email:
            return "Email é obrigatório."
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$'
        if not re.fullmatch(email_regex, email):
            return "Formato de email inválido."
        return None

    def tratar_usuario(self, usuario):
        if not usuario:
            return "Nome de usuário é obrigatório."
        min_length = 4
        max_length = 20
        if len(usuario) < min_length or len(usuario) > max_length:
            return f"Nome de usuário deve ter entre {min_length} e {max_length} caracteres."
        if not re.match(r'^\w+$', usuario):
            return "Nome de usuário pode conter apenas letras, números e underscores."
        return None

    def tratar_telefone(self, telefone):
        if not telefone:
            return "Número de telefone é obrigatório."
        telefone_limpo = re.sub(r'[^0-9]', '', telefone)
        if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
            return "Número de telefone (com DDD) deve ter 10 ou 11 dígitos."
        return None

    def tratar_cep(self, cep):
        if not cep:
            return "CEP é obrigatório."
        cep_limpo = re.sub(r'[\s-]', '', cep)
        if not cep_limpo.isdigit() or len(cep_limpo) != 8:
            return "Formato de CEP inválido."
        return None

    def validar_cpf(self, cpf):
        if not cpf.isdigit() or len(cpf) != 11:
            return "CPF deve ter 11 dígitos."
        if cpf in ['00000000000', '11111111111', '22222222222', '33333333333',
                   '44444444444', '55555555555', '66666666666', '77777777777',
                   '88888888888', '99999999999']:
            return "CPF inválido."
        for i in range(9, 11):
            soma = sum(int(cpf[num]) * (i + 1 - num) for num in range(0, i))
            digito = (soma * 10) % 11
            if digito == 10:
                digito = 0
            if str(digito) != cpf[i]:
                return "CPF inválido."
        return None

    def validar_num_casa(self, num_casa):
        if not num_casa:
            return "Número da casa é obrigatório."
        if not re.match(r'^\d+[A-Za-z]*$', num_casa):
            return "Número da casa inválido."
        return None

    def validar_senha(self, senha, confirm_senha):
        if not senha:
            return "Senha é obrigatória."
        if len(senha) < 8 or len(senha) > 20:
            return "Senha deve ter entre 8 e 20 caracteres."
        if senha != confirm_senha:
            return "Senhas não coincidem."
        return None

    def registrar_usuario(self, usuario, nome, email, telefone, cpf, cep, num_casa, senha, confirm_senha):
        self.erro_usuario = self.erro_nome = self.erro_email = self.erro_telefone = ''
        self.erro_cpf = self.erro_cep = self.erro_num_casa = self.erro_senha = ''
        erro_usuario = self.tratar_usuario(usuario)
        erro_nome = self.tratar_nome(nome)
        erro_email = self.tratar_email(email)
        erro_telefone = self.tratar_telefone(telefone)
        erro_cpf = self.validar_cpf(cpf)
        erro_cep = self.tratar_cep(cep)
        erro_num_casa = self.validar_num_casa(num_casa)
        erro_senha = self.validar_senha(senha, confirm_senha)
        if any([erro_usuario, erro_nome, erro_email, erro_telefone, erro_cpf, erro_cep, erro_num_casa, erro_senha]):
            self.erro_usuario = erro_usuario or ''
            self.erro_nome = erro_nome or ''
            self.erro_email = erro_email or ''
            self.erro_telefone = erro_telefone or ''
            self.erro_cpf = erro_cpf or ''
            self.erro_cep = erro_cep or ''
            self.erro_num_casa = erro_num_casa or ''
            self.erro_senha = erro_senha or ''
            return
        try:
            connection = mysql.connector.connect(host='localhost', database='sistema_login', user='root',
                                                 password='Abclopes1512vini!')
            cursor = connection.cursor()
            query = "INSERT INTO clientes (usuario, nome, email, telefone, cpf, cep, num_casa, senha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (usuario, nome, email, telefone, cpf, cep, num_casa, senha))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Erro ao registrar usuário: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
