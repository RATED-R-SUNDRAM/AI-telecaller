import google.generativeai as genai
import os
genai.configure(api_key="AIzaSyBu-EyvZ3TU_xzuUjKPpCz0grqroYyvm20")

model = genai.GenerativeModel("gemini-1.5-flash")
w
response = model.generate_content("Write a story about a magic backpack in 50 words.")
print(response.text)
