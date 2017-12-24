from proxy import proxy
from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def index():
    return "Hello, World!"


@app.route('/randomProxy')
def randomproxy():
    return str(proxyApp.randomChoice())


@app.route('/showAllProxy')
def showAllProxy():
    return str(proxyApp.showAllProxy())


@app.route('/removeProxy/<ip>', methods=['GET'])
def removeProxy(ip):
    proxyApp.removeProxy(ip)
    return


@app.route('/startGetProxy')
def startGetProxy():
    proxyApp.startGetProxy()
    return


if __name__ == '__main__':
    proxyApp = proxy()
    proxyApp.startGetProxy()
    app.run(host='0.0.0.0', debug=True)
