import os
from dotenv import load_dotenv
from anthropic import Anthropic
from system_prompt import SYSTEM_PROMPT

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

conversation_history = []

def chat(user_input):
    """Send a message and get a response, keeping full conversation history."""
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=conversation_history
    )

    assistant_reply = response.content[0].text

    conversation_history.append({
        "role": "assistant",
        "content": assistant_reply
    })

    return assistant_reply

def main():
    print("=" * 60)
    print("  Network Troubleshooter Bot — CLI Mode")
    print("  Type 'exit' to quit | Type 'reset' to clear history")
    print("=" * 60)
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye.")
            break

        if user_input.lower() == "reset":
            conversation_history.clear()
            print("--- Conversation history cleared ---\n")
            continue

        reply = chat(user_input)
        print(f"\nBot: {reply}\n")

if __name__ == "__main__":
    main()