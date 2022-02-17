from telethon import TelegramClient
import credentials  # contains api_id and api_hash
import os
from helper import ProgressBar
import sys


client = TelegramClient('dheena', credentials.api_id, credentials.api_hash)


async def download_media(destination):
    """
    Download pending file using pending.txt
    :param destination: destination/save directory path
    :return: None
    """
    global client
    await client.connect()

    pending_file_path = os.path.join(destination, 'pending.txt')
    with open(pending_file_path, 'r') as file:
        messages_info = file.readlines()

    prev_channel_id = None
    channel = None
    while len(messages_info) > 0:
        message_info, messages_info = messages_info[0], messages_info[1:]
        channel_id, message_id = message_info[:-1].split()
        message_id = int(message_id)

        if channel_id != prev_channel_id:
            channel = await client.get_entity(channel_id)
            prev_channel_id = channel_id

        message = await client.get_messages(channel, ids=message_id)
        print('Downloading:', message.file.name)
        p_bar = ProgressBar(unit='B', unit_scale=True, unit_divisor=1024)
        await client.download_media(message.media, file=destination, progress_callback=p_bar.new_update)
        p_bar.close()
        del p_bar

        with open(pending_file_path, 'w') as file:
            file.writelines(messages_info)

    print('Download Complete')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SyntaxError('Need destination directory name as argument')

    destination_dir = sys.argv[1]
    client.loop.run_until_complete(download_media(destination_dir))
