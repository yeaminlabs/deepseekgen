import os
import sys

from openai import OpenAI


def chat(prompt: str) -> str:
    """Send a prompt to OpenRouter using the OpenAI SDK."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "Please set the OPENROUTER_API_KEY environment variable."
        )

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://github.com/example/deepseekgen",
            "X-Title": "SNBD Host Helper",
        },
        model="openai/gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content


def main():
    if len(sys.argv) < 2:
        print("Usage: python snbd_chat_helper.py \"Your question\"")
        return
    prompt = " ".join(sys.argv[1:])
    try:
        reply = chat(prompt)
        print(reply)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
