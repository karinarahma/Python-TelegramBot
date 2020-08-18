import requests
import telebot

class BotHandler:
    def __init__(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)
    #url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update


token = '13408XXXXX:AAFWcvmmYLT86IXrTqfwI4ZwzFhtEPmBMFk' #Token of your bot
karina_bot = BotHandler(token) #Your bot's name
karina_telebot = telebot.TeleBot(token)


def main():
    new_offset = 0
    print('hi, now launching...')

    while True:
        all_updates=karina_bot.get_updates(new_offset)
        doc = open('demo.docx', 'rb')
        pic = 'https://github.com/python-telegram-bot/python-telegram-bot/blob/master/tests/data/telegram.png'

        if len(all_updates) > 0:
            for current_update in all_updates:
                print(current_update)
                first_update_id = current_update['update_id']
                if 'text' not in current_update['message']:
                    first_chat_text='New member'
                else:
                    first_chat_text = current_update['message']['text']
                first_chat_id = current_update['message']['chat']['id']
                if 'first_name' in current_update['message']:
                    first_chat_name = current_update['message']['chat']['first_name']
                elif 'new_chat_member' in current_update['message']:
                    first_chat_name = current_update['message']['new_chat_member']['username']
                elif 'from' in current_update['message']:
                    first_chat_name = current_update['message']['from']['first_name']
                else:
                    first_chat_name = "unknown"
            
                if first_chat_text.lower() == "/start":
                    karina_bot.send_message(first_chat_id, "Welcome to Karina's bot. Say hi/hello to me!")
                    new_offset = first_update_id + 1
                elif first_chat_text.lower().__contains__('hi') or  first_chat_text.lower().__contains__('hello'):
                    karina_bot.send_message(first_chat_id, 'Hello ' + first_chat_name + '!' + ' How are you?')
                    new_offset = first_update_id + 1
                elif first_chat_text.lower().__contains__('bad') or first_chat_text.lower().__contains__('not good') or first_chat_text.lower().__contains__('not okay'):
                    karina_bot.send_message(first_chat_id, "It's okay! Keep smiling and have a nice day " + ' :)')
                    new_offset = first_update_id + 1
                elif first_chat_text.lower().__contains__('fine') or  first_chat_text.lower().__contains__('good') or first_chat_text.lower().__contains__('okay'):
                    karina_bot.send_message(first_chat_id, 'Great! Have a nice day ' + first_chat_name + ' :)')
                    new_offset = first_update_id + 1
                elif first_chat_text.lower().__contains__('thank'):
                    karina_bot.send_message(first_chat_id, 'Anytime :)')
                    new_offset = first_update_id + 1
                elif first_chat_text.lower().__contains__('bye'):
                    karina_bot.send_message(first_chat_id, 'See you ' + first_chat_name + '. Nice to talk to you!')
                    new_offset = first_update_id + 1
                elif first_chat_text.lower() == "the document":
                    karina_bot.send_message(first_chat_id, 'Please wait..')
                    karina_telebot.send_document(first_chat_id, doc)
                    new_offset = first_update_id + 1
                elif first_chat_text.lower() == "the picture":
                    karina_telebot.send_photo(first_chat_id, pic)
                    new_offset = first_update_id + 1
                else:
                    karina_bot.send_message(first_chat_id, 'Sorry not understand what you type :( just say hi/hello to me!')
                    new_offset = first_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
