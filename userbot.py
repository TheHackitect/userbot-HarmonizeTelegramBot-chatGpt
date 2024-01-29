from art import *
from termcolor import colored
import json
import re
import datetime
import asyncio
import openai
from telethon.sync import TelegramClient, events
from colorama import init as color_ama
from bs4 import BeautifulSoup
import requests

# Function to generate a customized ASCII logo
def generate_logo():
    logo_text = '''TBOT'''
    colorful_logo = text2art(logo_text, font='block', chr_ignore=True)
    colorful_logo = colorful_logo.replace('A', colored('A', 'green'))
    colorful_logo = colorful_logo.replace('D', colored('D', 'yellow'))
    colorful_logo = colorful_logo.replace('U', colored('U', 'cyan'))
    colorful_logo = colorful_logo.replace('#', colored('█', 'blue'))
    return colorful_logo

# Load settings from settings.json
with open('settings.json') as settings_file:
    settings = json.load(settings_file)

# Phone numbers source
phone_numbers = open('numbers.txt', 'r')
numbers = [phone_number.strip() for phone_number in phone_numbers.readlines()]

api_id = settings["api_id"]
api_hash = settings["api_hash"]
session_name = settings["session_name"]
source_channel = settings["source_channel"]
dest_channel = settings["dest_channel"]
openai_api_key = settings["openai_api_key"]
feedback_account = settings["feedback_account"]

# Set OpenAI API key
openai.api_key = openai_api_key

# Set OpenAI parameters
openai_params = {
    'engine': 'gpt-3.5-turbo-instruct',
    'temperature': 0.7,
    'max_tokens': 2000
}

async def paraphrase_message(message_text):
    try:
        response = openai.Completion.create(
            prompt=message_text,
            **openai_params
        )
        paraphrased_text = response['choices'][0]['text']
        return paraphrased_text
    except Exception as e:
        print(f"Error in paraphrasing: {str(e)}")
        return None

async def send_feedback(client, feedback_text):
    try:
        feedback_entity = await client.get_entity(feedback_account)
        await client.send_message(feedback_entity, feedback_text)
    except Exception as e:
        print(f"Error sending feedback: {str(e)}")

async def handle_coin_tickers(message, coin_tickers):
    paraphrased_coin_tickers = await paraphrase_message(" ".join(coin_tickers))
    dest_entity = await client.get_entity(dest_channel)
    await client.send_message(dest_entity, paraphrased_coin_tickers)

async def handle_cointelegraph_links(client, dest_channel, cointelegraph_link):
    try:
        response = requests.get(cointelegraph_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        article_heading = soup.find('h1', class_='post__title').text.strip()
        article_content = "\n".join(p.text.strip() for p in soup.find_all('div', class_='post-content')[-1].find_all('p'))
        paraphrased_heading = await paraphrase_message(article_heading)
        paraphrased_content = await paraphrase_message(article_content)
        dest_entity = await client.get_entity(dest_channel)
        await client.send_message(dest_entity, f"{paraphrased_heading}\n\n{paraphrased_content}")
        feedback_text = f"Article from cointelegraph paraphrased and sent to {dest_channel}"
        await send_feedback(client, feedback_text)
    except Exception as e:
        print(f"Error handling cointelegraph link: {str(e)}")

async def handle_image_caption(message, dest_channel):
    paraphrased_caption = await paraphrase_message(message.caption)
    dest_entity = await client.get_entity(dest_channel)
    await client.send_file(dest_entity, message.media, caption=paraphrased_caption)

async def join_main(phone_number):
    async def start(phone_number):
        global client  # Declare client as a global variable
        phone_number = str(phone_number).strip()
        client = TelegramClient('session/' + phone_number, api_id, api_hash)
        await client.start(phone_number)
        me = await client.get_me()

        @client.on(events.NewMessage(incoming=True, chats=[source_channel]))
        async def handle_new_message(event):
            try:
                message = event.message
                message_text = message.raw_text
                sender_name = message.sender.first_name.lower() if message.sender else ""
        
                # Check if the message is from the user named "poe"
                if sender_name == "poe":
                    coin_tickers = re.findall(r'\$[A-Za-z0-9]+', message_text)
                    if coin_tickers:
                        await handle_coin_tickers(message, coin_tickers)

                    cointelegraph_links = re.findall(r'https://cointelegraph\.com/news/[\w-]+', message_text)
                    if cointelegraph_links:
                        await handle_cointelegraph_links(client, dest_channel, cointelegraph_links[0])

                    # Check if the message is an image with a caption
                    if message.media and hasattr(message, 'caption') and message.caption:
                        await handle_image_caption(message, dest_channel)

                    paraphrased_message = await paraphrase_message(message_text)
                    if paraphrased_message is None or paraphrased_message == "":
                        dest_entity = await client.get_entity(dest_channel)
                        await client.send_message(dest_entity, paraphrased_message)
                        feedback_text = f"Message Not Paraphrased\n\n Sent to:\n\n {dest_channel}:\n\n Message:\n\n{paraphrased_message}"
                        await send_feedback(client, feedback_text)
                    else:
                        dest_entity = await client.get_entity(dest_channel)
                        await client.send_message(dest_entity, paraphrased_message)
                        feedback_text = f"Message paraphrased and sent to {dest_channel}: {paraphrased_message}"
                        await send_feedback(client, feedback_text)
                else:
                    pass
            except Exception as e:
                print(f"Error handling new message: {str(e)}")

        await client.run_until_disconnected()

    await start(phone_number)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    for phone_number in numbers:
        loop.create_task(join_main(phone_number))

    print(generate_logo())
    loop.run_forever()
