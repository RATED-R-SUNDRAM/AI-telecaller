import google.generativeai as genai
import os
genai.configure(api_key="AIzaSyBu-EyvZ3TU_xzuUjKPpCz0grqroYyvm20")
model = genai.GenerativeModel("gemini-1.5-flash")

arr=[]
def fun(text):
    response = model.generate_content(text)
    return response.text

print(fun("Hello, how are you?"))
import requests

class GeminiChatSession:
    def __init__(self, api_key, default_message="Hello! How can I assist you today?"):
        """
        Initializes a GeminiChatSession.

        :param api_key: Your Gemini API key for authentication.
        :param default_message: Default message to start a new session.
        """
        self.api_key = api_key
        self.default_message = default_message
        self.conversation_context = []  # Stores the conversation history for the session

    def send_message(self, message):
        """
        Sends a message to the Gemini API and returns the response.

        :param message: User's input message.
        :return: Gemini's response to the message.
        """
        # Add user message to the context
        self.conversation_context.append({"role": "user", "content": message})

        # Prepare API payload
        payload = {
            "messages": self.conversation_context
        }

        # Replace with the actual Gemini API endpoint
        url = "https://api.gemini.com/models/gemini-1.5-flash"  
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            gemini_response = response.json()
            # Extract and save Gemini's response
            bot_message = gemini_response.get("message", {}).get("content", "")
            self.conversation_context.append({"role": "assistant", "content": bot_message})
            return bot_message
        else:
            return f"Error: {response.status_code} - {response.text}"

    def start_session(self):
        """
        Starts a new session with the default message.

        :return: Default message to initiate the conversation.
        """
        self.conversation_context = []  # Clear any previous session context
        return self.default_message

api_key = "AIzaSyBu-EyvZ3TU_xzuUjKPpCz0grqroYyvm20"  # Replace with your actual API key
chat_session = GeminiChatSession(api_key)

# Start a new session
print(chat_session.start_session())  # Outputs: "Hello! How can I assist you today?"

# Continue the conversation
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Ending session. Goodbye!")
        break
    response = chat_session.send_message(user_input)
    print(f"Gemini: {response}")