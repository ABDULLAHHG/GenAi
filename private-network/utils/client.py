from openai import OpenAI
from opik.integrations.openai import track_openai
from colorama import init, Fore

def connect_to_client():
    try:
        client = track_openai(OpenAI(
            base_url="http://192.168.1.194:8950/v1",
            api_key="tom",
        ))
        return client
    except Exception as e:
        print(Fore.RED + f"\nAn error occurred: {str(e)}")