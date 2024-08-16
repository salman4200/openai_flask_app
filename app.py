from flask import Flask, request, jsonify
from openai import OpenAI
import time
import os
app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

client = OpenAI(api_key=API_KEY)

@app.route('/run_assistant', methods=['POST'])
def run_assistant_endpoint():
    def run_assistant(message_body, assistant_id, client):

        thread = client.beta.threads.create()

        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message_body,
        )

        
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
        )

       
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            print(run.status)
            time.sleep(2)

       
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )

        
        output = []
        for message in reversed(messages.data):
            output.append(message.role + ": " + message.content[0].text.value)

        return output

    # Extract the message from the request
    data = request.get_json()
    message_body = data.get('message', 'Hello')

    # Run the assistant
    response = run_assistant(message_body, ASSISTANT_ID, client)

    # Return the response
    return jsonify({
        'statusCode': 200,
        'body': response
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
