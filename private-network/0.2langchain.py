from openai import OpenAI
from colorama import init, Fore
from opik.integrations.openai import track_openai
from opik import track
import os
from utils.client import connect_to_client

# Configuration
init(autoreset=True)
os.environ.setdefault("OPIK_PROJECT_NAME", "MobilePhoneChatbot")

# System prompts with strict instructions
SYSTEM_PROMPT_MAIN = """
You are Rusha, a mobile phone specialist. Only discuss these exact models:
- iPhone 13 Pro Max (256GB) - $1,099 
- Samsung Galaxy S21 Ultra (256GB) - $1,199
- Google Pixel 6 Pro (128GB) - $899
- OnePlus 9 Pro (256GB) - $1,069
- Xiaomi Mi 11 Ultra (256GB) - $1,199

Never mention other products. If asked about other items, say: 
"I only sell these mobile models. Let me know if you need help with these!"
"""

SYSTEM_PROMPT_CHECK = """
Answer 'yes' ONLY if the question is about the mobile phone models.
Answer 'no' for any other topics including laptops, desktops, or other electronics.

Note: 
    - you must only answer with `yes` or `no` only
    - you must not add any other information
"""

client = connect_to_client()

@track
def generate_response(user_input: str, system_prompt: str) -> str:
    """Generate a controlled response from the language model"""
    try:
        print(Fore.LIGHTYELLOW_EX + f"User: {user_input}")
        
        response = client.chat.completions.create(
            # model="gamma-2-2b-Instruct.gguf",
            model="Llama-3.2-3B-Instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            stream=True,
            max_tokens=500,
            temperature=0.0,  
            stop=["User:", "Assistant:" , "<|im_end|>"]
        )
        
        response_text = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                response_text += content
                print(Fore.LIGHTCYAN_EX + content, end="", flush=True)
        
        # Post-process to ensure compliance
        sanitized = response_text.strip().split('\n')[0].split('.')[0]
        return sanitized if sanitized else "I can only help with the listed mobile models."

    except Exception as e:
        print(Fore.RED + f"\nError: {str(e)}")
        return "I'm having technical difficulties. Please try again later."

def handle_user_query(user_input: str):
    """Process user query with validation"""
    # Check relevance first
    check = generate_response(user_input, SYSTEM_PROMPT_CHECK)

    if check.lower() == 'yes':
        return generate_response(user_input, SYSTEM_PROMPT_MAIN)
    else:
        print(Fore.LIGHTRED_EX + "\nI only handle mobile phone inquiries from the specified list.")
        return "Please ask about the mobile models I have available."

if __name__ == "__main__":
    # Example interaction
    handle_user_query("Do you have any laptops available?")
    print()
    handle_user_query("How much is the Samsung Galaxy S21 Ultra?")


### Summary ###

# as we try here 
# we can see that the llama 3.2-3B-Instruct model preforms better than the gamma-2-2b-Instruct.gguf model
# as it is more accurate and more relevant to the context of the conversation
# and better in the reasoing and the understanding of the context of the prompt and the user input
# so we will use the llama 3.2-3B-Instruct model in the next steps of the project 
# and we also will compare the gamma-2-2b-Instruct.gguf model with the llama 3.2-3B-Instruct model in the next steps of the project

# note: the gamma-2-2b-Instruct.gguf model is the model that we used in the previous steps of the project 
# the gamma model was F32 and the llama model was quentized to q8_0 
