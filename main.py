import argparse
import os

import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def ask_to_chatgpt(prompt: str, sys_setting: str) -> tuple[str, int]:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": sys_setting},
            {"role": "user", "content": prompt},
        ],
    )

    message = response["choices"][0]["message"]["content"]
    token = int(response["usage"]["total_tokens"])
    return (message, token)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--system", type=str, help="Input system setting for ChatGPT"
    )
    args = parser.parse_args()
    sys_setting = args.system

    fee = 0
    try:
        while True:

            user_input = input("\033[34m> \033[0m")
            if len(user_input) > 500:
                print("Please input 500 characters or fewer.")
                continue

            message, token = ask_to_chatgpt(user_input, sys_setting)
            fee += token * 0.000002

            print(f"\033[32m{message}\033[0m")

    except KeyboardInterrupt:
        print(f"\n\nBye! API usage fee: {fee:.4f}$")


if __name__ == "__main__":
    main()
