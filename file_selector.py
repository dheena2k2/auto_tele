from telethon import TelegramClient
import credentials  # contains api_id and api_hash
import os
import sys


client = TelegramClient('dheena', credentials.api_id, credentials.api_hash)


async def select_media(channel_name, destination, start_substring='', append=False):
    """
    Create or append pending.txt file which contains pending
    downloads
    :param channel_name: channel's unique name
    :param destination: destination/save directory path
    :param start_substring: substring that the start file name have
    :param append: whether to append to previous pending.txt
    :return: None
    """
    global client
    await client.connect()
    channel = await client.get_entity(channel_name)

    pending_file_path = os.path.join(destination, 'pending.txt')
    if os.path.exists(pending_file_path) and append:
        file = open(pending_file_path, 'a')
    else:
        file = open(pending_file_path, 'w')

    is_requested_message = False
    async for message in client.iter_messages(channel, reverse=True):
        if message.media:  # if media exists
            if message.file.name and start_substring in message.file.name and not is_requested_message:
                is_requested_message = True
            if is_requested_message:
                print('Confirm action (y/n/e) for:')  # options indicate yes, no and exit
                print(message.file.name)
                option = input()
                while option not in ['e', 'E', 'n', 'N', 'y', 'Y']:
                    option = input()
                if option == 'e' or option == 'E':
                    break
                if option == 'n' or option == 'N':
                    continue
                write_line = '%d %d\n' % (channel.id, message.id)  # write channel id and message id to file
                file.write(write_line)

    file.close()


def remove_file(destination):
    """
    Remove pending.txt file if it exists
    :param destination: destination/save directory path
    :return: None
    """
    pending_file_path = os.path.join(destination, 'pending.txt')
    if os.path.exists(pending_file_path):
        os.remove(pending_file_path)
    else:
        print('path "%s" does not exist' % pending_file_path)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise SyntaxError('Need at least 2 arguments')

    if sys.argv[1] not in ['n', 'a', 'c']:
        raise ValueError('First argument should be any of n, a or c')
    write_type = sys.argv[1]
    destination_dir = sys.argv[2]

    channel_id_name = ''
    if len(sys.argv) > 3:
        channel_id_name = sys.argv[3]

    common_str = ''
    if len(sys.argv) > 4:
        common_str = sys.argv[4]

    if write_type == 'c':
        remove_file(destination_dir)
    else:
        if write_type == 'n':
            to_append = False
        else:
            to_append = True
        client.loop.run_until_complete(
            select_media(channel_name=channel_id_name, destination=destination_dir, start_substring=common_str,
                         append=to_append))
