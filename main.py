import sys
import json
import random
from pyrogram import Client
import time
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.api_id = your_api_id
        self.api_hash = "your_api_hash"
        self.apps = Client(
            "Sessions/",
            int(self.api_id),
            self.api_hash,
            phone_number="your_phone_number",
        )
        self.apps.start()

        self.link_label = QtWidgets.QLabel("Link do grupo", self)
        self.link_input = QtWidgets.QLineEdit(self)
        self.link_input.setPlaceholderText("Insira o link ou @ do canal/grupo")
        self.num_label = QtWidgets.QLabel("Quantidade de usuarios", self)
        self.num_input = QtWidgets.QLineEdit(self)
        self.num_input.setPlaceholderText("Insira a quantidade de usuarios")
        self.time_label = QtWidgets.QLabel("Tempo de pausa entre as ações", self)
        self.time_input = QtWidgets.QLineEdit(self)
        self.time_input.setPlaceholderText("Insira o tempo de pausa entre as ações")
        self.message_label = QtWidgets.QLabel("Mensagem a ser enviada", self)
        self.message_input = QtWidgets.QTextEdit(self)
        self.message_input.setPlaceholderText("Insira a mensagem a ser enviada")
        self.message_input.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.message_input.setMinimumSize(QtCore.QSize(100, 300))
        self.img_label = QtWidgets.QLabel("Imagem a ser enviada", self)
        self.img_input = QtWidgets.QLineEdit(self)
        self.img_input.setPlaceholderText("Insira o caminho da imagem a ser enviada")
        self.send_button = QtWidgets.QPushButton("Enviar mensagem", self)
        self.send_button.clicked.connect(self.send_messages)
        self.send_button.setMinimumSize(QtCore.QSize(200, 50))
        self.send_image_caption = QtWidgets.QPushButton("Enviar imagem com legenda", self)
        self.send_image_caption.clicked.connect(self.send_image_with_caption)
        self.send_image_caption.setMinimumSize(QtCore.QSize(200, 50))
        self.clear_button = QtWidgets.QPushButton("Apagar banco de dados", self)
        self.clear_button.clicked.connect(self.clear_sent_messages)
        self.clear_button.setMinimumSize(QtCore.QSize(200, 50))

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.link_label, 0, 0)
        layout.addWidget(self.link_input, 0, 1)
        layout.addWidget(self.num_label, 1, 0)
        layout.addWidget(self.num_input, 1, 1)
        layout.addWidget(self.time_label, 2, 0)
        layout.addWidget(self.time_input, 2, 1)
        layout.addWidget(self.message_label, 3, 0)
        layout.addWidget(self.message_input, 3, 1)
        layout.addWidget(self.img_label, 4, 0)
        layout.addWidget(self.img_input, 4, 1)
        layout.addWidget(self.send_button, 5, 0, 1, 2)
        layout.addWidget(self.send_image_caption, 6, 0, 1, 2)
        layout.addWidget(self.clear_button, 7, 0, 1, 2)

        self.setLayout(layout)
        self.setGeometry(600, 600, 600, 150)
        self.setWindowTitle('Robô Mensageiro em Massa ')
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.show()

    def send_messages(self):
        print("Iniciando envio de mensagens...")
        group_link = self.link_input.text()
        chat_id = self.apps.get_chat(group_link).id
        members = list(self.apps.get_chat_members(chat_id))
        random.shuffle(members)

        try:
            with open("sent_messages.json", "r") as f:
                sent_messages = json.load(f)
        except FileNotFoundError:
            sent_messages = []

        num_users = int(self.num_input.text()) + len(sent_messages)
        time_message = int(self.time_input.text())
        send_message = self.message_input.toPlainText()
        image_path = self.img_input.text()

        for i, member in enumerate(members):
            if i >= num_users:
                break

            user_id = member.user.id
            if user_id not in sent_messages:
                user_name = member.user.first_name
                message_text = send_message
                try:
                    if send_message and image_path:
                        time.sleep(2)
                        self.apps.send_photo(user_id, image_path)
                        time.sleep(8)
                        self.apps.send_message(user_id, message_text)
                    elif send_message:
                        self.apps.send_message(user_id, message_text)
                    elif image_path:
                        self.apps.send_photo(user_id, image_path)
                except:
                    continue

                sent_messages.append(user_id)
                with open("sent_messages.json", "w") as f:
                    json.dump(sent_messages, f)
                print(f"Usuario {user_name} ({user_id}) adicionado ao banco de dados ")
                print(f"Mensagem enviada para {user_name} ({user_id})")
                print(f"Total de mensagens enviadas: {len(sent_messages)}")
                print("Usuários restantes: ", num_users - len(sent_messages))
                time.sleep(time_message)

        print("Mensagens enviadas!")

    def send_image_with_caption(self):
        print("Iniciando envio de imagens com legenda...")
        group_link = self.link_input.text()
        chat_id = self.apps.get_chat(group_link).id
        members = list(self.apps.get_chat_members(chat_id))
        random.shuffle(members)

        try:
            with open("sent_messages.json", "r") as f:
                sent_messages = json.load(f)
        except FileNotFoundError:
            sent_messages = []

        num_users = int(self.num_input.text()) + len(sent_messages)
        time_message = int(self.time_input.text())
        send_message = self.message_input.text()
        image_path = self.img_input.text()

        for i, member in enumerate(members):
            if i >= num_users:
                break

            user_id = member.user.id
            if user_id not in sent_messages:
                user_name = member.user.first_name
                message_text = send_message
                try:
                    if image_path:
                        self.apps.send_photo(user_id, image_path, caption=message_text)
                except:
                    continue

                sent_messages.append(user_id)
                with open("sent_messages.json", "w") as f:
                    json.dump(sent_messages, f)
                time.sleep(time_message)

        print("Mensagens enviadas!")

    def clear_sent_messages(self):
        try:
            with open("sent_messages.json", "w") as f:
                json.dump([], f)
            print("Banco de dados apagado com sucesso!")
        except Exception as e:
            print("Erro ao apagar Banco de Dados:", e)

if __name__ == '__main__':
    font = QtGui.QFont("Arial", 10)
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("assets/robo.png"))
    app.setStyle("Fusion")
    app.setStyleSheet("QWidget { background-color: #333; color: #fff; }")
    app.setFont(font)
    ex = App()
    sys.exit(app.exec_())


