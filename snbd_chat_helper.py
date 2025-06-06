import os
import sys
import argparse
import requests


def chat(prompt: str, model: str) -> str:
    """Send a prompt to OpenRouter using a direct HTTP request."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "Please set the OPENROUTER_API_KEY environment variable."
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }

    res = requests.post(
        "https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers
    )
    res.raise_for_status()
    j = res.json()
    return j.get("choices", [{}])[0].get("message", {}).get("content", "")


def main():
    parser = argparse.ArgumentParser(description="SNBD chat helper using OpenRouter")
    parser.add_argument("prompt", nargs="+", help="Prompt text")
    parser.add_argument(
        "-m",
        "--model",
        default="mistral/mistral-7b-instruct",
        help="Model to use",
    )
    args = parser.parse_args()

    prompt = " ".join(args.prompt)

    try:
        reply = chat(prompt, args.model)
        print(reply)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
