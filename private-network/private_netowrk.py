from openai import OpenAI
from colorama import init
from colorama import Fore, Back, Style
from opik.integrations.openai import track_openai
import time
from opik import track
import os 
# create opik project name
os.environ["OPIK_PROJECT_NAME"] = "food_chatbot"

@track
def main():
    
    init()

    client = OpenAI(
        base_url="http://192.168.181.9:8950/v1",
        api_key="tom",
    )
    client = track_openai(client)

    prompts = [
        "Who are you?"
    ]


    for prompt in prompts:
        print(Fore.LIGHTMAGENTA_EX + prompt, end="\n")
        response = client.chat.completions.create(
            model="gamma-2-2b.gguf",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            stream=True,
            max_tokens=50,
        )
        words = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                words += chunk.choices[0].delta.content
                print(
                    Fore.LIGHTBLUE_EX + chunk.choices[0].delta.content,
                    end="",
                    flush=True,
                )
    return words

print(main())