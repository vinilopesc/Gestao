from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from back.homepage import HomePage
from back.loginpage import LoginPage
from back.cadastro import CadastroPage


Builder.load_file(r'front/login.kv')
Builder.load_file(r'front/home.kv')
Builder.load_file(r'front/cadastro.kv')


class MainApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(LoginPage(name='loginpage'))
        self.screen_manager.add_widget(HomePage(name='homepage'))
        self.screen_manager.add_widget(CadastroPage(name="cadastropage"))
        return self.screen_manager

    def mudar_tela(self, tela_id):
        self.screen_manager.current = tela_id


if __name__ == '__main__':
    MainApp().run()