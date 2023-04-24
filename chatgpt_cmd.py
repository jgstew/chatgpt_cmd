import cmd2
import os

import openai
import dotenv

class ChatGPT(cmd2.Cmd):
    prompt = 'ChatGPT> '

    def __init__(self):
        super().__init__()

        # remove built-in commands:
        del cmd2.Cmd.do_alias
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_macro
        del cmd2.Cmd.do_run_pyscript
        del cmd2.Cmd.do_run_script
        del cmd2.Cmd.do_set
        del cmd2.Cmd.do_shell
        del cmd2.Cmd.do_shortcuts

        # rename built-in commands:
        cmd2.Cmd.do_chat_history = cmd2.Cmd.do_history

        # remove built-in commands:
        del cmd2.Cmd.do_history

        # alias exit for quit
        self.do_exit = self.do_quit
        
        # load env vars from .env file
        dotenv.load_dotenv()
        # load api key from env
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def default(self, arg):
        """if unknown command, send full thing to chatgpt"""

        # check if input is a single word:
        if arg.strip() == "":
            self.perror(f"Unknown command `{arg.raw}`")
            self.pfeedback("NOTE: arbitrary text with more than one word will be sent to chatgpt automatically")
            self.pfeedback("Displaying help and list of commands:")
            self.do_help("-v")
        else:
            # more than one word entered:
            self.do_sendgpt(arg.raw)

    def do_sendgpt(self, arg):
        """Send a message to ChatGPT"""

        if not openai.api_key or openai.api_key.strip() == "":
            self.perror("No OPENAI_API_KEY environment variable found!")
            self.pfeedback("Use the set_api_key command to set the api key for this session")
            return True
        
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

        # output the response:
        self.poutput(result)

    def do_set_api_key(self, arg):
        """Set openapi key"""
        if arg and arg.strip() != "" and len(arg) > 8:
            openai.api_key = arg.strip()
        else:
            self.perror("Invalid API Key Entered!")

    def do_quit(self, arg):
        """Exit the program if arg empty"""
        if arg.strip() == "":
            self.poutput("Exiting ChatGPT...")
            return True
        else:
            self.do_sendgpt(arg.raw)

if __name__ == '__main__':
    ChatGPT().cmdloop()
