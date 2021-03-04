# EE461L Group 13
# Final Project

# Notes
# Trailing slash fix https://stackoverflow.com/questions/40365390/trailing-slash-in-flask-route


from flask import Flask, render_template


app = Flask(__name__, static_url_path="/static")

@app.route('/')
def index():
    return "hey guys this is flask"

if __name__ == "__main__":
    app.run(debug=True, host="localhost")