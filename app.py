import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


def assistant_prompt():
    return """You are meant to imitate a student named "Ashley" who is the AI Team Lead for a club called ACM. You are friendly, helpful, and respond excitedly to the user. Additional info to keep in mind is that the AI Team hosts workshops every Thursday at 6:00 PM. Please keep your responses to only a few sentences."""  # Prompt given to the model

def first_message():
    return """Hi! I'm Ashley. I'm a third year Computer Science student at CSUF looking to make the world a smarter place via artificial intelligence."""

conversation=[{"role": "system", "content": assistant_prompt()}, 
              {"role": "assistant", "content": first_message()}]    # The conversation is an array of messages
                                                                    # "system" messages are instructions given to the model
                                                                    # "user" messages are given by the person having the conversation
                                                                    # "assistant" messages are responses given by the model

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]                                    # Gets a "prompt" or "message" from the user
        conversation.append({"role": "user", "content": format(prompt)})   # Adds the user's message to the conversation array

        response = openai.ChatCompletion.create(                           # Creating a "response" object, which contains a response message from the model
            model="gpt-3.5-turbo",
            messages=conversation                                          # We pass in the conversation so far
        )

        conversation.append({"role": "assistant", "content": format(response['choices'][0]['message']['content'])}) # Adds the model's response to the conversation array
        return redirect(url_for("index", result=response['choices'][0]['message']['content']))                      # Redirects the user to the index page, with the model's response as a parameter

    result = request.args.get("result")
    return render_template("index.html", result=result)