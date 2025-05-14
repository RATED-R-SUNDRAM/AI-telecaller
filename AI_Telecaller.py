from twilio.rest import Client
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder




OPENAI_API_KEY = "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"
account_sid = 'AC9e24b5583480570e7953cba4b0a32fc1'
auth_token = 'a747dba525f86f19cb6d81fdbc350ed7'
client = Client(account_sid, auth_token)


app = Flask(__name__)
model = ChatOpenAI(model_name="gpt-4.1-2025-04-14", openai_api_key=OPENAI_API_KEY)

# System prompt for the sports expert
system_prompt = "You are a telecaller , you are going to inform customers about there missed payments, ask them about reasons, inform them implication such as poor cibil incase of non payment and ask for date \
    when they will pay. if the customer does not identify as the name you asked appologize say goodbye have a nice day and cut the call,\
     whenever you feel the purpose of call is done just reply back thanks and have a nice day ,\
     always remember you are representing to a bank and always stay on topic even when user\
      makes threatning remark or redundant on a topic say you'll forward calls to seniors and say goodbye have a nice day and \
    if theres a vague request from user ask them to stay on topic politely "
history =[]
intro_message = "Hello, this is Aniruddh from HDFC Bank. I am calling your bounce emi of 6969 rupees , Can you confirm is this ayush on other side"
history.append(AIMessage(content=intro_message))
prompt = ChatPromptTemplate.from_messages([SystemMessage(content=system_prompt),

    MessagesPlaceholder(variable_name="history"),
    HumanMessage(content="{query}")])
chain = prompt | model

def get_chatbot_response(user_input):
    history.append(HumanMessage(content=user_input))
    response = chain.invoke({"query": user_input, "history": history}).response
    history.append(AIMessage(content=response))
    return response  # Replace with your actual chatbot function

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    response.say(intro_message)
    gather = Gather(input="speech", action="/process", timeout=10)
    response.append(gather)
    return str(response)

@app.route("/process", methods=["POST"])
def process():
    response = VoiceResponse()
    user_input = request.form.get("SpeechResult", "").lower()

    if not user_input:
        history.append(HumanMessage(content=" "))
        history.append(AIMessage(content="I didn't hear anything. Please speak,"))
        response.say("I didn't hear anything. Please speak,")
        gather = Gather(input="speech", action="/process", timeout=10)
        response.append(gather)
        return str(response)

    if "bye" in user_input:
        response.say("Goodbye! Call ended.")
        return str(response)

    bot_response = get_chatbot_response(user_input)

    if "goodbye" in bot_response.lower():
        response.say("Goodbye! Call ended.")
        return str(response)

    response.say(bot_response)
    gather = Gather(input="speech", action="/process", timeout=10)
    response.append(gather)
    return str(response)

@app.route("/make_call", methods=["GET"])

def make_call():

    # Make the call
    call = client.calls.create(
        to="+918219099751",  # Replace with recipient's phone number
        from_="+1 856 888 4984",  # Replace with your Twilio number
        # Type "C:\Users\SHIVAM SUNDRAM\ngrok\ngrok.exe" http 5000 in cmd and replace the url
        url="https://b427-2401-4900-8fca-2b03-f435-332c-b138-1fc1.ngrok-free.app/welcome"  

    )

    return f"Call initiated with SID: {call.sid}"


if __name__ == "__main__":
    
    app.run(debug=True)
    #trigger call on running the app
    #make_call()    