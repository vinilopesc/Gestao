from kivy.uix.screenmanager import Screen
import mysql.connector
import os


db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Abclopes1512vini!",
    database="sistema_login"
)
db_cursor = db_connection.cursor()


class LoginPage(Screen):
    def login(self):
        username = self.ids.user_input.text
        password = self.ids.password_input.text


