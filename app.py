from proxy import proxy
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/randomProxy')
def randomproxy():
    return proxyApp.randomChoice()

if __name__ == '__main__':
    proxyApp = proxy()
    proxyApp.startGetProxy()
    app.run(host='0.0.0.0', debug=True)
