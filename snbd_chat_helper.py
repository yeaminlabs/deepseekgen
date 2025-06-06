import os
import requests
import json
import sys


def chat(prompt: str) -> str:
    """Send a prompt to the DeepSeek R1 model via OpenRouter API."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise EnvironmentError("Please set the OPENROUTER_API_KEY environment variable.")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # Optional headers recommended by OpenRouter
        "HTTP-Referer": "https://github.com/example/deepseekgen",  # Update with your domain if needed
        "X-Title": "SNBD Host Helper",
    }
    payload = {
        "model": "deepseek-ai/deepseek-llm-r1",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


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
