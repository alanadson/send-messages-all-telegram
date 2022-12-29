# Send Messages All Telegram

This is a Python script for sending messages to users in a Telegram group. The script uses the pyrogram library to connect to the Telegram API and perform message sending operations.

## Requirements

In order to run the script, you will need to have Python 3 installed on your machine and install the following libraries:

```bash
pip install pyrogram
```

```bash
pip install TgCrypto
```

```bash
pip install PyQt5
```

## Configuration

Before running the script, you will need to provide your API ID and API hash to access the Telegram API. You will also need to provide the phone number associated with your Telegram account.

To obtain your API ID and API hash, you will need to create an app in the [Telegram Developer Dashboard](https://my.telegram.org/auth).

## Usage

To use the script, simply run it with Python:

```bash
python main.py
```

The script will display the following options:

1.Send messages
2.Clear database
3.Exit
To send messages, simply select option 1 and follow the instructions in the terminal. The script will ask for the group link, the number of users to send messages to, the time interval between each message, and the message to be sent. The script will then send the messages and store the IDs of the users it has already sent messages to in a sent_messages.json file.

If you wish to clear the database, simply select option 2. This will clear the sent_messages.json file and allow you to send messages to the same users again.

To exit the script, simply select option 3.
