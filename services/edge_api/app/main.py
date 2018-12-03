from flask import Flask, render_template
import requests
import sys
app = Flask(__name__)

@app.route('/')
def index():
    text = requests.get("http://172.19.0.1:8085/api/addUser").text
    print(text, file=sys.stdout)
    return render_template('index.html', text=text)


if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0')