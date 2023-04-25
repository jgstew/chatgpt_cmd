# chatgpt_cmd
a python cmd2 chatgpt chatbot

currently does not send previous prompt and response to keep the conversation going.

## Provide your OpenAI API Key:

### use .env file:

put your `OPENAI_API_KEY` in a `.env` file in the same folder as `chatgpt_cmd.py` like:

```
OPENAI_API_KEY=your-key-goes-here
```

### use environment variable:

You can store `OPENAI_API_KEY` as an environment variable and it will be used.

### use single session only command:

Use `set_api_key` command in interactive CLI to set an API key for use only during the current session.

## Example Usage:

Example usage with non-interactive CLI: `python ./chatgpt_cmd.py "how long until newyears" exit`

```
As today's date is 24 April, 2023, there are 8 months and 7 days until the next new year's eve, which is on 31 December, 2023.
Exiting ChatGPT_CMD...
```

Example usage with interactive CLI: `python ./chatgpt_cmd.py`

```
ChatGPT> write a poem about using chatgpt on the command line
Using ChatGPT on the command line,
Is a marvel of modern time,
With questions asked and answers found,
The exchange of knowledge does astound.
Type away, and see what comes,
From this digital oracle, never once glum,
A source of wisdom, always on hand,
A guide to help you understand.

Though not as fancy as its GUI kin,
Using ChatGPT on the command line is no sin,
No flashy colors or designs to see,
But it gets the job done perfectly.

So ask away, and have no fear,
ChatGPT on the command line is near,
With answers quick and knowledge sound,
There’s no limit to what we can be found.
ChatGPT> exit
Exiting ChatGPT_CMD...
```
