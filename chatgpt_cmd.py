import cmd2
import os

import openai
import dotenv

class ChatGPT(cmd2.Cmd):
    prompt = 'chatgpt> '

    def __init__(self):
        super().__init__()
        dotenv.load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def do_sendgpt(self, arg):
        """Send a message to ChatGPT"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chatbot"},
                {"role": "user", "content": arg},
            ]
        )

        result = ''
        for choice in response.choices:
            result += choice.message.content

        self.poutput(result)

    def do_quit(self, arg):
        """Exit the program"""
        self.poutput("Exiting ChatGPT...")
        return True
    
    def do_exit(self, arg):
        """alias for quit"""
        self.do_quit(arg)
        return True
    
    def default(self, arg):
        """if unknown command, send full thing to chatgpt"""
        self.do_sendgpt(arg)

if __name__ == '__main__':
    ChatGPT().cmdloop()
