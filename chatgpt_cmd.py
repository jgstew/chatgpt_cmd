"""
A python CLI ChatGPT chatbot
"""
import os

import cmd2
import dotenv
import openai


class ChatGPT(cmd2.Cmd):
    """extends cmd2 which provides the interactivity"""

    prompt = "ChatGPT> "

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
        cmd2.Cmd.do_command_history = cmd2.Cmd.do_history

        # remove built-in commands:
        del cmd2.Cmd.do_history

        # alias exit for quit
        self.do_exit = self.do_quit

        # load env vars from .env file
        dotenv.load_dotenv()
        # load api key from env
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def default(self, statement):
        """if unknown command, send full thing to chatgpt"""

        # save entered item to history:
        self.history.append(statement)

        # check if input is a single word:
        if statement.strip() == "":
            self.perror(f"Unknown command `{statement.raw}`")
            self.pfeedback(
                "NOTE: arbitrary text with more than one word will be sent to chatgpt automatically"
            )
            self.pfeedback("Displaying help and list of commands:")
            self.do_help("-v")
        else:
            # more than one word entered:
            self.do_sendgpt(statement.raw)

    def do_sendgpt(self, statement):
        """Send a message to ChatGPT"""

        if not openai.api_key or openai.api_key.strip() == "":
            self.perror("No OPENAI_API_KEY environment variable found!")
            self.pfeedback(
                "Use the set_api_key command to set the api key for this session"
            )
            return True

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chatbot"},
                {"role": "user", "content": statement},
            ],
        )

        result = ""
        for choice in response.choices:
            result += choice.message.content

        # output the response:
        self.poutput(result)

    def do_set_api_key(self, statement):
        """Set openai api key for current session only"""
        if (
            statement
            and statement.strip() != ""
            and len(statement) > 8
            and " " not in statement.strip()
        ):
            openai.api_key = statement.strip()
        else:
            self.perror("Invalid API Key Entered!")

    def do_save_api_key(self, statement):
        """save openai api key to .env file"""

        if (
            statement
            and statement.strip() != ""
            and len(statement) > 8
            and " " not in statement.strip()
        ):
            openai.api_key = statement.strip()

        if (
            openai.api_key
            and openai.api_key.strip() != ""
            and len(openai.api_key) > 8
            and " " not in openai.api_key
        ):
            # quote_mode: always or auto or never
            dotenv.set_key(".env", "OPENAI_API_KEY", openai.api_key, quote_mode="never")

    def do_quit(self, statement):
        """Exit the program if arg empty"""
        if statement.strip() == "":
            self.poutput("Exiting ChatGPT...")
            return True
        else:
            self.do_sendgpt(statement.raw)


if __name__ == "__main__":
    ChatGPT().cmdloop()
