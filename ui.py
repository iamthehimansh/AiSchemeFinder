from flask import Flask, request, jsonify, Response, stream_with_context
import json
import os
from main import get_response
from datetime import datetime

app = Flask(__name__)

# Store chats in memory (in production, use a proper database)
chats = {}

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/chats')
def get_chats():
    return jsonify(list(chats.keys()))

@app.route('/api/chat/<chat_id>')
def get_chat(chat_id):
    return jsonify(chats.get(chat_id, []))

@app.route('/api/chat/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    if chat_id in chats:
        del chats[chat_id]
    return jsonify({"status": "success"})

@app.route('/api/chat')
def chat():
    message = request.args.get('message')
    chat_id = request.args.get('chat_id')
    
    if not chat_id:
        chat_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    if chat_id not in chats:
        chats[chat_id] = []
    
    # Add user message to chat history
    chats[chat_id].append({"role": "user", "content": message})
    
    def generate():
        assistant_message = ""
        for chunk in get_response(message):
            assistant_message += chunk
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        
        # Add assistant message to chat history after completion
        chats[chat_id].append({"role": "assistant", "content": assistant_message})
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.static_folder = 'templates'
    app.run(debug=True, port=5000)