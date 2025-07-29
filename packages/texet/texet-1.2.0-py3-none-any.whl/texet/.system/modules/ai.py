from imports import *


class AI:
    ####################################################################################// Load
    def __init__(self, content: str):
        self.content = content
        self.extensions = self.__loadExtensions()
        self.characters = self.__loadCharacters()
        pass

    ####################################################################################// Main
    def response(key: str, task: str, returns: str):
        chat = [
            {
                "role": "system",
                "content": f"You are my assistant. You don't ask any questions. You must only return {returns} as requested.",
            },
            {
                "role": "user",
                "content": task,
            },
        ]

        try:
            cli.trace("Sending AI request ...")
            openai.api_key = key
            response = openai.ChatCompletion.create(model="gpt-4o", messages=chat)
        except openai.error.OpenAIError as e:
            cli.error(f"AI system error: {str(e)}")
            return ""
        except openai.error.RateLimitError as e:
            cli.error(f"AI rate limit error: {str(e)}")
            return ""
        except openai.error.InvalidRequestError as e:
            cli.error(f"AI invalid request error: {str(e)}")
            return ""
        except openai.error.AuthenticationError as e:
            cli.error(f"AI authentication error: {str(e)}")
            return ""
        except Exception as e:
            cli.error(f"Error: {str(e)}")
            return ""

        result = ""
        for choice in response.choices:
            result += choice.message.content

        return AI(result)

    def content(content: str):
        return AI(content)

    ####################################################################################// Actions
    def full(self):
        return self.content

    def text(self):
        content = self.code()
        if not content:
            return content

        cli.trace("Parsing text characters")
        for char in self.characters:
            content = content.replace(char, self.characters[char])

        return content

    def code(self):
        if not self.content:
            cli.trace("Empty AI response content!")
            return ""

        content = self.content
        cli.trace("Parsing code extensions")
        for replacer in self.extensions:
            content = content.replace("```" + replacer, "```")

        parse = content.split("```")
        n = 0
        collect = ""
        code = ""
        for index in range(len(parse)):
            if n == 0:
                collect += parse[index].replace("\n", " ")
                n = 1
            else:
                n = 0
                code += "\n\n" + parse[index]

        if len(str(code)) > 0:
            content = str(code)

        return content

    ####################################################################################// Helpers
    def __loadExtensions(self):
        file = os.path.dirname(os.path.dirname(__file__)) + "/sources/ext.yml"
        if not cli.isFile(file):
            cli.trace("Invalid extensions file: " + file)
            return []

        cli.trace("Reading extensions file")
        collect = set(cli.read(file).splitlines())

        return sorted(collect, key=len, reverse=True)

    def __loadCharacters(self):
        return {
            "—": "-",
            "“": '"',
            "”": '"',
            "‘": "'",
            "’": "'",
            "¯": "'",
            "ツ": "-",
            "ν": "v",
            "í": "i",
            ", and": " and",
            # "": "",
        }
