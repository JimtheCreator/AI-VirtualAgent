from flask import Flask, render_template, request, jsonify
import os
from chatbot import chat_response


# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the templates directory
template_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'templates'))

# Construct paths to the CSS, JS, and image files
css_path = os.path.join(script_dir, 'src', 'javascript', 'style.css')
js_path = os.path.join(script_dir, 'src', 'javascript', 'app.js')
img_path = os.path.join(script_dir, 'src', 'javascript', 'images', 'chatbox-icon.svg')

# Convert paths to a format that can be used in HTML
css_path = os.path.relpath(css_path, os.path.dirname(__file__))
js_path = os.path.relpath(js_path, os.path.dirname(__file__))
img_path = os.path.relpath(img_path, os.path.dirname(__file__))

# Initialize the Flask application with the template directory
app = Flask(__name__, template_folder=template_dir)

@app.get("/")
def indexGet():
    return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = chat_response(text)
    message = {"answer": response}
    
    return jsonify(message)

if __name__ == '__main__':
    print(app.template_folder)  # Should print the path to your templates folder
    app.run(debug=True)
    
    