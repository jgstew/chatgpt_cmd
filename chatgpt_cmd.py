"""
A python CLI ChatGPT chatbot
"""
import datetime
import os
import re

import cmd2
import dotenv
import openai


class ChatGPT(cmd2.Cmd):
    """extends cmd2 which provides the interactivity"""

    prompt = "ChatGPT> "
    # set default chatgpt model:
    model = "gpt-4o"
    context_limit = 20  # Maximum number of messages to keep in context
    cached_models = None  # Class-level variable to cache models

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

        # Initialize context for conversation history
        self.context = []

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
    
    def cache_available_models(self):
        """Cache available models from OpenAI API"""
        if not self.cached_models:
            try:
                self.cached_models = [
                    item["id"]
                    for item in openai.Model.list()["data"]
                    if "gpt-" in item["id"] and "-preview" not in item["id"] and not re.search(r"\d{4}", item["id"])
                ]
            except Exception as e:
                self.perror(f"Error fetching models: {e}")

    def do_list_models(self, statement):
        """Print the list of OpenAI models"""

        if not self.cached_models:
            self.cache_available_models()

        # Display the cached models
        if statement != "do_not_display_models":
            for model_id in self.cached_models:
                self.pfeedback(model_id)

    def complete_select_model(self, text, line, begidx, endidx):
        """Define completion for apis."""

        # only initialize once
        if not self.cached_models:
            self.cache_available_models()

        # return the matching subset:
        return [name for name in self.cached_models if name.startswith(text)]

    def do_select_model(self, statement):
        """Select a model from the cached list of models"""
        if not self.cached_models:
            self.cache_available_models()

        model_name = statement.strip()
        if model_name in self.cached_models:
            self.model = model_name
            self.pfeedback(f"Model switched to: {model_name}")
        else:
            self.perror(f"Model '{model_name}' not found in cached models.")
            self.pfeedback("Use the 'list_models' command to view available models.")

    def do_sendgpt(self, statement):
        """Send a message to ChatGPT"""

        if not openai.api_key or openai.api_key.strip() == "":
            self.perror("No OPENAI_API_KEY environment variable found!")
            self.pfeedback(
                "Use the set_api_key command to set the api key for this session"
            )
            return True

        time_local = datetime.datetime.now(datetime.timezone.utc).astimezone()

        # Add user input to context
        self.context.append({"role": "user", "content": statement})

        # Trim context if it exceeds the limit
        if len(self.context) > self.context_limit:
            self.context.pop(0)

        # Prepare messages with context
        messages = [
            {
                "role": "system",
                "content": f"""You are a helpful assistant called ChatGPT_CMD.
                 You have all the capabilities of ChatGPT but you run as a command line interface.
                 Your responses should be informative and clear, but not excessively long. You have to help users quickly.
                 Today's date is {time_local.strftime("%d %B, %Y")} and the current time is {time_local.strftime("%H:%M %p")}.""",
            }
        ] + self.context

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
        )

        result = ""
        for choice in response.choices:
            result += choice.message.content

        # Add ChatGPT response to context
        self.context.append({"role": "assistant", "content": result})

        # Trim context if it exceeds the limit
        if len(self.context) > self.context_limit:
            self.context.pop(0)

        # Output the response:
        self.poutput(result)

    def do_clear_context(self, _=""):
        """Clear the conversation context"""
        self.context = []
        self.pfeedback("Conversation context cleared.")

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
            self.poutput("Exiting ChatGPT_CMD...")
            return True
        else:
            self.do_sendgpt(statement.raw)


if __name__ == "__main__":
    ChatGPT().cmdloop()
