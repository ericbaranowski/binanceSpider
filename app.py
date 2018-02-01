from proxy import proxy
from flask import Flask

app = Flask(__name__)
proxyApp = proxy()
proxyApp.startGetProxy()

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
    return "remove done"


@app.route('/startGetProxy')
def startGetProxy():
    proxyApp.startGetProxy()
    return "get proxy done"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
