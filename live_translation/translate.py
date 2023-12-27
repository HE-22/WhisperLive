import os
import time
from dotenv import load_dotenv
from openai import OpenAI
import logging

from live_translation import prompt

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=api_key)
logging.basicConfig(level=logging.INFO)


def translate_text(text: str, lang1: str, lang2: str) -> str:
    """
    - Uses OpenAI's GPT model to translate the provided text.
    - Calls the _translate_with_gpt function to perform the translation.

    Args:
        text (str): The text to be translated.
        lang1 (str): The source language.
        lang2 (str): The target language.

    Returns:
        str: The translated text.
    """
    translated_text = ""
    try:
        translated_text = _translate_with_gpt(text, lang1, lang2)
    except Exception as e:
        logging.error(f"An error occurred while translating the text: {e}")

    return translated_text


def _translate_with_gpt(text: str, lang1: str, lang2: str) -> str:
    """
    - Uses OpenAI's GPT model to translate the provided text.
    - Creates a system prompt based on the source and target languages.
    - Sends a request to the OpenAI API and retrieves the translated text.

    Args:
        text (str): The text to be translated.
        lang1 (str): The source language.
        lang2 (str): The target language.

    Returns:
        str: The translated text.
    """
    system_prompt = prompt.system_prompt_template.format(lang1=lang1, lang2=lang2)
    translated_text = ""
    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
        )
        translated_text = completion.choices[0].message.content
    except Exception as e:
        logging.error(f"An error occurred while translating the text: {e}")

    return translated_text


# async def main():
#     """
#     creates a system prompt,
#     translates a given text using the translate_with_gpt function,
#     and prints the translated text.
#     """
#     system_prompt = prompt.system_prompt_template.format(
#         lang1="English", lang2="Spanish"
#     )
#     text = "Hello, how are you?"

#     try:
#         translated_text = await _translate_with_gpt(text, system_prompt)
#     except Exception as e:
#         logging.error(f"An error occurred while translating the text: {e}")
#         return
#     print(translated_text)


# if __name__ == "__main__":
#     start_time = time.time()
#     asyncio.run(main())
#     end_time = time.time()
#     logging.info(f"Execution time: {end_time - start_time} seconds")
