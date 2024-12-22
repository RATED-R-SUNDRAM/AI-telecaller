from twilio.rest import Client
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import google.generativeai as genai
import os
genai.configure(api_key="AIzaSyBu-EyvZ3TU_xzuUjKPpCz0grqroYyvm20")
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize the chat session with your Gemini API key
api_key = "AIzaSyBu-EyvZ3TU_xzuUjKPpCz0grqroYyvm20"  # Replace with your actual API key
#chat_session = GeminiChatSession(api_key)

# Start a new session
# print(chat_session.start_session())  # Outputs: "Hello! How can I assist you today?"

# # Continue the conversation
# while True:
#     user_input = input("You: ")
#     if user_input.lower() == "exit":
#         print("Ending session. Goodbye!")
#         break
#     response = chat_session.send_message(user_input)
#     print(f"Gemini: {response}")

# Twilio Account SID and Auth Token
account_sid = 'AC9e24b5583480570e7953cba4b0a32fc1'
auth_token = 'a747dba525f86f19cb6d81fdbc350ed7'
client = Client(account_sid, auth_token)
arr=["Hi Sir! I am calling from ABC BANK hope you are doing good"]
# Flask app for handling Twilio requests

def fun(arr):
    msg = ",".join(arr)
    print(msg)
    
    # Initializing flags to track whether each objective has been completed
    objective_1_completed = False
    objective_2_completed = False
    objective_3_completed = False
    
    # The conversation so far is provided in a comma-separated list below
    context = f"""
    You are a telecaller speaking to a person named Rohit, reminding him about a due payment of 5000, which was due on the 5th of the month. 
    The conversation has been ongoing, and you are in the middle of it. The conversation so far is provided in a comma-separated list below, 
    where each entry represents an exchange between you and Rohit, with the last message being from him.
    
    The conversation so far: [{msg}]
    
    Your objective is to continue the conversation empathetically, keeping the following goals in mind:
    
    1. **Understand why the payment hasn't been made:** Ask Rohit why he hasn't been able to make the payment yet. Be empathetic and non-judgmental.
    2. **Inform about the consequences:** Let him know that there will be financial implications if the payment isn't made soon, but do so in a gentle and understanding tone.
    3. **Ask for a payment commitment:** Politely ask when he will be able to make the payment.
    
    Here’s the flow to follow:
    - If **none** of the objectives have been addressed, begin by asking about the reason for non-payment.
    - If **objective 1** has been addressed, move on to inform about the financial implications (**objective 2**).
    - If **objectives 1 and 2** have been completed, ask when he will make the payment (**objective 3**).
    - If **all three** objectives have been addressed, politely end the conversation with a warm goodbye, wishing him a good day.
    
    **Important Instructions:**
    - Track which objective has been addressed based on the conversation so far.
    - If a question related to an objective has already been answered, skip it and move on to the next objective.
    - If Rohit expresses that he doesn't want to answer a question or provides a satisfactory response, consider that objective complete and move on.
    - Avoid asking the same question more than once.
    - Keep the conversation natural, engaging, and empathetic.

    **Current status:**
    - Objective 1: {'Completed' if objective_1_completed else 'Pending'}
    - Objective 2: {'Completed' if objective_2_completed else 'Pending'}
    - Objective 3: {'Completed' if objective_3_completed else 'Pending'}
    """
    
    # Generate the response based on the context
    response = model.generate_content(context)
    return response.text

def fun2(arr):
    msg=",".join(arr)
    context = f"the above is a transcript of a call between telecaller and a person regarding his late payment, the conversation\
        is a comma separated back and forth where first message is of telecaller and last message is of person, the conversation is as below : [{msg}] \
        find out the reason for late payment and summarise in couple of words also find out the day the person promised to pay"
    response = model.generate_content(context)
app = Flask(__name__)
text="Hi Sir! I am calling from ABC BANK hope you are doing good"
@app.route("/welcome", methods=['GET', 'POST'])
def welcome():
    response = VoiceResponse()
    
    # Welcome message and gather speech input
    gather = Gather(input="speech", action="/handle-speech", method="POST")
    #text=arr[-1]
    gather.say(f"{text}")
    response.append(gather)
    
    # If no speech is received
    response.say("I didn’t catch that. Goodbye!")
    
    return Response(str(response), mimetype="application/xml")

@app.route("/handle-speech", methods=['GET', 'POST'])
def handle_speech():
    global text
    """Processes speech input and keeps the conversation going."""
    response = VoiceResponse()
    transcript = request.values.get("SpeechResult", "").strip().lower()  # Capture user speech
    if "goodbye" in arr[-1]:
        print(fun2(arr))
        response.hangup()

    if transcript:
        # End the call if the user says "Goodbye"
        if "goodbye" in transcript:
            response.say("Goodbye! Have a great day!")
            print(fun2(arr))
            response.hangup()
            
        else:
            # Echo the user's input prefixed with "Please"
            #global text
            arr.append(transcript)
            text=fun(arr)
            arr.append(text)
            # text=f"Please {transcript}. What else would you like to say?"
            
            response.redirect("/welcome")  # Redirect back to welcome for continuous conversation
    else:
        # Redirect to welcome if no input is detected
        #global text
        msg=arr[-1]
        text=f"I'm sorry, I didn't catch that, I was saying {msg}"
        response.redirect("/welcome")

    return Response(str(response), mimetype="application/xml")
@app.route("/test", methods=["GET"])
def test():
    return "this is a test"
@app.route("/trigger-call", methods=["GET"])
def make_call():

    # Make the call
    call = client.calls.create(
        to="+918219099751",  # Replace with recipient's phone number
        from_="+1 856 888 4984",  # Replace with your Twilio number
        # Type "C:\Users\SHIVAM SUNDRAM\ngrok\ngrok.exe" http 5000 in cmd and replace the url
        url="https://7af1-2401-4900-1c9a-5ea-dc04-9410-112c-228f.ngrok-free.app/welcome"  

    )

    return f"Call initiated with SID: {call.sid}"


if __name__ == "__main__":
    
    app.run(debug=True)
    #trigger call on running the app
    #make_call()    