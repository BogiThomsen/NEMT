from flask import Flask, render_template
from user_api import users
import connexion

app = connexion.App(__name__, specification_dir = './')
app.add_api('swagger.yml')


@app.route('/')
def index():
    return render_template('index.html', users=users)



if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0')