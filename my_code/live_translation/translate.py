import os
from dotenv import load_dotenv
from openai import OpenAI
import asyncio
import logging

import prompt

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=api_key)


async def translate_with_gpt(text: str, system_prompt: str) -> str:
    """
    This function uses OpenAI's GPT model to translate the provided text.

    Args:
        text (str): The text to be translated.
        system_prompt (str): The system prompt to guide the translation.

    Returns:
        str: The translated text.
    """

    completion = openai_client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
    )

    translated_text = completion.choices[0].message.content

    return translated_text


async def main():
    """
    creates a system prompt,
    translates a given text using the translate_with_gpt function,
    and prints the translated text.
    """
    system_prompt = prompt.system_prompt_template.format(
        lang1="English", lang2="Spanish"
    )
    text = "Hello, how are you?"
    try:
        translated_text = await translate_with_gpt(text, system_prompt)
    except Exception as e:
        logging.error(f"An error occurred while translating the text: {e}")
        return
    print(translated_text)


if __name__ == "__main__":
    asyncio.run(main())
