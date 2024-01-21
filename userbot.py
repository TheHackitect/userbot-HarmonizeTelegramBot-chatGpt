from art import *
from termcolor import colored  # Import the colored function
import json
import re
import datetime
import asyncio
import openai  # Import OpenAI library
from telethon.sync import TelegramClient, events
from colorama import Fore, init as color_ama



# Function to generate a customized ASCII logo
def generate_logo():
    # Set the text for the logo
    logo_text = '''TBOT'''

    # Use a different font and customize characters
    colorful_logo = text2art(logo_text, font='block', chr_ignore=True)
    colorful_logo = colorful_logo.replace('A', colored('A', 'green'))
    colorful_logo = colorful_logo.replace('D', colored('D', 'yellow'))
    colorful_logo = colorful_logo.replace('U', colored('U', 'cyan'))

    # Customize characters further
    colorful_logo = colorful_logo.replace('#', colored('█', 'blue'))  # Replace '#' with a filled block

    return colorful_logo


# Load settings from settings.json
with open('settings.json') as settings_file:
    settings = json.load(settings_file)


# Phone numbers source
phone_numbers = open('numbers.txt', 'r')
numbers = [phone_number.strip() for phone_number in phone_numbers.readlines()]
currentNumber = 0

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
    'engine': 'gpt-3.5-turbo-instruct',  # GPT-3.5 Turbo engine
    'temperature': 0.7,
    'max_tokens': 2000 #This model's maximum context length is 4097 tokens, however you requested 5136 tokens (136 in your prompt; 5000 for the completion). Please reduce your prompt; or completion length.
}

async def paraphrase_message(message_text):
    try:
        # Make a call to OpenAI to paraphrase the message
        response = openai.Completion.create(
            prompt=message_text,
            **openai_params
        )
        print(response)
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

async def join_main(phone_number):
    async def start(phone_number):
        phone_number = str(phone_number).strip()
        
        client = TelegramClient('session/' + phone_number, api_id, api_hash)
        await client.start(phone_number)
        me = await client.get_me()

        @client.on(events.NewMessage(incoming=True, chats=[source_channel]))
        async def handle_new_message(event):
            try:
                message = event.message
                message_text = message.raw_text

                # Paraphrase the message
                paraphrased_message = await paraphrase_message(message_text)
                if paraphrase_message == None or paraphrase_message == "":
                    dest_entity = await client.get_entity(dest_channel)
                    await client.send_message(dest_entity, paraphrased_message)
                    
                    # Send feedback about the action
                    feedback_text = f"Message Not Paraphrased\n\n Sent to:\n\n {dest_channel}:\n\n Message:\n\n{paraphrased_message}"
                    await send_feedback(client, feedback_text)
                else:
                    print("paraphrase_message", paraphrase_message)
                    # Forward the paraphrased message to the destination channel
                    dest_entity = await client.get_entity(dest_channel)
                    await client.send_message(dest_entity, paraphrased_message)

                    # Send feedback about the action
                    feedback_text = f"Message paraphrased and sent to {dest_channel}: {paraphrased_message}"
                    await send_feedback(client, feedback_text)
            except Exception as e:
                print(f"Error handling new message: {str(e)}")

        await client.run_until_disconnected()

    await start(phone_number)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    for phone_number in numbers:
        loop.create_task(join_main(phone_number))

    # Print the generated logo
    print(generate_logo())
    loop.run_forever()
