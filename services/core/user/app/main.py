from flask import Flask, request
import json
import hashlib
import uuid
import secrets
import connexion

#Setups that is used throughout the user service.
app = connexion.App(__name__, specification_dir = './')
app.add_api('swagger.yml')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
  app.run(debug=True,host='localhost')