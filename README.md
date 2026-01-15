# 📞 AI Telecaller: AI calls with Twilio + LangChain


## 🚀 What It Does

* Makes real calls with Twilio.
* Greets and listens using speech recognition.
* Uses GPT-4.1 via LangChain for smart replies.
* Keeps conversation context.
* Handles silence, wrong ID, threats, and ends calls professionally.

---

## 🧩 Tech Stack

* Flask webhooks
* Twilio Voice API
* LangChain + OpenAI GPT-4.1
* Ngrok for local tunneling
* dotenv for secrets

---

## ⚡ How It Works

1. Flask app runs with call endpoints.
2. Twilio calls and plays intro.
3. User speaks; Twilio sends transcript.
4. LangChain generates reply.
5. Twilio plays reply; loop continues.
6. Call ends gracefully.

---

## 🎯 Why It’s Special

* Drives calls purposefully.
* Bank-grade professionalism.
* Production-ready setup.
* Robust failsafe logic.

---

## 🔧 Setup

1. Install: `pip install flask twilio langchain-openai python-dotenv`
2. Run ngrok: `ngrok http 5000`
3. Start Flask: `python app.py`
4. Trigger call: visit `/make_call`

---

## 👨‍💻 Author

Shivam Sundram — blending data science, Gen AI, and production engineering.
