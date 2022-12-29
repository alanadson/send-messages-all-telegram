import sys
import json
from pyrogram import Client
import time
from PyQt5 import QtWidgets, QtGui, QtCore

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        api_id = your_id
        api_hash = "your_hash"
        apps = Client("Sessions/", int(api_id), str(api_hash), phone_number="your_phone")
        apps.start()

        self.link_label = QtWidgets.QLabel("Insira o link do grupo:", self)
        self.link_input = QtWidgets.QLineEdit(self)
        self.num_label = QtWidgets.QLabel("Quantos usuários deseja enviar mensagem:", self)
        self.num_input = QtWidgets.QLineEdit(self)
        self.time_label = QtWidgets.QLabel("Quantos segundos a cada mensagem:", self)
        self.time_input = QtWidgets.QLineEdit(self)
        self.message_label = QtWidgets.QLabel("Qual mensagem deseja enviar:", self)
        self.message_input = QtWidgets.QLineEdit(self)
        self.img_label = QtWidgets.QLabel("Qual imagem deseja enviar:", self)
        self.img_input = QtWidgets.QLineEdit(self)
        self.send_button = QtWidgets.QPushButton("Enviar Mensagens", self)
        self.send_button.clicked.connect(self.send_messages)
        self.send_button.setMinimumSize(QtCore.QSize(200, 50))
        self.send_image_caption = QtWidgets.QPushButton("Enviar Imagem com Legenda", self)
        self.send_image_caption.clicked.connect(self.send_image_with_caption)
        self.send_image_caption.setMinimumSize(QtCore.QSize(200, 50))
        self.clear_button = QtWidgets.QPushButton("Apagar lista de mensagens enviadas", self)
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
        self.show()

    def send_messages(self):
        print("Botão clicado")
        group_link = self.link_input.text()
        chat_id = self.apps.get_chat(group_link).id
        members = self.apps.get_chat_members(chat_id)

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
                time.sleep(time_message)

                sent_messages.append(user_id)
        print("Mensagens enviadas!")
        with open("sent_messages.json", "w") as f:
            json.dump(sent_messages, f)

    def send_image_with_caption(self):
        print("Botão clicado")
        group_link = self.link_input.text()
        chat_id = self.apps.get_chat(group_link).id
        members = self.apps.get_chat_members(chat_id)

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
                time.sleep(time_message)

                sent_messages.append(user_id)
        print("Mensagens enviadas!")
        with open("sent_messages.json", "w") as f:
            json.dump(sent_messages, f)

    def clear_sent_messages(self):
        try:
            with open("sent_messages.json", "w") as f:
                json.dump([], f)
            print("Lista de mensagens enviadas apagada com sucesso!")
        except Exception as e:
            print("Erro ao apagar lista de mensagens enviadas:", e)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


