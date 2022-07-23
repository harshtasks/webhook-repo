from app import create_app

app = create_app()

# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def ese():
#   return "hwewer"

if __name__ == '__main__':
  app.run(host="0.0.0.0", port="9090", debug=True)