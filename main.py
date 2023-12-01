from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from back.homepage import HomePage
from back.loginpage import LoginPage
from back.cadastro import CadastroPage
from back.clientes import ClientesPage
from back.financeiro import FinanceiroPage
from back.fornecedores import FornecedoresPage
import firebase_admin
from firebase_admin import credentials, firestore



Builder.load_file(r'front/login.kv')
Builder.load_file(r'front/home.kv')
Builder.load_file(r'front/fornecedores.kv')
Builder.load_file(r'front/cadastro.kv')
Builder.load_file(r'front/clientes.kv')
Builder.load_file(r'front/financeiro.kv')


class MainApp(App):
    usuario_atual = None
    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(LoginPage(name='loginpage'))
        self.screen_manager.add_widget(CadastroPage(name="cadastropage"))
        self.screen_manager.add_widget(HomePage(name='homepage'))
        self.screen_manager.add_widget(FornecedoresPage(name='fornecedorespage'))
        self.screen_manager.add_widget(FinanceiroPage(name='financeiropage'))
        self.screen_manager.add_widget(ClientesPage(name='clientespage'))
        self.inicializar_firebase()
        return self.screen_manager

    def inicializar_firebase(self):
        try:
            firebase_admin.get_app()
        except ValueError:
            certificado = credentials.Certificate("projetoafya-firebase-adminsdk-th8n9-37ed0b0337.json")
            firebase_admin.initialize_app(certificado)

    def mudar_tela(self, tela_id):
        self.screen_manager.current = tela_id


if __name__ == '__main__':
    MainApp().run()