# HarmonizeTelegramBot

Welcome to **HarmonizeTelegramBot** – Your Personal Harmony Guardian!

![Bot in Action](link-to-your-image)

## Overview

HarmonizeTelegramBot is a nifty Python script powered by the Telethon library, designed to bring harmony to your Telegram channels by filtering and forwarding messages based on customizable parameters. Whether you're keeping an eye on cryptocurrency metrics or monitoring specific alerts, this bot has you covered.

## Features

- Real-time message monitoring in your private channels.
- Customizable parameters for forwarding messages to specific channels.
- Smart filtering based on Market Cap (MC), Token Liquidity (Liq), SOL value, and more.
- Swift and responsive message forwarding, ensuring timely alerts.

## Getting Started

### Prerequisites

To get started, ensure you have the following:

- Python 3.7 or higher
- Telethon library

### Installation


## Obtaining api_id
In order to obtain an API id and develop your own application using the Telegram API you need to do the following:

- Sign up for Telegram using any application.

- Log in to your Telegram core: https://my.telegram.org.

- Go to "API development tools" and fill out the form.

- You will get basic addresses as well as the api_id and api_hash parameters required for user authorization.
For the moment each number can only have one api_id connected to it.
We will be sending important developer notifications to the phone number that you use in this process, so please use an up-to-date number connected to your active Telegram account.

- Put the Hash and the ID you get in the settings.json file where they are meant to be

- Put your phone number in the numbers.txt file (Onr line only! ) No white spaces, No new lines/empty lines!


Change into the project directory: (in the terminal eg vscode)

```bash
cd filterbot
```

Create a virtual enviroment to keep your installations

```bash
python -m venv venv
```

Activate the virtual enviroment

```bash
./venv/scripts/activate.ps1
```
Install dependencies:

```bash
pip install -r requirements.txt
```
Run the bot:

```bash
python userbot.py
```

## Usage
Customize your bots behavior by tweaking the settings.json file. Run the bot and let it keep your channels harmonized and informed!

## Configuration
Edit the settings.json file to adjust parameters such as MC values, SOL triggers, and more. Tailor the bot to your specific needs effortlessly.

Contributing
If you'd like to contribute, please see the CONTRIBUTING.md file.

## License
This project is licensed under the MIT License – see the LICENSE file for details.

HarmonizeTelegramBot – Striving for Harmony in Your Telegram Channels. 🌐🤖✨


Feel free to replace the placeholder image link (`link-to-your-image`) with an actual image link that showcases your bot in action or any relevant visual representation. Adjust the text further based on your preferences and project details.





