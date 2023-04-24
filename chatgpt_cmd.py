import cmd2
import os

import openai
import dotenv

class ChatGPT(cmd2.Cmd):
    prompt = 'ChatGPT> '

    def __init__(self):
        super().__init__()

        # remove commands:
        del cmd2.Cmd.do_alias
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_macro
        del cmd2.Cmd.do_run_pyscript
        del cmd2.Cmd.do_run_script
        del cmd2.Cmd.do_set
        del cmd2.Cmd.do_shell
        del cmd2.Cmd.do_shortcuts

        # rename command:
        cmd2.Cmd.do_chat_history = cmd2.Cmd.do_history

        # remove history command:
        del cmd2.Cmd.do_history
        
        # load env vars from .env file
        dotenv.load_dotenv()
        # load api key from env
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
