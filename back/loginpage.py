import requests
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App


class LoginPage(Screen):
    def login(self, email_input, senha_input):
        email = email_input.text
        senha = senha_input.text

        url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?"
        api_key = "key=AIzaSyDi_cUuulZbBNfvVJfLfiRrOJrIBpK5vAE"
        api = url + api_key
        dados = {
            "email": email,
            "password": senha,
            "returnSecureToken": True
        }

        response = requests.post(api, json=dados)
        result = response.json()

        if response.status_code == 200:
            App.get_running_app().usuario_atual = result["localId"]
            self.manager.current = 'homepage'
        else:
            erro_mensagem = result.get("error", {}).get("message", "Erro desconhecido")
            self.mostrar_popup_erro(f"Falha no login: {erro_mensagem}")

    def mostrar_popup_erro(self, mensagem):
        popup = Popup(title='Erro', content=Label(text=mensagem), size_hint=(None, None), size=(400, 400))
        popup.open()
