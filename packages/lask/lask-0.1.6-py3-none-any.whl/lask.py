#!/usr/bin/env python3
"""
lask: A CLI tool to prompt ChatGPT and other LLMs from the terminal.
Usage:
    lask "Your prompt here"
This is a minimal implementation using OpenAI's API. Set your API key in the OPENAI_API_KEY environment variable.
"""
import os
import sys
import requests

def main():
    if len(sys.argv) < 2:
        print("Usage: lask 'Your prompt here'")
        sys.exit(1)
    prompt = " ".join(sys.argv[1:])
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: Please set the OPENAI_API_KEY environment variable.")
        sys.exit(1)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4.1",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    print(f"Prompting OpenAI API with: {prompt}\n")
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.text}")
        sys.exit(1)
    result = response.json()
    print(result["choices"][0]["message"]["content"].strip())

if __name__ == "__main__":
    main()