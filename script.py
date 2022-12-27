import json
from pyrogram import Client
import time

api_id = your_id
api_hash = "your_hash"
apps = Client("Sessions/", int(api_id), str(api_hash), phone_number="your_phone")
apps.start()

while True:
    print("\n1. Send messages")
    print("2. Clear database")
    print("3. Exit")
    action = int(input("Choose an option: "))

    if action == 1:
        group_link = input("Insert the group link: ")
        chat_id = apps.get_chat(group_link).id
        members = apps.get_chat_members(chat_id)

        try:
            with open("sent_messages.json", "r") as f:
                sent_messages = json.load(f)
        except FileNotFoundError:
            sent_messages = []

        num_users = int(input("How many users do you want to send a message to:  "))
        num_users = num_users + len(sent_messages)
        time_message = int(input("How many seconds between each message: "))
        send_message = input(f"What message do you want to send: ")
        for i, member in enumerate(members):
            if i >= num_users:
                break

            user_id = member.user.id
            if user_id not in sent_messages:
                user_name = member.user.first_name
                message_text = send_message
                apps.send_message(user_id, message_text)
                apps.send_photo(chat_id=user_id, photo="image.jpg", caption=message_text)
                time.sleep(time_message)

                sent_messages.append(user_id)
        print("Messages sent!")
        with open("sent_messages.json", "w") as f:
            json.dump(sent_messages, f)
    elif action == 2:
        with open("sent_messages.json", "w") as f:
            json.dump([], f)
        print("Database cleared")
    elif action == 3:
        break

apps.stop()
