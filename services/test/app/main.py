from flask import Flask, render_template
import requests
import json
app = Flask(__name__)

@app.route('/')
def index():
    text = requests.get("http://172.19.0.1:8085/api/hej").json()
    return render_template('index.html', text=text["1"])


if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0')