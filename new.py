from twilio.rest import Client
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather

# Twilio Account SID and Auth Token
account_sid = 'AC9e24b5583480570e7953cba4b0a32fc1'
auth_token = 'a747dba525f86f19cb6d81fdbc350ed7'
client = Client(account_sid, auth_token)

# Flask app for handling Twilio requests
app = Flask(__name__)
arr=[]
@app.route("/welcome", methods=['GET', 'POST'])
def welcome():
    response = VoiceResponse()

    # Welcome message and gather speech input
    gather = Gather(input="speech", action="/handle-speech", method="POST")
    gather.say("Welcome to our service. You can say 'Account Balance' to check your balance, "
               "'Customer Support' to connect with an agent, or 'Options' for more options.")
    response.append(gather)
    
    # If no speech received, say goodbye
    response.say("We didn’t receive any input. Goodbye!")
    
    return Response(str(response), mimetype="application/xml")

@app.route("/handle-speech", methods=['GET', 'POST'])
def handle_speech():
    response = VoiceResponse()
    transcript = request.values.get("SpeechResult", "").lower()  # Capture and process the speech text

    # Process response based on what the user said
    arr.append(transcript)
    if "balance" in transcript:
        response.say("Your account balance is $100.")
    elif "customer support" in transcript:
        response.say("Connecting you to customer support.")
        response.dial("+1234567890")  # Replace with actual customer support number
    elif "options" in transcript:
        response.say("For more options, visit our website.")
    else:
        response.say("I'm sorry, I didn't understand that. Please try again.")
        response.redirect("/welcome")  # Redirect back to the welcome message

    return Response(str(response), mimetype="application/xml")

def make_call():
    call = client.calls.create(
        to="+918219099751",  # Replace with recipient's phone number
        from_="+1 856 888 4984",  # Replace with your Twilio number
        url="http://your-server.com/welcome"  # Your server URL for Twilio to reach
    )
    print(f"Call initiated with SID: {call.sid}")

if __name__ == "__main__":
    make_call()
    app.run(debug=True)
    print(arr)
