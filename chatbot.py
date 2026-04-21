import os
import openai
from openai import OpenAI
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# This list stores the full conversation history
# Updated with your location context for accuracy
conversation_history = [
    {
        "role": "system",
        "content": "You are a helpful, friendly assistant. The user is Medhavi in Gurugram, India. Answer clearly and concisely."
    }
]

def chat(user_message):
    """Send a message and get a response."""
    try:
        # Add the user's message to history
        conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            max_tokens=500,
            temperature=0.7
        )

        # Extract the assistant's reply
        assistant_reply = response.choices[0].message.content

        # Add the reply to history so the bot remembers context
        conversation_history.append({
            "role": "assistant",
            "content": assistant_reply
        })
        return assistant_reply

    except openai.RateLimitError:
        # Custom message for quota/billing issues
        return "System Note: The chatbot is currently in standby. As soon as the API quota is updated or payment is processed, I'll be back to assist you!"
    except Exception as e:
        # Handles any other unexpected errors
        return f"An unexpected error occurred: {e}"

def main():
    """Main loop — runs the chatbot in the terminal."""
    print("=" * 40)
    print("   Python Chatbot — type 'quit' to exit")
    print("=" * 40)

    while True:
        # Get input from the user
        user_input = input("\nYou: ").strip()

        # Exit condition
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Bot: Goodbye! See you next time.")
            break

        # Skip empty input
        if not user_input:
            continue

        # Get and print the bot's response
        print("Bot: ", end="", flush=True)
        response = chat(user_input)
        print(response)

if __name__ == "__main__":
    main()