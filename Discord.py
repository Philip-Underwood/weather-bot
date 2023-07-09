import os
import requests
import json

DiscordEnabled = True
webhook_url = os.getenv('DISCORD_WEBHOOK')


def Discord(content):
    if DiscordEnabled:
        # Create a formatted message
        data = {
            "content": content
        }

        # Convert the dictionary to a JSON object
        json_data = json.dumps(data)

        # Send the message

        response = requests.post(
            webhook_url,
            data=json_data,
            headers={'Content-Type': 'application/json'}
        )

        # If the response was not successful, raise an exception
        if response.status_code != 204:
            raise ValueError(
                f'Request returned an error {response.status_code}, '
                f'the response is:\n{response.text}'
            )
